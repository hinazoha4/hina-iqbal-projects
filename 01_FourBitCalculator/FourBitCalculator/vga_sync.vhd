library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;  -- This line is essential for 'unsigned'

entity vga_sync is
    port (
        clk         : in  std_logic;
        reset       : in  std_logic;
        hsync       : out std_logic;
        vsync       : out std_logic;
        video_on    : out std_logic;
        pixel_x     : out unsigned(9 downto 0);
        pixel_y     : out unsigned(9 downto 0)
    );
end vga_sync;

architecture behavioral of vga_sync is
    -- VGA 640x480 @ 60Hz timing constants
    constant H_DISPLAY   : integer := 640;
    constant H_FRONT     : integer := 16;
    constant H_SYNC      : integer := 96;
    constant H_BACK      : integer := 48;
    constant H_TOTAL     : integer := H_DISPLAY + H_FRONT + H_SYNC + H_BACK;

    constant V_DISPLAY   : integer := 480;
    constant V_FRONT     : integer := 10;
    constant V_SYNC      : integer := 2;
    constant V_BACK      : integer := 33;
    constant V_TOTAL     : integer := V_DISPLAY + V_FRONT + V_SYNC + V_BACK;

    signal h_count : unsigned(9 downto 0) := (others => '0');
    signal v_count : unsigned(9 downto 0) := (others => '0');
begin

    process(clk, reset)
    begin
        if reset = '1' then
            h_count <= (others => '0');
            v_count <= (others => '0');
        elsif rising_edge(clk) then
            if h_count = to_unsigned(H_TOTAL-1, h_count'length) then
                h_count <= (others => '0');
                if v_count = to_unsigned(V_TOTAL-1, v_count'length) then
                    v_count <= (others => '0');
                else
                    v_count <= v_count + 1;
                end if;
            else
                h_count <= h_count + 1;
            end if;
        end if;
    end process;

    -- Output assignments
    hsync <= '0' when (h_count >= to_unsigned(H_DISPLAY+H_FRONT, h_count'length) and
                       h_count <  to_unsigned(H_DISPLAY+H_FRONT+H_SYNC, h_count'length))
             else '1';

    vsync <= '0' when (v_count >= to_unsigned(V_DISPLAY+V_FRONT, v_count'length) and
                       v_count <  to_unsigned(V_DISPLAY+V_FRONT+V_SYNC, v_count'length))
             else '1';

    video_on <= '1' when (h_count < to_unsigned(H_DISPLAY, h_count'length) and
                          v_count < to_unsigned(V_DISPLAY, v_count'length))
                else '0';

    pixel_x <= h_count;
    pixel_y <= v_count;

end behavioral;
