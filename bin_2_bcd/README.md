![example workflow](https://github.com/npatsiatzis/bcd_bin_conv/actions/workflows/regression.yml/badge.svg)
![example workflow](https://github.com/npatsiatzis/bcd_bin_conv/actions/workflows/coverage.yml/badge.svg)
![example workflow](https://github.com/npatsiatzis/bcd_bin_conv/actions/workflows/regression_pyuvm_bin_2_bcd.yml/badge.svg)
![example workflow](https://github.com/npatsiatzis/bcd_bin_conv/actions/workflows/coverage_pyuvm_bin_2_bcd.yml/badge.svg)
### RTL implementation for conversion from bcd to binary and vice versa


- conversion based on the double dabble algorithm
- purely combinational implementation that can be pipelined appropriately for timing considerations

-- Binary to BCD conversion direction
-- RTL code in:
- [VHDL](https://github.com/npatsiatzis/bcd_bin_conv/tree/main/bin_2_cd/rtl/VHDL)

-- Functional verification with methodologies:
- [cocotb](https://github.com/npatsiatzis/bcd_bin_conv/tree/main/bin_2_bcd/cocotb_sim)
- [pyuvm](https://github.com/npatsiatzis/bcd_bin_conv/tree/main/bin_2_bcd/pyuvm_sim)


