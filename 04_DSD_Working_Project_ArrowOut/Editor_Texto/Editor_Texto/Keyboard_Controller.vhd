library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

entity Keyboard_Controller is
    Port (
        scan_ready  : in STD_LOGIC;
        scan_code   : in STD_LOGIC_VECTOR(7 downto 0);
        wren        : out STD_LOGIC;
        read        : out STD_LOGIC;
        state           : in STD_LOGIC_VECTOR(2 downto 0); -- Estado atual
        next_state           : out STD_LOGIC_VECTOR(2 downto 0) -- Próximo estado
    );
end Keyboard_Controller;

architecture Behavioral of Keyboard_Controller is
    -- Sinais para os break codes
    signal break_code_F0: std_logic;
	signal break_code_E0: std_logic;

begin

    -- Mapear os break codes
    break_code_F0 <= '1' when (scan_code = "11110000") else  -- 0xF0
                  '0';
    break_code_E0 <= '1' when (scan_code = "11100000") else -- 0xE0
				   '0';

    -- Transição de estados baseada em sinais de entrada
    next_state <= "000" when (state = "000" and scan_ready = '0') else
		 "000" when (state = "010") else
		 "000" when (state = "100") else
		 "001" when (state = "000" and scan_ready = '1') else
		 "010" when (state = "001" and break_code_F0 = '0' and break_code_E0 = '0') else
		 "011" when (state = "001" and (break_code_F0 = '1' or break_code_E0 = '1')) else
		 "011" when (state = "011" and (break_code_F0 = '1' or break_code_E0 = '1')) else
		 "100" when (state = "011" and break_code_F0 = '0' and break_code_E0 = '0') else
		 "000";

    -- Lógica das saidas
    wren <= '1' when (state = "010") else
			'0';
	
	read <= '1' when (state = "010") else
			'1' when (state = "100") else
			'0';

end Behavioral;
