![example workflow](https://github.com/npatsiatzis/bcd_bin_conv/actions/workflows/regression.yml/badge.svg)
![example workflow](https://github.com/npatsiatzis/bcd_bin_conv/actions/workflows/coverage.yml/badge.svg)
![example workflow](https://github.com/npatsiatzis/bcd_bin_conv/actions/workflows/regression_pyuvm_bcd_2_bin.yml/badge.svg)
![example workflow](https://github.com/npatsiatzis/bcd_bin_conv/actions/workflows/coverage_pyuvm_bcd_2_bin.yml/badge.svg)
### RTL implementation for conversion from bcd to binary and vice versa


- conversion based on the double dabble algorithm
- purely combinational implementation that can be pipelined appropriately for timing considerations

-- BCD to Binary conversion direction
-- RTL code in:
- [VHDL](https://github.com/npatsiatzis/bcd_bin_conv/tree/main/bcd_2_bin/rtl/VHDL)

-- Functional verification with methodologies:
- [cocotb](https://github.com/npatsiatzis/bcd_bin_conv/tree/main/bcd_2_bin/cocotb_sim)
- [pyuvm](https://github.com/npatsiatzis/bcd_bin_conv/tree/main/bcd_2_bin/pyuvm_sim)


