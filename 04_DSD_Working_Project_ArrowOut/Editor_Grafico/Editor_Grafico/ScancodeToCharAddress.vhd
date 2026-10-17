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
        char_address <= "000001" when (scan_code = x"1C") else -- A
                      "000010" when (scan_code = x"32") else -- B
                      "000011" when (scan_code = x"21") else -- C
                      "000100" when (scan_code = x"23") else -- D
                      "000101" when (scan_code = x"24") else -- E
                      "000110" when (scan_code = x"2B") else -- F
                      "000111" when (scan_code = x"34") else -- G
                      "001000" when (scan_code = x"33") else -- H
                      "001001" when (scan_code = x"43") else -- I
                      "001010" when (scan_code = x"3B") else -- J
                      "001011" when (scan_code = x"42") else -- K
                      "001100" when (scan_code = x"4B") else -- L
                      "001101" when (scan_code = x"3A") else -- M
                      "001110" when (scan_code = x"31") else -- N
                      "001111" when (scan_code = x"44") else -- O
                      "010000" when (scan_code = x"4D") else -- P
                      "010001" when (scan_code = x"15") else -- Q
                      "010010" when (scan_code = x"2D") else -- R
                      "010011" when (scan_code = x"1B") else -- S
                      "010100" when (scan_code = x"2C") else -- T
                      "010101" when (scan_code = x"3C") else -- U
                      "010110" when (scan_code = x"2A") else -- V
                      "010111" when (scan_code = x"1D") else -- W
                      "011000" when (scan_code = x"22") else -- X
                      "011001" when (scan_code = x"35") else -- Y
                      "011010" when (scan_code = x"1A") else -- Z
                      "110000" when (scan_code = x"45") else -- 0
                      "110001" when (scan_code = x"16") else -- 1
                      "110010" when (scan_code = x"1E") else -- 2
                      "110011" when (scan_code = x"26") else -- 3
                      "110100" when (scan_code = x"25") else -- 4
                      "110101" when (scan_code = x"2E") else -- 5
                      "110110" when (scan_code = x"36") else -- 6
                      "110111" when (scan_code = x"3D") else -- 7
                      "111000" when (scan_code = x"3E") else -- 8
                      "111001" when (scan_code = x"46") else -- 9
                      "100111" when (scan_code = x"4E") else -- '
                      "100000" when (scan_code = x"29") else -- space
                      "011011" when (scan_code = x"52") else -- (
                      "011101" when (scan_code = x"5D") else -- )
                      "101100" when (scan_code = x"41") else -- ,
                      "101110" when (scan_code = x"49") else -- .
                      "101101" when (scan_code = x"4A") else -- -
                      "101111" when (scan_code = x"55") else -- /
                      "101011" when (scan_code = x"54") else -- +
                      "100111" when (scan_code = x"5B") else -- ,
                      "000000"; -- Default for unknown scancode
end Behavioral;
