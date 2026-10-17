library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.STD_LOGIC_UNSIGNED.ALL;

entity vga_controller is
  Port (
    clk     : in  std_logic;                       -- 25 MHz clock input
    hsync   : out std_logic;                       -- Horizontal sync
    vsync   : out std_logic;                       -- Vertical sync
    pixel_x : out std_logic_vector(9 downto 0);    -- X coordinate (0–799)
    pixel_y : out std_logic_vector(9 downto 0);    -- Y coordinate (0–524)
    active  : out std_logic                        -- High when inside visible area (640x480)
  );
end vga_controller;

architecture Behavioral of vga_controller is

  signal h_count : std_logic_vector(9 downto 0) := (others => '0');
  signal v_count : std_logic_vector(9 downto 0) := (others => '0');

begin

  process(clk)
  begin
    if rising_edge(clk) then
      -- Horizontal counter
      if h_count = 799 then
        h_count <= (others => '0');
        -- Vertical counter
        if v_count = 524 then
          v_count <= (others => '0');
        else
          v_count <= v_count + 1;
        end if;
      else
        h_count <= h_count + 1;
      end if;
    end if;
  end process;

  -- Horizontal sync pulse (pulse from 656 to 751)
  hsync <= not (h_count >= 656 and h_count < 752);

  -- Vertical sync pulse (pulse from 490 to 491)
  vsync <= not (v_count >= 490 and v_count < 492);

  -- Output current pixel positions
  pixel_x <= h_count;
  pixel_y <= v_count;

  -- Signal high only in active display region (640 x 480)
  active <= '1' when (h_count < 640 and v_count < 480) else '0';

end Behavioral;