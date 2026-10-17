library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL; 

ENTITY PAINT_CONTROL IS 
    PORT(   
        px_col: IN STD_LOGIC_VECTOR(7 DOWNTO 0); 
        px_row: IN STD_LOGIC_VECTOR(7 DOWNTO 0); 
        px_col_mouse: IN STD_LOGIC_VECTOR(7 DOWNTO 0); 
        px_row_mouse: IN STD_LOGIC_VECTOR(7 DOWNTO 0); 
        paint_colour : IN STD_LOGIC_VECTOR(2 DOWNTO 0); 
        clear : IN STD_LOGIC; 
        left_b : IN STD_LOGIC; 
        right_b : IN STD_LOGIC; 
        red : OUT STD_LOGIC; 
        green : OUT STD_LOGIC; 
        blue : OUT STD_LOGIC; 
        cursor : OUT STD_LOGIC
    );
END PAINT_CONTROL; 

ARCHITECTURE Behavior OF PAINT_CONTROL IS 
BEGIN 
    PROCESS( 
        px_col, 
        px_row, 
        px_col_mouse, 
        px_row_mouse, 
        left_b, 
        right_b, 
        paint_colour, 
        clear)
        
     variable px_col_int : integer; 
     variable px_row_int : integer; 
     variable px_col_mouse_int : integer; 
     variable px_row_mouse_int : integer; 
    
    BEGIN 
    
    px_col_int := TO_INTEGER(unsigned(px_col)); 
    px_row_int := TO_INTEGER(unsigned(px_row)); 
    px_col_mouse_int := TO_INTEGER(unsigned(px_col_mouse)); 
    px_row_mouse_int := TO_INTEGER(unsigned(px_row_mouse)); 
    
    if(left_b = '1') then 
		if((px_col_int = px_col_mouse_int) AND (px_row_int = px_row_mouse_int)) then
			red <= paint_colour(2); 
			green <= paint_colour(1); 
			blue <= paint_colour(0); 
			cursor <= '1'; 
		end if; 
	elsif(right_b = '1') then 
		if((px_col_int = px_col_mouse_int) AND (px_row_int = px_row_mouse_int)) then
			red <= '0'; 
			green <= '0'; 
			blue <= '0'; 
			cursor <= '1'; 
		end if; 
	else 
		if((px_col_int = px_col_mouse_int) AND (px_row_int = px_row_mouse_int)) then
			red <= paint_colour(2); 
			green <= paint_colour(1); 
			blue <= paint_colour(0); 
			cursor <= '1'; 
		end if; 
		
	end if;  
     
    END PROCESS; 
END Behavior;
