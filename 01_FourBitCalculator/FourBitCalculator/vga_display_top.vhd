library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.STD_LOGIC_UNSIGNED.ALL;

entity vga_display_top is
  Port (
    clk_25MHz : in  std_logic;
    hsync     : out std_logic;
    vsync     : out std_logic;
    red       : out std_logic_vector(3 downto 0);
    green     : out std_logic_vector(3 downto 0);
    blue      : out std_logic_vector(3 downto 0)
  );
end vga_display_top;

architecture Behavioral of vga_display_top is

  -- VGA signals
  signal hsync_sig, vsync_sig, active : std_logic;
  signal pixel_x, pixel_y : std_logic_vector(9 downto 0);

  -- Character positioning
  signal char_row, char_col : integer range 0 to 59;
  signal char_index         : std_logic_vector(12 downto 0);
  signal char_code          : std_logic_vector(6 downto 0);
  signal row_index          : std_logic_vector(2 downto 0);
  signal row_pixels         : std_logic_vector(7 downto 0);
  signal pixel_col_in_char  : integer range 0 to 7;

begin

  -- VGA Timing Controller
  vga_ctrl : entity work.vga_controller
    port map (
      clk     => clk_25MHz,
      hsync   => hsync_sig,
      vsync   => vsync_sig,
      pixel_x => pixel_x,
      pixel_y => pixel_y,
      active  => active
    );

  -- Character Cell Calculation (8x8)
  char_col <= to_integer(unsigned(pixel_x(9 downto 3))); -- x / 8
  char_row <= to_integer(unsigned(pixel_y(9 downto 3))); -- y / 8

  char_index <= std_logic_vector(to_unsigned((char_row * 80 + char_col), 13));
  row_index  <= pixel_y(2 downto 0);  -- Which row inside the 8x8 char

  -- Screen RAM
  screen_buffer : entity work.screen_ram
    port map (
      clk      => clk_25MHz,
      wr_en    => '0',                     -- no writes in this example
      wr_addr  => (others => '0'),
      wr_data  => (others => '0'),
      rd_addr  => char_index,
      rd_data  => char_code
    );

  -- Character Generator
  font_rom : entity work.vga_font_rom
    port map (
      char_code  => char_code,
      row_index  => row_index,
      row_pixels => row_pixels
    );

  -- Pixel bit within row
  pixel_col_in_char <= to_integer(unsigned(pixel_x(2 downto 0)));

  -- Output color: white pixel if corresponding font bit is set
  process(clk_25MHz)
  begin
    if rising_edge(clk_25MHz) then
      hsync <= hsync_sig;
      vsync <= vsync_sig;

      if active = '1' and row_pixels(7 - pixel_col_in_char) = '1' then
        red   <= "1111";
        green <= "1111";
        blue  <= "1111";
      else
        red   <= (others => '0');
        green <= (others => '0');
        blue  <= (others => '0');
      end if;
    end if;
  end process;
end Behavioral;