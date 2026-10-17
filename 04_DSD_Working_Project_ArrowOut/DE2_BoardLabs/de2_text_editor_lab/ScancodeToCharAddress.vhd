library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.STD_LOGIC_ARITH.ALL;
use IEEE.STD_LOGIC_UNSIGNED.ALL;

entity ScancodeToCharAddress is
    Port (
        scan_code   : in  STD_LOGIC_VECTOR (7 downto 0); -- 8 bits for scancode
        char_address   : out STD_LOGIC_VECTOR (5 downto 0)   -- 6 bits for CHAR_ROM address
    );
end ScancodeToCharAddress;

architecture Behavioral of ScancodeToCharAddress is
begin
        char_address <= "000001" when (scan_code = x"1C" ) else -- A 
				"000010" when (scan_code = x"32" ) else 
				"000011" when (scan_code = x"21" ) else 
				"000100" when (scan_code = x"23" ) else 
				"000101" when (scan_code = x"24" ) else 
				"000110" when (scan_code = x"2B" ) else 
				"000111" when (scan_code = x"34" ) else 
				"001000" when (scan_code = x"33" ) else 
				"001001" when (scan_code = x"43" ) else 
				"001010" when (scan_code = x"3B" ) else 
				"001011" when (scan_code = x"42" ) else 
				"001100" when (scan_code = x"4B" ) else 
				"001101" when (scan_code = x"3A" ) else 
				"001110" when (scan_code = x"31" ) else 
				"001111" when (scan_code = x"44" ) else 
				"010000" when (scan_code = x"4D" ) else 
				"010001" when (scan_code = x"15" ) else 
				"010010" when (scan_code = x"2D" ) else 
				"010011" when (scan_code = x"1B" ) else 
				"010100" when (scan_code = x"2C" ) else 
				"010101" when (scan_code = x"3C" ) else 
				"010110" when (scan_code = x"2A" ) else 
				"010111" when (scan_code = x"1D" ) else 
				"011000" when (scan_code = x"22" ) else 
				"011001" when (scan_code = x"35" ) else 
				"011010" when (scan_code = x"1A" ) else -- Z
				"110000" when (scan_code = x"45" ) else -- 0
				"110001" when (scan_code = x"16" ) else 
				"110010" when (scan_code = x"1E" ) else 
				"110011" when (scan_code = x"26" ) else 
				"110100" when (scan_code = x"25" ) else 
				"110101" when (scan_code = x"2E" ) else 
				"110110" when (scan_code = x"36" ) else 
				"110111" when (scan_code = x"3D" ) else 
				"111000" when (scan_code = x"3E" ) else 
				"111001" when (scan_code = x"46" ) else -- 9
				"100111" when (scan_code = x"4E" ) else -- '
				"100000" when (scan_code = x"29" ) else -- space
				"011011" when (scan_code = x"52" ) else -- (
				"011101" when (scan_code = x"5D" ) else -- )
				"101100" when (scan_code = x"41" ) else -- ,
				"101110" when (scan_code = x"49" ) else -- .
				"101101" when (scan_code = x"4A" ) else -- -
				"101111" when (scan_code = x"55" ) else -- /
				"101011" when (scan_code = x"54" ) else -- +
				"100111" when (scan_code = x"5B" ) else -- ,
				"000000";
end Behavioral;
