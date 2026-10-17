library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;


entity Vertical_RGB_Pattern is
    Port (
        clock_50MHz : in STD_LOGIC;
        pixel_clock : in STD_LOGIC;
        pattern_select : in STD_LOGIC_VECTOR(1 downto 0);
        pixel_row : in STD_LOGIC_VECTOR(9 downto 0);
        pixel_column : in STD_LOGIC_VECTOR(9 downto 0);
        red_out : out STD_LOGIC_VECTOR(9 downto 0);
        green_out : out STD_LOGIC_VECTOR(9 downto 0);
        blue_out : out STD_LOGIC_VECTOR(9 downto 0)
    );
end Vertical_RGB_Pattern;

architecture Behavioral of Vertical_RGB_Pattern is

begin

    -- Registered RGB mux: pattern_select chooses one of several test patterns
    process(pixel_clock, pattern_select, pixel_row, pixel_column)
        variable v_red : STD_LOGIC_VECTOR(9 downto 0);
        variable v_green : STD_LOGIC_VECTOR(9 downto 0);
        variable v_blue : STD_LOGIC_VECTOR(9 downto 0);
    begin
        if rising_edge(pixel_clock) then
            case pattern_select is
                when "00" =>
                    -- Eight horizontal color bands vs pixel_row
                    -- Red
                    if unsigned(pixel_row) < 80 then
                        v_red := (others => '1');
                        v_green := (others => '0');
                        v_blue := (others => '0');
                    -- Green
                    elsif unsigned(pixel_row) < 160 then
                        v_red := (others => '0');
                        v_green := (others => '1');
                        v_blue := (others => '0');
                    -- Blue
                    elsif unsigned(pixel_row) < 240 then
                        v_red := (others => '0');
                        v_green := (others => '0');
                        v_blue := (others => '1');
                    -- Yellow
                    elsif unsigned(pixel_row) < 320 then
                        v_red := (others => '1');
                        v_green := (others => '1');
                        v_blue := (others => '0');
                    -- Cyan
                    elsif unsigned(pixel_row) < 400 then
                        v_red := (others => '0');
                        v_green := (others => '1');
                        v_blue := (others => '1');
                    -- Magenta
                    elsif unsigned(pixel_row) < 480 then
                        v_red := (others => '1');
                        v_green := (others => '0');
                        v_blue := (others => '1');
                    -- White
                    elsif unsigned(pixel_row) < 560 then
                        v_red := (others => '1');
                        v_green := (others => '1');
                        v_blue := (others => '1');
                    -- Black
                    else
                        v_red := (others => '0');
                        v_green := (others => '0');
                        v_blue := (others => '0');
                    end if;
                    
				when "01" =>
					-- Color checkerboard vs row/column blocks
					if ((unsigned(pixel_column) / 80) mod 2 = 0 and (unsigned(pixel_row) / 60) mod 2 = 0) or
					   ((unsigned(pixel_column) / 80) mod 2 = 1 and (unsigned(pixel_row) / 60) mod 2 = 1) then
						if (unsigned(pixel_column) mod 80 < 40) then
							v_red := (others => '1');
							v_green := (others => '0');
							v_blue := (others => '0');
						else
							v_red := (others => '0');
							v_green := (others => '1');
							v_blue := (others => '0');
						end if;
					else
						if (unsigned(pixel_column) mod 80 < 40) then
							v_red := (others => '0');
							v_green := (others => '0');
							v_blue := (others => '1');
						else
							v_red := (others => '1');
							v_green := (others => '1');
							v_blue := (others => '0');
						end if;
					end if;

				when "10" =>
					-- Thin diagonal line (column tracks row)
					if (unsigned(pixel_column) = (3 * unsigned(pixel_row)) / 4) then 
						v_red := (others => '1');
						v_green := (others => '1');
						v_blue := (others => '1'); 
					else
						v_red := (others => '0');
						v_green := (others => '0');
						v_blue := (others => '0');
					end if;

                when others =>
                    -- Off / default
                    v_red := (others => '0');
                    v_green := (others => '0');
                    v_blue := (others => '0');
            end case;
            
            -- Drive outputs
            red_out <= v_red;
            green_out <= v_green;
            blue_out <= v_blue;
        end if;
    end process;

end Behavioral;
