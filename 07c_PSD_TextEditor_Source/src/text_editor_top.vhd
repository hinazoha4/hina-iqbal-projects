library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;

entity text_editor_top is
    port (
        CLOCK_50  : in  std_logic;
        KEY       : in  std_logic_vector(3 downto 0);
        SW        : in  std_logic_vector(17 downto 0);
        LEDR      : out std_logic_vector(17 downto 0);
        PS2_CLK   : in  std_logic;
        PS2_DAT   : in  std_logic;
        VGA_R     : out std_logic_vector(9 downto 0);
        VGA_G     : out std_logic_vector(9 downto 0);
        VGA_B     : out std_logic_vector(9 downto 0);
        VGA_HS    : out std_logic;
        VGA_VS    : out std_logic;
        VGA_CLK   : out std_logic;
        VGA_BLANK : out std_logic;
        VGA_SYNC  : out std_logic
    );
end entity;

architecture rtl of text_editor_top is
    constant COLS : integer := 80;
    constant ROWS : integer := 60;
    constant MEM_SIZE : integer := COLS * ROWS;
    constant BLANK_CHAR : std_logic_vector(5 downto 0) := "111111";

    type text_mem_t is array (0 to MEM_SIZE - 1) of std_logic_vector(5 downto 0);
    function ps2_to_char(scan : std_logic_vector(7 downto 0)) return std_logic_vector is
    begin
        case scan is
            when x"1C" => return "000001"; -- A
            when x"32" => return "000010"; -- B
            when x"21" => return "000011"; -- C
            when x"23" => return "000100"; -- D
            when x"24" => return "000101"; -- E
            when x"2B" => return "000110"; -- F
            when x"34" => return "000111"; -- G
            when x"33" => return "001000"; -- H
            when x"43" => return "001001"; -- I
            when x"3B" => return "001010"; -- J
            when x"42" => return "001011"; -- K
            when x"4B" => return "001100"; -- L
            when x"3A" => return "001101"; -- M
            when x"31" => return "001110"; -- N
            when x"44" => return "001111"; -- O
            when x"4D" => return "010000"; -- P
            when x"15" => return "010001"; -- Q
            when x"2D" => return "010010"; -- R
            when x"1B" => return "010011"; -- S
            when x"2C" => return "010100"; -- T
            when x"3C" => return "010101"; -- U
            when x"2A" => return "010110"; -- V
            when x"1D" => return "010111"; -- W
            when x"22" => return "011000"; -- X
            when x"35" => return "011001"; -- Y
            when x"1A" => return "011010"; -- Z
            when x"29" => return BLANK_CHAR; -- Space
            when others => return "111110"; -- Unsupported
        end case;
    end function;

    signal pixel_clock  : std_logic;
    signal video_on     : std_logic;
    signal pixel_row    : std_logic_vector(9 downto 0);
    signal pixel_column : std_logic_vector(9 downto 0);
    signal red_bit      : std_logic;
    signal green_bit    : std_logic;
    signal blue_bit     : std_logic;
    signal red_out      : std_logic;
    signal green_out    : std_logic;
    signal blue_out     : std_logic;

    signal scan_code  : std_logic_vector(7 downto 0);
    signal scan_ready : std_logic;
    signal read_stb   : std_logic := '0';
    signal break_code : std_logic := '0';

    signal cursor_x : unsigned(6 downto 0) := to_unsigned(0, 7);
    signal cursor_y : unsigned(5 downto 0) := to_unsigned(0, 6);

    signal cell_x   : unsigned(6 downto 0);
    signal cell_y   : unsigned(5 downto 0);
    signal font_row : std_logic_vector(2 downto 0);
    signal font_col : std_logic_vector(2 downto 0);

    signal cursor_cell : std_logic;
    signal font_pixel  : std_logic;
    signal char_addr   : std_logic_vector(5 downto 0);
    signal text_mem    : text_mem_t := (others => BLANK_CHAR);
    signal display_idx : integer range 0 to MEM_SIZE - 1;
    signal write_idx   : integer range 0 to MEM_SIZE - 1;
    signal draw_pixel  : std_logic;
    signal invert_mode : std_logic;
    signal clear_active : std_logic := '0';
    signal clear_idx    : integer range 0 to MEM_SIZE - 1 := 0;

    attribute ramstyle : string;
    attribute ramstyle of text_mem : signal is "M4K, no_rw_check";
begin
    invert_mode <= SW(0);

    keyboard_inst : entity work.keyboard
        port map (
            keyboard_clk  => PS2_CLK,
            keyboard_data => PS2_DAT,
            clock_25Mhz   => pixel_clock,
            reset         => not KEY(0),
            read          => read_stb,
            scan_code     => scan_code,
            scan_ready    => scan_ready
        );

    vga_sync_inst : entity work.VGA_SYNC
        port map (
            clock_50Mhz     => CLOCK_50,
            red             => red_bit,
            green           => green_bit,
            blue            => blue_bit,
            red_out         => red_out,
            green_out       => green_out,
            blue_out        => blue_out,
            horiz_sync_out  => VGA_HS,
            vert_sync_out   => VGA_VS,
            video_on        => video_on,
            pixel_clock     => pixel_clock,
            pixel_row       => pixel_row,
            pixel_column    => pixel_column
        );

    char_rom_inst : entity work.char_rom
        port map (
            clock             => pixel_clock,
            character_address => char_addr,
            font_row          => font_row,
            font_col          => font_col,
            rom_mux_output    => font_pixel
        );

    process (pixel_clock)
        variable typed_char : std_logic_vector(5 downto 0);
        variable back_x     : unsigned(6 downto 0);
        variable back_y     : unsigned(5 downto 0);
        variable back_idx   : integer range 0 to MEM_SIZE - 1;
    begin
        if rising_edge(pixel_clock) then
            read_stb <= '0';
            if KEY(1) = '0' and clear_active = '0' then
                clear_active <= '1';
                clear_idx <= 0;
            end if;

            if clear_active = '1' then
                text_mem(clear_idx) <= BLANK_CHAR;
                if clear_idx = MEM_SIZE - 1 then
                    clear_active <= '0';
                    clear_idx <= 0;
                else
                    clear_idx <= clear_idx + 1;
                end if;
            elsif scan_ready = '1' then
                read_stb <= '1';
                if scan_code = x"F0" then
                    break_code <= '1';
                elsif break_code = '1' then
                    break_code <= '0';
                else
                    case scan_code is
                        when x"5A" => -- Enter
                            cursor_x <= to_unsigned(0, cursor_x'length);
                            if cursor_y < ROWS - 1 then
                                cursor_y <= cursor_y + 1;
                            end if;
                        when x"66" => -- Backspace
                            back_x := cursor_x;
                            back_y := cursor_y;
                            if cursor_x > 0 then
                                back_x := cursor_x - 1;
                            elsif cursor_y > 0 then
                                back_y := cursor_y - 1;
                                back_x := to_unsigned(COLS - 1, cursor_x'length);
                            end if;
                            back_idx := to_integer(back_y) * COLS + to_integer(back_x);
                            text_mem(back_idx) <= BLANK_CHAR;
                            cursor_x <= back_x;
                            cursor_y <= back_y;
                        when others =>
                            typed_char := ps2_to_char(scan_code);
                            -- Ignore pure modifier keys (Shift/Ctrl/Alt/Caps).
                            if scan_code /= x"12" and scan_code /= x"59" and
                               scan_code /= x"14" and scan_code /= x"11" and
                               scan_code /= x"58" and typed_char /= "111110" then
                                text_mem(write_idx) <= typed_char;
                                if cursor_x < COLS - 1 then
                                    cursor_x <= cursor_x + 1;
                                elsif cursor_y < ROWS - 1 then
                                    cursor_x <= to_unsigned(0, cursor_x'length);
                                    cursor_y <= cursor_y + 1;
                                end if;
                            end if;
                    end case;
                end if;
            end if;

            -- Synchronous read encourages BRAM inference (much lower LAB usage).
            char_addr <= text_mem(display_idx);
        end if;
    end process;

    cell_x   <= unsigned(pixel_column(9 downto 3));
    cell_y   <= unsigned(pixel_row(8 downto 3));
    font_row <= pixel_row(2 downto 0);
    font_col <= pixel_column(2 downto 0);
    write_idx <= to_integer(cursor_y) * COLS + to_integer(cursor_x);
    display_idx <= to_integer(cell_y) * COLS + to_integer(cell_x);

    cursor_cell <= '1' when (cell_x = cursor_x and cell_y = cursor_y) else '0';
    draw_pixel <= '0' when char_addr = BLANK_CHAR else font_pixel;

    process (draw_pixel, cursor_cell, invert_mode, SW, pixel_row, pixel_column)
        variable grid_line : std_logic;
        variable lit       : std_logic;
    begin
        if (pixel_row(2 downto 0) = "000") or (pixel_column(2 downto 0) = "000") then
            grid_line := '1';
        else
            grid_line := '0';
        end if;

        lit := (draw_pixel and (not grid_line)) or cursor_cell;
        if invert_mode = '1' then
            lit := not lit;
        end if;

        red_bit <= lit;
        green_bit <= lit;
        blue_bit <= lit;
    end process;

    VGA_R <= (others => red_out);
    VGA_G <= (others => green_out);
    VGA_B <= (others => blue_out);
    VGA_CLK <= pixel_clock;
    VGA_BLANK <= video_on;
    VGA_SYNC <= '0';

    LEDR(7 downto 0) <= scan_code;
    LEDR(8) <= scan_ready;
    LEDR(9) <= invert_mode;
    LEDR(16 downto 10) <= std_logic_vector(cursor_x);
    LEDR(17) <= cursor_y(0);
end architecture;
