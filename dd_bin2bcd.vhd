library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity dd_bin2bcd is
generic(
	g_bin_width : natural := 8;
	g_bcd_width : natural := 12);
port(
	i_bin : in std_ulogic_vector(g_bin_width-1 downto 0);
	o_bcd : out std_ulogic_vector(g_bcd_width-1 downto 0));
end dd_bin2bcd;

architecture rtl of dd_bin2bcd is

	--Calculate the length of the number in decimal notation
	function floor_log(n : natural; base : natural) return natural is 
		variable log, residual : natural;
	begin
		residual := n;
		log :=0;

		while (residual > (base-1)) loop
			residual := residual / base;
			log := log  +1;
		end loop ; 
		return log;

	end floor_log;

	function decimal_size (dec : natural) return natural is 
	begin
		if(dec = 0) then
			return 1;
		else
			return floor_log(dec,10) + 1;
		end if;
	end decimal_size;


	--Double-Dabble method to convert a binary numer to bcd representation
	function dd (bin_vec : std_ulogic_vector) return std_ulogic_vector is
		constant  c_digits : natural := decimal_size(2**g_bin_width-1);
		variable w_bin : unsigned(g_bin_width-1 downto 0);
		variable w_bcd : unsigned(g_bcd_width-1 downto 0) :=(others => '0');
	begin
		w_bin := unsigned(bin_vec);
		for i in 0 to g_bin_width-1 loop

			for j in 0 to c_digits-1 loop
				if(w_bcd(j*4 + 3 downto j*4) > 4) then
					w_bcd(j*4 + 3 downto j*4) := w_bcd(j*4 + 3 downto j*4) + 3;
				end if;
			end loop;

			w_bcd := w_bcd(w_bcd'left-1 downto 0) & w_bin(w_bin'left);
			w_bin := w_bin(w_bin'left -1 downto 0) & '0';

		end loop;
		return std_ulogic_vector(w_bcd);	
	end dd;

begin

	o_bcd <= dd(i_bin);
	
	
end rtl;