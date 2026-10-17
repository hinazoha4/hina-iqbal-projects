library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

entity reg4bit is
  Port (
    clk     : in  std_logic;
    reset   : in  std_logic;
    load    : in  std_logic;
    data_in : in  std_logic_vector(3 downto 0);
    data_out: out std_logic_vector(3 downto 0)
  );
end reg4bit;

architecture Behavioral of reg4bit is
  signal reg : std_logic_vector(3 downto 0) := (others => '0');
begin
  process(clk, reset)
  begin
    if reset = '1' then
      reg <= (others => '0');
    elsif rising_edge(clk) then
      if load = '1' then
        reg <= data_in;
      end if;
    end if;
  end process;

  data_out <= reg;
end Behavioral;