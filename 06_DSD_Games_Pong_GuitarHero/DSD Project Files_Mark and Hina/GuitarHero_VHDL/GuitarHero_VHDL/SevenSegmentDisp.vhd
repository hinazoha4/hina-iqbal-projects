-----------------------------------------------------------------------------
-- Ryan Campbell & Marguerite Smith
--
--	11/23/2021
--
--	ECE 287
--
-- Final Project
--
--	The purpose of this code is the take the output from the buttons in
-- the guitar hero game and to translate them into a usable output for
-- the two seven segment displays in use.
-----------------------------------------------------------------------------

LIBRARY ieee;
USE ieee.std_logic_1164.all;

ENTITY SevenSegPort IS

	PORT (s :	IN	STD_LOGIC_VECTOR(4 DOWNTO 0) := (OTHERS => '0');
			outA, outB, outC, outD, outE, outF, outG, h, i, j, k, l, m, n : OUT STD_LOGIC) ;
			
END SevenSegPort;

ARCHITECTURE SevenSegmentDisp OF SevenSegPort IS
BEGIN
	--First Seven Segment Display
	
	outA <= not((s(4) and s(1)) or (not s(3) and s(1)) or (s(4) and not s(2) and s(0)) or (not s(4) and not s(2) and not s(0)) or (not s(4) and s(2) and s(0)) or (not s(4) and s(3) and not s(1)) or (s(4) and not s(3) and not s(0)));
	
	outB <= not((not s(4) and not s(2)) or (s(3) and s(2) and not s(1)) or (s(4) and not s(3) and s(0)) or (not s(3) and s(1) and s(0)) or (not s(4) and s(3) and not s(0)) or (s(4) and not s(3) and s(1)) or (s(2) and not s(1) and not s(0)) or (s(3) and not s(1) and not s(0)));
	
	outC <= not(s(0) or (s(3) and not s(2)) or (not s(3) and not s(1)) or (s(4) and not s(2)) or (not s(4) and s(2) and s(1)));
	
	outD <= not((not s(4) and not s(2) and not s(0)) or (not s(3) and s(1) and not s(0)) or (not s(2) and s(1) and not s(0)) or (s(4) and not s(3) and not s(0)) or (s(3) and s(2) and not s(1)) or (s(3) and s(2) and s(0)) or (s(4) and s(2) and s(1)) or (s(4) and s(3) and s(0)) or (not s(4) and not s(3) and not s(2) and s(1)) or (not s(4) and s(2) and not s(1) and s(0)));
	
	outE <= not((not s(4) and not s(2) and not s(0)) or (not s(3) and s(1) and not s(0)) or (not s(2) and s(1) and not s(0)) or (s(4) and not s(3) and not s(0)) or (not s(4) and s(3) and not s(1) and not s(0)));
	
	outF <= not((not s(3) and not s(1) and not s(0)) or (s(3) and not s(2) and not s(1)) or (s(3) and not s(2) and not s(0)) or (s(3) and s(2) and s(1)) or (s(4) and not s(2) and s(1)) or (not s(4) and not s(3) and s(2) and not s(1)) or (not s(4) and not s(3) and s(2) and not s(0)));
	
	outG <= not((s(3) and not s(1)) or (s(3) and s(2)) or (s(4) and s(1)) or (not s(3) and not s(2) and s(1)) or (not s(3) and s(1) and not s(0)) or (not s(4) and s(2) and not s(1)) or (s(4) and not s(2) and not s(0)));
	
	--Second Seven Segment Display
	
	h <= not((not s(4) and not s(3)) OR (not s(3) and s(2)) or (s(4) and s(3)) or (not s(4) and not s(2) and not s(1)));
	
	i <= '0';
	
	j <= not((not s(4)) or (not s(3) and not s(2)));
	
	k <= not((not s(4) and not s(3)) OR (not s(3) and s(2)) or (s(4) and s(3)) or (not s(4) and not s(2) and not s(1)));
	
	l <= not((not s(4) and not s(3)) OR (not s(3) and s(2)) or (s(4) and s(3)) or (not s(4) and not s(2) and not s(1)));
	
   m <= not((not s(4) and not s(3)) or (not s(4) and not s(2) and not s(1)));

	n <= not((s(4) and s(2)) or (s(4) and s(3)));
	
END SevenSegmentDisp;