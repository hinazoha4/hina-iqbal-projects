library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;

ENTITY Cursor IS
    PORT(
        memory_rgb : IN STD_LOGIC_VECTOR(2 DOWNTO 0); 
        px_col : IN STD_LOGIC_VECTOR(7 DOWNTO 0); 
        px_row : IN STD_LOGIC_VECTOR(7 DOWNTO 0); 
        px_col_mouse : IN STD_LOGIC_VECTOR(7 DOWNTO 0); 
        px_row_mouse : IN STD_LOGIC_VECTOR(7 DOWNTO 0); 
        vga_red : OUT STD_LOGIC;
        vga_green : OUT STD_LOGIC;
        vga_blue : OUT STD_LOGIC
    );
END ENTITY Cursor;

ARCHITECTURE Behavior OF Cursor IS
BEGIN
    PROCESS(memory_rgb, px_col, px_row, px_col_mouse, px_row_mouse)
    BEGIN
        
        vga_red <= memory_rgb(0);
        vga_green <= memory_rgb(1);
        vga_blue <= memory_rgb(2);
        
        IF (px_col = px_col_mouse) AND (px_row = px_row_mouse) THEN           
            vga_red <= '1';
            vga_green <= '1';
            vga_blue <= '1';
        ELSE
            vga_red <= memory_rgb(0);
            vga_green <= memory_rgb(1);
            vga_blue <= memory_rgb(2);
        END IF;
    END PROCESS;
        
END ARCHITECTURE Behavior;
