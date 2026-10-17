library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;

entity pixel_canvas is
    generic (
        WIDTH_CELLS  : integer := 80;
        HEIGHT_CELLS : integer := 60
    );
    port (
        clk        : in  std_logic;
        clear      : in  std_logic;
        write_en   : in  std_logic;
        write_x    : in  unsigned(6 downto 0);
        write_y    : in  unsigned(5 downto 0);
        write_rgb  : in  std_logic_vector(2 downto 0);
        read_x     : in  unsigned(6 downto 0);
        read_y     : in  unsigned(5 downto 0);
        read_rgb   : out std_logic_vector(2 downto 0);
        busy_clear : out std_logic
    );
end entity;

architecture rtl of pixel_canvas is
    constant MEM_SIZE : integer := WIDTH_CELLS * HEIGHT_CELLS;
    type canvas_mem_t is array (0 to MEM_SIZE - 1) of std_logic_vector(2 downto 0);
    signal mem : canvas_mem_t := (others => "000");

    signal clear_active : std_logic := '0';
    signal clear_idx    : integer range 0 to MEM_SIZE - 1 := 0;
    signal read_idx     : integer range 0 to MEM_SIZE - 1;
    signal write_idx    : integer range 0 to MEM_SIZE - 1;
begin
    read_idx <= to_integer(read_y) * WIDTH_CELLS + to_integer(read_x);
    write_idx <= to_integer(write_y) * WIDTH_CELLS + to_integer(write_x);

    process (clk)
    begin
        if rising_edge(clk) then
            if clear = '1' and clear_active = '0' then
                clear_active <= '1';
                clear_idx <= 0;
            end if;

            if clear_active = '1' then
                mem(clear_idx) <= "000";
                if clear_idx = MEM_SIZE - 1 then
                    clear_active <= '0';
                    clear_idx <= 0;
                else
                    clear_idx <= clear_idx + 1;
                end if;
            elsif write_en = '1' then
                mem(write_idx) <= write_rgb;
            end if;

            read_rgb <= mem(read_idx);
        end if;
    end process;

    busy_clear <= clear_active;
end architecture;
