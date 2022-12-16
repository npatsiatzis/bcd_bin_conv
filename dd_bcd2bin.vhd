library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity dd_bcd2bin is
generic(
	g_bcd_width : natural :=12;
	g_bin_width : natural :=10);
port(
	i_bcd : in std_ulogic_vector(g_bcd_width -1 downto 0);
	o_bin : out std_ulogic_vector(g_bin_width -1 downto 0));
end dd_bcd2bin;

architecture conv of dd_bcd2bin is

	function  dd (bcd_vec : std_ulogic_vector) return std_ulogic_vector is
		constant  c_digits : natural := g_bcd_width /4;
		variable bin : unsigned(g_bin_width -1 downto 0) := (others => '0');
		variable bcd : unsigned(g_bcd_width -1 downto 0);
	begin
		bcd := unsigned(bcd_vec);
		for i in bin'range loop
			bin := bcd(0) & bin(bin'high downto 1);
			bcd := '0' & bcd(bcd'high downto 1); 
			for j in 0 to c_digits-1 loop 
				if(bcd(j*4 + 3 downto j*4) >= 8) then
					bcd(j*4 + 3 downto j*4) := bcd(j*4 + 3 downto j*4) - 3;
				end if;
			end loop;

		end loop;
		return std_ulogic_vector(bin);
	end  dd;
begin

	o_bin <= dd(i_bcd);
end conv;