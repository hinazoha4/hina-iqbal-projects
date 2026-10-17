library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;

entity CursorControl is
    Port (
        scan_code   : in  STD_LOGIC_VECTOR(7 downto 0);
        reset       : in  STD_LOGIC; 
        wren        : in  STD_LOGIC;
        col         : out STD_LOGIC_VECTOR(5 downto 0);
        row         : out STD_LOGIC_VECTOR(4 downto 0);
        backspace   : out STD_LOGIC; 
        arrow 		: out STD_LOGIC; 
        w_addr      : out STD_LOGIC_VECTOR(11 downto 0)
    );
end CursorControl;

architecture Behavioral of CursorControl is
    signal col_counter : unsigned(6 downto 0) := (others => '0');
    signal row_counter : unsigned(5 downto 0) := (others => '0');
    constant SCAN_CODE_ENTER     : STD_LOGIC_VECTOR(7 downto 0) := x"5A"; -- Enter
    constant SCAN_CODE_BACKSPACE : STD_LOGIC_VECTOR(7 downto 0) := x"66"; -- Backspace
    constant SCAN_CODE_L_ARROW     : STD_LOGIC_VECTOR(7 downto 0) := x"6B";  -- setas
    constant SCAN_CODE_R_ARROW : STD_LOGIC_VECTOR(7 downto 0) := x"74"; 
    constant SCAN_CODE_UP_ARROW     : STD_LOGIC_VECTOR(7 downto 0) := x"75"; 
    constant SCAN_CODE_DW_ARROW : STD_LOGIC_VECTOR(7 downto 0) := x"72"; 
    
begin
    Cursor: PROCESS(scan_code, wren, reset)

    begin
    
        if reset = '0' then
            col_counter <= (others => '0'); 
            row_counter <= (others => '0'); 
            backspace <= '0';
            arrow <= '0'; 
        elsif rising_edge(wren) then
            if wren = '1' then
                -- enter
                if scan_code = SCAN_CODE_ENTER then
                    row_counter <= row_counter + 1;
                    col_counter <= (others => '0');
                    backspace <= '1'; 
                    arrow <= '0'; 
                -- backspace
                elsif scan_code = SCAN_CODE_BACKSPACE then
                    
                    if col_counter /= 0 then
                        col_counter <= col_counter - 1;
                    elsif row_counter /= 0 then
                        row_counter <= row_counter - 1;
                        col_counter <= to_unsigned(39, col_counter'length);
                    end if;
                    backspace <= '1';
                    arrow <= '0'; 
                    
				elsif scan_code = SCAN_CODE_L_ARROW then 

                    if col_counter /= 0 then
                        col_counter <= col_counter - 1;
    
                    elsif row_counter /= 0 then
                        row_counter <= row_counter - 1;
                        col_counter <= to_unsigned(39, col_counter'length);
                    end if;
                    arrow <= '1';
                    
                elsif scan_code = SCAN_CODE_R_ARROW then 
                
					if col_counter = 39 then  
						col_counter <= (others => '0'); 
						row_counter <= row_counter + 1; 
					else 
						col_counter <= col_counter + 1; 
					end if; 
                    arrow <= '1';
                
				elsif scan_code = SCAN_CODE_UP_ARROW then 
					if row_counter = 0 then 
						row_counter <= to_unsigned(29, row_counter'length); 
					else 
						row_counter <= row_counter - 1; 
					end if; 
					arrow <= '1'; 
					
				elsif scan_code = SCAN_CODE_DW_ARROW then 

					if row_counter = 29 then 
						row_counter <= (others => '0'); 
					else 
						row_counter <= row_counter + 1; 
					end if; 
					arrow <= '1'; 	
					         
                -- resto
                else
                    if col_counter /= 39 then
                        col_counter <= col_counter + 1;
                    -- fim de linha
                    else
                        col_counter <= (others => '0');
                        if row_counter /= 29 then
                            row_counter <= row_counter + 1;
                        end if;
                    end if;
                    backspace <= '0';
                    arrow <= '0'; 
                end if;
            end if; 	
        end if;
      
        col <= std_logic_vector(col_counter(5 downto 0)); 
        row <= std_logic_vector(row_counter(4 downto 0)); 
        
        w_addr <= std_logic_vector((row_counter * 40) + col_counter); 
        
    end process; 
end Behavioral;
