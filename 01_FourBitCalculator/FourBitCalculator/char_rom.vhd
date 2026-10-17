library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;

entity char_rom is
  Port (
    char_code  : in  std_logic_vector(5 downto 0); -- ASCII code (0–127)
    row_index  : in  std_logic_vector(2 downto 0); -- Row index within 8x8 char (0–7)
    row_pixels : out std_logic_vector(7 downto 0)  -- Pixel pattern for that row
  );
end char_rom;

architecture Behavioral of char_rom is

  -- ROM: 128 characters × 8 rows = 1024 entries
  type rom_array is array (0 to 1023) of std_logic_vector(7 downto 0);
  constant rom : rom_array := (
    -- ASCII 32 (space)
    256 => "00000000", 257 => "00000000", 258 => "00000000", 259 => "00000000",
    260 => "00000000", 261 => "00000000", 262 => "00000000", 263 => "00000000",

    -- ASCII 33 (!)
    264 => "00011000", 265 => "00011000", 266 => "00011000", 267 => "00011000",
    268 => "00000000", 269 => "00000000", 270 => "00011000", 271 => "00000000",

    -- Add more characters here...

    others => "00000000"
  );

  signal index : integer range 0 to 1023;

begin

  -- Type conversion from std_logic_vector(9 downto 0) to integer
  index <= to_integer(all(char_code & row_index));

  row_pixels <= rom(index);

end Behavioral;
