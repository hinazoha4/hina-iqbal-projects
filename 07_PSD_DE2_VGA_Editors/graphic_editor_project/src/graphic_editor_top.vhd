library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;

entity graphic_editor_top is
    port (
        CLOCK_50  : in    std_logic;
        KEY       : in    std_logic_vector(3 downto 0);
        SW        : in    std_logic_vector(17 downto 0);
        LEDR      : out   std_logic_vector(17 downto 0);
        PS2_CLK   : inout std_logic;
        PS2_DAT   : inout std_logic;
        VGA_R     : out   std_logic_vector(9 downto 0);
        VGA_G     : out   std_logic_vector(9 downto 0);
        VGA_B     : out   std_logic_vector(9 downto 0);
        VGA_HS    : out   std_logic;
        VGA_VS    : out   std_logic;
        VGA_CLK   : out   std_logic;
        VGA_BLANK : out   std_logic;
        VGA_SYNC  : out   std_logic
    );
end entity;

architecture rtl of graphic_editor_top is
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

    signal left_button     : std_logic;
    signal right_button    : std_logic;
    signal mouse_row       : std_logic_vector(9 downto 0);
    signal mouse_column    : std_logic_vector(9 downto 0);
    signal cursor_x        : unsigned(6 downto 0);
    signal cursor_y        : unsigned(5 downto 0);
    signal pixel_cell_x    : unsigned(6 downto 0);
    signal pixel_cell_y    : unsigned(5 downto 0);
    signal canvas_rgb      : std_logic_vector(2 downto 0);
    signal brush_rgb       : std_logic_vector(2 downto 0);
    signal draw_enable     : std_logic;
    signal clear_canvas    : std_logic;
    signal clear_busy      : std_logic;
    signal cursor_overlay  : std_logic;
begin
    mouse_inst : entity work.MOUSE
        port map (
            clock_25Mhz         => pixel_clock,
            reset               => not KEY(0),
            mouse_data          => PS2_DAT,
            mouse_clk           => PS2_CLK,
            left_button         => left_button,
            right_button        => right_button,
            mouse_cursor_row    => mouse_row,
            mouse_cursor_column => mouse_column
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

    canvas_inst : entity work.pixel_canvas
        port map (
            clk        => pixel_clock,
            clear      => clear_canvas,
            write_en   => draw_enable,
            write_x    => cursor_x,
            write_y    => cursor_y,
            write_rgb  => brush_rgb,
            read_x     => pixel_cell_x,
            read_y     => pixel_cell_y,
            read_rgb   => canvas_rgb,
            busy_clear => clear_busy
        );

    cursor_x <= unsigned(mouse_column(9 downto 3));
    cursor_y <= unsigned(mouse_row(8 downto 3));
    pixel_cell_x <= unsigned(pixel_column(9 downto 3));
    pixel_cell_y <= unsigned(pixel_row(8 downto 3));
    brush_rgb <= SW(3 downto 1);

    draw_enable <= left_button and SW(0) and not clear_busy;
    clear_canvas <= not KEY(1);

    cursor_overlay <= '1' when (unsigned(pixel_column) = unsigned(mouse_column) or unsigned(pixel_row) = unsigned(mouse_row)) else '0';

    red_bit <= (canvas_rgb(2) and video_on) or cursor_overlay;
    green_bit <= (canvas_rgb(1) and video_on) or (cursor_overlay and SW(4));
    blue_bit <= (canvas_rgb(0) and video_on) or (cursor_overlay and not SW(4));

    VGA_R <= (others => red_out);
    VGA_G <= (others => green_out);
    VGA_B <= (others => blue_out);
    VGA_CLK <= pixel_clock;
    VGA_BLANK <= video_on;
    VGA_SYNC <= '0';

    LEDR(0) <= left_button;
    LEDR(1) <= right_button;
    LEDR(2) <= SW(0);
    LEDR(3) <= clear_busy;
    LEDR(6 downto 4) <= brush_rgb;
    LEDR(13 downto 7) <= std_logic_vector(cursor_x);
    LEDR(17 downto 14) <= std_logic_vector(cursor_y(5 downto 2));
end architecture;
