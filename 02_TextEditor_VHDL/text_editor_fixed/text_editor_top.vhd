-- ============================================================
-- text_editor_top.vhd
-- LAB6 Mini-Project 1: VGA Text Terminal with Line Editor
-- DE2 Board - 640x480 VGA, PS/2 Keyboard
-- ============================================================

LIBRARY IEEE;
USE IEEE.STD_LOGIC_1164.ALL;
USE IEEE.STD_LOGIC_ARITH.ALL;
USE IEEE.STD_LOGIC_UNSIGNED.ALL;

ENTITY text_editor_top IS
  PORT (
    CLOCK_50    : IN  STD_LOGIC;
    KEY         : IN  STD_LOGIC_VECTOR(3 DOWNTO 0);
    PS2_CLK     : IN  STD_LOGIC;
    PS2_DAT     : IN  STD_LOGIC;
    VGA_R       : OUT STD_LOGIC_VECTOR(9 DOWNTO 0);
    VGA_G       : OUT STD_LOGIC_VECTOR(9 DOWNTO 0);
    VGA_B       : OUT STD_LOGIC_VECTOR(9 DOWNTO 0);
    VGA_HS      : OUT STD_LOGIC;
    VGA_VS      : OUT STD_LOGIC;
    VGA_BLANK   : OUT STD_LOGIC;
    VGA_SYNC    : OUT STD_LOGIC;   -- tied to '0', DE2 requires it
    VGA_CLK     : OUT STD_LOGIC
  );
END text_editor_top;

ARCHITECTURE rtl OF text_editor_top IS

  -- ---- Constants -----------------------------------------------
  CONSTANT COLS   : INTEGER := 80;
  CONSTANT ROWS   : INTEGER := 30;

  -- ---- Component declarations ----------------------------------
  -- NOTE: component name is vga_sync_mod to avoid clash with port VGA_SYNC
  COMPONENT VGA_SYNC
    PORT (
      clock_50Mhz                   : IN  STD_LOGIC;
      red, green, blue              : IN  STD_LOGIC;
      red_out, green_out, blue_out  : OUT STD_LOGIC;
      horiz_sync_out, vert_sync_out : OUT STD_LOGIC;
      video_on, pixel_clock         : OUT STD_LOGIC;
      pixel_row, pixel_column       : OUT STD_LOGIC_VECTOR(9 DOWNTO 0)
    );
  END COMPONENT;

  COMPONENT keyboard
    PORT (
      keyboard_clk, keyboard_data   : IN  STD_LOGIC;
      clock_25Mhz, reset, read      : IN  STD_LOGIC;
      scan_code                     : OUT STD_LOGIC_VECTOR(7 DOWNTO 0);
      scan_ready                    : OUT STD_LOGIC
    );
  END COMPONENT;

  COMPONENT Char_ROM
    PORT (
      clock             : IN  STD_LOGIC;
      character_address : IN  STD_LOGIC_VECTOR(5 DOWNTO 0);
      font_row, font_col: IN  STD_LOGIC_VECTOR(2 DOWNTO 0);
      rom_mux_output    : OUT STD_LOGIC
    );
  END COMPONENT;

  -- ---- Internal signals ----------------------------------------
  SIGNAL reset        : STD_LOGIC;

  -- VGA
  SIGNAL pixel_row    : STD_LOGIC_VECTOR(9 DOWNTO 0);
  SIGNAL pixel_col    : STD_LOGIC_VECTOR(9 DOWNTO 0);
  SIGNAL video_on     : STD_LOGIC;
  SIGNAL pixel_clk    : STD_LOGIC;
  SIGNAL vga_r_bit    : STD_LOGIC;
  SIGNAL vga_g_bit    : STD_LOGIC;
  SIGNAL vga_b_bit    : STD_LOGIC;
  SIGNAL vga_r_out    : STD_LOGIC;
  SIGNAL vga_g_out    : STD_LOGIC;
  SIGNAL vga_b_out    : STD_LOGIC;

  -- Keyboard
  SIGNAL scan_code    : STD_LOGIC_VECTOR(7 DOWNTO 0);
  SIGNAL scan_ready   : STD_LOGIC;
  SIGNAL kb_read      : STD_LOGIC;
  SIGNAL prev_ready   : STD_LOGIC;
  SIGNAL break_flag   : STD_LOGIC;
  SIGNAL extended_flag: STD_LOGIC;

  -- Text buffer: 80 cols x 30 rows, 7-bit CHAR_ROM address
  TYPE char_row_t IS ARRAY (0 TO COLS-1) OF STD_LOGIC_VECTOR(6 DOWNTO 0);
  TYPE char_buf_t IS ARRAY (0 TO ROWS-1) OF char_row_t;
  SIGNAL char_buf     : char_buf_t;

  -- Cursor
  SIGNAL cur_col      : INTEGER RANGE 0 TO COLS;
  SIGNAL cur_row      : INTEGER RANGE 0 TO ROWS-1;

  -- Blink
  SIGNAL blink_cnt    : STD_LOGIC_VECTOR(24 DOWNTO 0);
  SIGNAL blink        : STD_LOGIC;

  -- CHAR_ROM wiring
  SIGNAL char_addr    : STD_LOGIC_VECTOR(5 DOWNTO 0);
  SIGNAL font_row_sig : STD_LOGIC_VECTOR(2 DOWNTO 0);
  SIGNAL font_col_sig : STD_LOGIC_VECTOR(2 DOWNTO 0);
  SIGNAL rom_out      : STD_LOGIC;

  -- Display cell
  SIGNAL disp_row     : INTEGER RANGE 0 TO 63;
  SIGNAL disp_col     : INTEGER RANGE 0 TO 127;
  SIGNAL is_cursor    : STD_LOGIC;
  SIGNAL in_bounds    : STD_LOGIC;

BEGIN

  reset <= NOT KEY(0);

  -- ---- VGA_SYNC instantiation ----------------------------------
  U_VGA : VGA_SYNC
    PORT MAP (
      clock_50Mhz    => CLOCK_50,
      red            => vga_r_bit,
      green          => vga_g_bit,
      blue           => vga_b_bit,
      red_out        => vga_r_out,
      green_out      => vga_g_out,
      blue_out       => vga_b_out,
      horiz_sync_out => VGA_HS,
      vert_sync_out  => VGA_VS,
      video_on       => video_on,
      pixel_clock    => pixel_clk,
      pixel_row      => pixel_row,
      pixel_column   => pixel_col
    );

  -- Replicate single bit to 10-bit VGA buses
  VGA_R     <= (OTHERS => vga_r_out);
  VGA_G     <= (OTHERS => vga_g_out);
  VGA_B     <= (OTHERS => vga_b_out);
  VGA_BLANK <= video_on;
  VGA_SYNC  <= '0';
  VGA_CLK   <= pixel_clk;

  -- ---- Keyboard ------------------------------------------------
  U_KB : keyboard
    PORT MAP (
      keyboard_clk  => PS2_CLK,
      keyboard_data => PS2_DAT,
      clock_25Mhz   => pixel_clk,
      reset         => reset,
      read          => kb_read,
      scan_code     => scan_code,
      scan_ready    => scan_ready
    );

  -- ---- Character cell being displayed --------------------------
  -- Each char is 8 pixels wide, 16 pixels tall (font scaled x2 vertically)
  disp_row <= CONV_INTEGER(pixel_row(9 DOWNTO 4));  -- pixel_row / 16
  disp_col <= CONV_INTEGER(pixel_col(9 DOWNTO 3));  -- pixel_col / 8

  in_bounds <= '1' WHEN (disp_row < ROWS AND disp_col < COLS) ELSE '0';

  -- CHAR_ROM address: from buffer, or space if out of bounds
  char_addr <= char_buf(disp_row)(disp_col)(5 DOWNTO 0)
               WHEN in_bounds = '1' ELSE "100000";

  font_row_sig <= pixel_row(3 DOWNTO 1);  -- 3 bits, scaled x2
  font_col_sig <= pixel_col(2 DOWNTO 0);

  -- ---- CHAR_ROM ------------------------------------------------
  U_CROM : Char_ROM
    PORT MAP (
      clock             => pixel_clk,
      character_address => char_addr,
      font_row          => font_row_sig,
      font_col          => font_col_sig,
      rom_mux_output    => rom_out
    );

  -- ---- Cursor at current typing position -----------------------
  is_cursor <= '1' WHEN (disp_row = cur_row AND disp_col = cur_col
                         AND blink = '1' AND in_bounds = '1')
               ELSE '0';

  -- ---- Pixel colour output (white text, black background) ------
  PROCESS (video_on, rom_out, is_cursor, in_bounds)
    VARIABLE px : STD_LOGIC;
  BEGIN
    px := rom_out XOR is_cursor;
    IF video_on = '1' AND in_bounds = '1' THEN
      vga_r_bit <= px;
      vga_g_bit <= px;
      vga_b_bit <= px;
    ELSE
      vga_r_bit <= '0';
      vga_g_bit <= '0';
      vga_b_bit <= '0';
    END IF;
  END PROCESS;

  -- ---- Blink counter -------------------------------------------
  PROCESS (CLOCK_50, reset)
  BEGIN
    IF reset = '1' THEN
      blink_cnt <= (OTHERS => '0');
      blink     <= '1';
    ELSIF rising_edge(CLOCK_50) THEN
      blink_cnt <= blink_cnt + 1;
      IF blink_cnt = 0 THEN
        blink <= NOT blink;
      END IF;
    END IF;
  END PROCESS;

  -- ---- Keyboard FSM & text buffer ------------------------------
  PROCESS (CLOCK_50, reset)
    VARIABLE char_v : STD_LOGIC_VECTOR(6 DOWNTO 0);
    VARIABLE do_char : BOOLEAN;
  BEGIN
    IF reset = '1' THEN
      FOR ri IN 0 TO ROWS-1 LOOP
        FOR ci IN 0 TO COLS-1 LOOP
          char_buf(ri)(ci) <= "0100000";  -- space
        END LOOP;
      END LOOP;
      cur_col       <= 0;
      cur_row       <= 0;
      prev_ready    <= '0';
      kb_read       <= '0';
      break_flag    <= '0';
      extended_flag <= '0';

    ELSIF rising_edge(CLOCK_50) THEN
      kb_read  <= '0';
      do_char  := FALSE;
      char_v   := "0000000";

      IF scan_ready = '1' AND prev_ready = '0' THEN
        kb_read <= '1';

        IF scan_code = X"E0" THEN
          extended_flag <= '1';

        ELSIF scan_code = X"F0" THEN
          break_flag <= '1';

        ELSE
          IF break_flag = '0' THEN
            -- ---- Key PRESS: decode scan code ----
            CASE scan_code IS
              WHEN X"1C" => char_v := "0000001"; do_char := TRUE;  -- A
              WHEN X"32" => char_v := "0000010"; do_char := TRUE;  -- B
              WHEN X"21" => char_v := "0000011"; do_char := TRUE;  -- C
              WHEN X"23" => char_v := "0000100"; do_char := TRUE;  -- D
              WHEN X"24" => char_v := "0000101"; do_char := TRUE;  -- E
              WHEN X"2B" => char_v := "0000110"; do_char := TRUE;  -- F
              WHEN X"34" => char_v := "0000111"; do_char := TRUE;  -- G
              WHEN X"33" => char_v := "0001000"; do_char := TRUE;  -- H
              WHEN X"43" => char_v := "0001001"; do_char := TRUE;  -- I
              WHEN X"3B" => char_v := "0001010"; do_char := TRUE;  -- J
              WHEN X"42" => char_v := "0001011"; do_char := TRUE;  -- K
              WHEN X"4B" => char_v := "0001100"; do_char := TRUE;  -- L
              WHEN X"3A" => char_v := "0001101"; do_char := TRUE;  -- M
              WHEN X"31" => char_v := "0001110"; do_char := TRUE;  -- N
              WHEN X"44" => char_v := "0001111"; do_char := TRUE;  -- O
              WHEN X"4D" => char_v := "0010000"; do_char := TRUE;  -- P
              WHEN X"15" => char_v := "0010001"; do_char := TRUE;  -- Q
              WHEN X"2D" => char_v := "0010010"; do_char := TRUE;  -- R
              WHEN X"1B" => char_v := "0010011"; do_char := TRUE;  -- S
              WHEN X"2C" => char_v := "0010100"; do_char := TRUE;  -- T
              WHEN X"3C" => char_v := "0010101"; do_char := TRUE;  -- U
              WHEN X"2A" => char_v := "0010110"; do_char := TRUE;  -- V
              WHEN X"1D" => char_v := "0010111"; do_char := TRUE;  -- W
              WHEN X"22" => char_v := "0011000"; do_char := TRUE;  -- X
              WHEN X"35" => char_v := "0011001"; do_char := TRUE;  -- Y
              WHEN X"1A" => char_v := "0011010"; do_char := TRUE;  -- Z
              WHEN X"45" => char_v := "0110000"; do_char := TRUE;  -- 0
              WHEN X"16" => char_v := "0110001"; do_char := TRUE;  -- 1
              WHEN X"1E" => char_v := "0110010"; do_char := TRUE;  -- 2
              WHEN X"26" => char_v := "0110011"; do_char := TRUE;  -- 3
              WHEN X"25" => char_v := "0110100"; do_char := TRUE;  -- 4
              WHEN X"2E" => char_v := "0110101"; do_char := TRUE;  -- 5
              WHEN X"36" => char_v := "0110110"; do_char := TRUE;  -- 6
              WHEN X"3D" => char_v := "0110111"; do_char := TRUE;  -- 7
              WHEN X"3E" => char_v := "0111000"; do_char := TRUE;  -- 8
              WHEN X"46" => char_v := "0111001"; do_char := TRUE;  -- 9
              WHEN X"29" => char_v := "0100000"; do_char := TRUE;  -- Space
              WHEN X"49" => char_v := "0111010"; do_char := TRUE;  -- . period

              WHEN X"5A" =>
                -- ENTER: move to next line
                cur_col <= 0;
                IF cur_row = ROWS-1 THEN
                  -- Scroll up
                  FOR ri IN 0 TO ROWS-2 LOOP
                    char_buf(ri) <= char_buf(ri+1);
                  END LOOP;
                  FOR ci IN 0 TO COLS-1 LOOP
                    char_buf(ROWS-1)(ci) <= "0100000";
                  END LOOP;
                ELSE
                  cur_row <= cur_row + 1;
                END IF;

              WHEN X"66" =>
                -- BACKSPACE
                IF cur_col > 0 THEN
                  char_buf(cur_row)(cur_col-1) <= "0100000";
                  cur_col <= cur_col - 1;
                ELSIF cur_row > 0 THEN
                  cur_row <= cur_row - 1;
                  cur_col <= COLS - 1;
                END IF;

              WHEN OTHERS => NULL;
            END CASE;

            -- Place printable character in buffer
            IF do_char THEN
              char_buf(cur_row)(cur_col) <= char_v;
              IF cur_col = COLS-1 THEN
                cur_col <= 0;
                IF cur_row = ROWS-1 THEN
                  FOR ri IN 0 TO ROWS-2 LOOP
                    char_buf(ri) <= char_buf(ri+1);
                  END LOOP;
                  FOR ci IN 0 TO COLS-1 LOOP
                    char_buf(ROWS-1)(ci) <= "0100000";
                  END LOOP;
                ELSE
                  cur_row <= cur_row + 1;
                END IF;
              ELSE
                cur_col <= cur_col + 1;
              END IF;
            END IF;

          END IF;  -- break_flag = '0'

          -- Clear flags after any real key code
          extended_flag <= '0';
          break_flag    <= '0';
        END IF;
      END IF;

      prev_ready <= scan_ready;
    END IF;
  END PROCESS;

END rtl;
