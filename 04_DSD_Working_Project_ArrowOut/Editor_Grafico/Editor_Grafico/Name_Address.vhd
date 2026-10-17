library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;

ENTITY Name_Address IS
    PORT(   
        px_row: IN STD_LOGIC_VECTOR(9 DOWNTO 0); 
        px_col: IN STD_LOGIC_VECTOR(9 DOWNTO 0); 
        character_address: OUT STD_LOGIC_VECTOR(5 DOWNTO 0) -- Assuming this is the output for the character address
    );
END Name_Address;

ARCHITECTURE Behavior OF Name_Address IS
BEGIN
    PROCESS (px_row, px_col) 
    variable px_row_int : integer; 
    variable px_col_int : integer; 
    BEGIN
		px_row_int := TO_INTEGER(unsigned(px_row)); 
		px_col_int := TO_INTEGER(unsigned(px_col)); 
		
        if ((px_col_int >= 240) AND (px_col_int <= 247)) then          
			case px_row_int is
				when 240 to 247 =>
					character_address <= O"14"; -- 'L'
				when 248 to 255 =>
					character_address <= O"05"; -- 'E'
				when 256 to 263 =>
					character_address <= O"17"; -- 'O'
				when 264 to 271 =>
					character_address <= O"16"; -- 'N'
				when 272 to 279 =>
					character_address <= O"01"; -- 'A'
				when 280 to 287 =>
					character_address <= O"22"; -- 'R'
				when 288 to 295 =>
					character_address <= O"04"; -- 'D'
				when 296 to 303 =>
					character_address <= O"17"; -- 'O'
				when 304 to 311 =>
					character_address <= O"40"; -- ' '
				when 312 to 319 =>
					character_address <= O"07"; -- 'G'
				when 320 to 327 =>
					character_address <= O"17"; -- 'O'
				when 328 to 335 =>
					character_address <= O"16"; -- 'N'
				when 336 to 343 =>
					character_address <= O"03"; -- 'C'
				when 344 to 351 =>
					character_address <= O"01"; -- 'A'
				when 352 to 359 =>
					character_address <= O"14"; -- 'L'
				when 360 to 367 =>
					character_address <= O"26"; -- 'V'
				when 368 to 375 =>
					character_address <= O"05"; -- 'E'
				when 376 to 383 =>
					character_address <= O"23"; -- 'S'
				when others =>
					character_address <= O"40"; -- default value
			end case;
        else 
            character_address <= O"40";
        end if; 

    END PROCESS;

END Behavior;
