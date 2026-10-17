library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;

entity ReadAddress is
    Port (
        px_col    : in  STD_LOGIC_VECTOR(9 downto 4);
        px_row    : in  STD_LOGIC_VECTOR(9 downto 4);
        read_addr : out STD_LOGIC_VECTOR(11 downto 0)
    );
end ReadAddress;

architecture Behavioral of ReadAddress is
begin
    Cursor: PROCESS(px_col, px_row)
        variable temp_address : INTEGER;
        variable row: integer; 
        variable column: integer; 
    begin
        -- converter a inteiro
        row := to_integer(unsigned(px_row(9 downto 4)));  
        column := to_integer(unsigned(px_col(9 downto 4)));  

        -- calculo do endereço de leitura
        temp_address := row * 40 + column;
        -- converter a vetor
        read_addr <= std_logic_vector(to_unsigned(temp_address, read_addr'length)); 
        
    end process;
end Behavioral;