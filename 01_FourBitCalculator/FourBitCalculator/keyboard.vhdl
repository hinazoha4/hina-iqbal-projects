library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.STD_LOGIC_UNSIGNED.ALL;

entity ps2_keyboard is
  Port (
    clk       : in  std_logic;
    ps2_clk   : in  std_logic;
    ps2_data  : in  std_logic;
    keycode   : out std_logic_vector(7 downto 0);
    key_ready : out std_logic
  );
end ps2_keyboard;

architecture Behavioral of ps2_keyboard is
  signal ps2_clk_prev : std_logic := '1';
  signal bit_count    : integer range 0 to 10 := 0;
  signal data_buffer  : std_logic_vector(7 downto 0) := (others => '0');
  signal shift_reg    : std_logic_vector(10 downto 0);
begin
  process(clk)
  begin
    if rising_edge(clk) then
      if ps2_clk_prev = '1' and ps2_clk = '0' then  -- Falling edge
        shift_reg <= ps2_data & shift_reg(10 downto 1);
        bit_count <= bit_count + 1;

        if bit_count = 10 then  -- Full frame received
          keycode   <= shift_reg(8 downto 1);
          key_ready <= '1';
          bit_count <= 0;
        else
          key_ready <= '0';
        end if;
      end if;
      ps2_clk_prev <= ps2_clk;
    end if;
  end process;
end Behavioral;