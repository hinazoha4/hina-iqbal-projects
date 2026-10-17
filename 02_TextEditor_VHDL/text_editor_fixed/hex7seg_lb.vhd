-- 4 bit to 7 seg hex ditigit with low brightness
-- for use on remote boards during covid
-- jlobo feb 2021

LIBRARY IEEE;
USE IEEE.STD_LOGIC_1164.all;
USE  IEEE.STD_LOGIC_ARITH.all;
USE  IEEE.STD_LOGIC_UNSIGNED.all;

-- Hexadecimal to 7 Segment Decoder for LED Display

ENTITY hex7seg_lb IS
	
	PORT( hex_digit	: IN	STD_LOGIC_VECTOR(3 DOWNTO 0);
	      CLOCK_50	: in	std_logic;
	      HEX0		: OUT   STD_LOGIC_VECTOR(6 downto 0) );

END hex7seg_lb;

ARCHITECTURE a OF hex7seg_lb IS
	SIGNAL segment_data : STD_LOGIC_VECTOR(6 DOWNTO 0);
	SIGNAL count_1Mhz	: STD_LOGIC_VECTOR(5 DOWNTO 0); 
	SIGNAL enable		: std_logic;

BEGIN

	PROCESS(CLOCK_50)
	BEGIN
-- Divide by 50
		IF CLOCK_50'EVENT and CLOCK_50 = '1' THEN
			IF count_1Mhz < 49 THEN
				count_1Mhz <= count_1Mhz + 1;
			ELSE
				count_1Mhz <= "000000";
			END IF;
			if count_1Mhz > 2 THEN
				enable <= '1';
			else
				enable <= '0';
			end if;
		END IF;	

	END PROCESS;

	PROCESS  (Hex_digit)
		-- HEX to 7 Segment Decoder for LED Display
	BEGIN
		-- Hex-digit is the four bit binary value to display in hexadecimal
	  CASE Hex_digit IS
         WHEN "0000" =>
             segment_data <= "1111110";
         WHEN "0001" =>
             segment_data <= "0110000";
         WHEN "0010" =>
             segment_data <= "1101101";
         WHEN "0011" =>
             segment_data <= "1111001";
         WHEN "0100" =>
             segment_data <= "0110011";
       	 WHEN "0101" =>
             segment_data <= "1011011";
       	 WHEN "0110" =>
             segment_data <= "1011111";
    	 WHEN "0111" =>
             segment_data <= "1110000";
 	     WHEN "1000" =>
             segment_data <= "1111111";
     	 WHEN "1001" =>
             segment_data <= "1111011"; 
         WHEN "1010" =>
             segment_data <= "1110111";
       	 WHEN "1011" =>
             segment_data <= "0011111"; 
       	 WHEN "1100" =>
             segment_data <= "1001110"; 
       	 WHEN "1101" =>
       		 segment_data <= "0111101"; 
      	 WHEN "1110" =>
      	     segment_data <= "1001111"; 
      	 WHEN "1111" =>
      	     segment_data <= "1000111"; 
	   	 WHEN OTHERS =>
        	 segment_data <= "0111110";
	  END CASE;

	END PROCESS;

		-- extract segment data bits and invert
		-- LED driver circuit is inverted
		-- jlobo: OR with enable to reduce brightness
	HEX0(6) <= enable OR (NOT segment_data(0));
	HEX0(5) <= enable OR (NOT segment_data(1));
	HEX0(4) <= enable OR (NOT segment_data(2));
	HEX0(3) <= enable OR (NOT segment_data(3));	
	HEX0(2) <= enable OR (NOT segment_data(4));
	HEX0(1) <= enable OR (NOT segment_data(5));
	HEX0(0) <= enable OR (NOT segment_data(6));
END a;

