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

    signal cursor_x : unsigned(6 downto 0) := to_unsigned(40, 7);
    signal cursor_y : unsigned(5 downto 0) := to_unsigned(30, 6);
    signal char_sel : std_logic_vector(5 downto 0) := "000001";

    signal cell_x   : unsigned(6 downto 0);
    signal cell_y   : unsigned(5 downto 0);
    signal font_row : std_logic_vector(2 downto 0);
    signal font_col : std_logic_vector(2 downto 0);

    signal cursor_cell : std_logic;
    signal font_pixel  : std_logic;
    signal char_addr   : std_logic_vector(5 downto 0);
    signal invert_mode : std_logic;
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
    begin
        if rising_edge(pixel_clock) then
            read_stb <= '0';
            if scan_ready = '1' then
                read_stb <= '1';
                if scan_code = x"F0" then
                    break_code <= '1';
                elsif break_code = '1' then
                    break_code <= '0';
                else
                    case scan_code is
                        when x"1D" => -- W
                            if cursor_y > 0 then
                                cursor_y <= cursor_y - 1;
                            end if;
                        when x"1B" => -- S
                            if cursor_y < 59 then
                                cursor_y <= cursor_y + 1;
                            end if;
                        when x"1C" => -- A
                            if cursor_x > 0 then
                                cursor_x <= cursor_x - 1;
                            end if;
                        when x"23" => -- D
                            if cursor_x < 79 then
                                cursor_x <= cursor_x + 1;
                            end if;
                        when x"29" => -- Space
                            char_sel <= "000000";
                        when others =>
                            char_sel <= scan_code(5 downto 0);
                    end case;
                end if;
            end if;
        end if;
    end process;

    cell_x   <= unsigned(pixel_column(9 downto 3));
    cell_y   <= unsigned(pixel_row(8 downto 3));
    font_row <= pixel_row(2 downto 0);
    font_col <= pixel_column(2 downto 0);

    cursor_cell <= '1' when (cell_x = cursor_x and cell_y = cursor_y) else '0';
    char_addr <= std_logic_vector(unsigned(char_sel) xor ("00" & cell_x(3 downto 0)));

    process (font_pixel, cursor_cell, invert_mode, SW, pixel_row, pixel_column)
        variable grid_line : std_logic;
        variable lit       : std_logic;
    begin
        if (pixel_row(2 downto 0) = "000") or (pixel_column(2 downto 0) = "000") then
            grid_line := '1';
        else
            grid_line := '0';
        end if;

        lit := (font_pixel and (not grid_line)) or cursor_cell;
        if invert_mode = '1' then
            lit := not lit;
        end if;

        red_bit <= lit;
        green_bit <= lit xor SW(1);
        blue_bit <= lit xor SW(2);
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
