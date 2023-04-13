![example workflow](https://github.com/npatsiatzis/bcd_bin_conv/actions/workflows/regression.yml/badge.svg)
![example workflow](https://github.com/npatsiatzis/bcd_bin_conv/actions/workflows/coverage.yml/badge.svg)

### RTL implementation for conversion from bcd to binary and vice versa


- conversion based on the double dabble algorithm
- purely combinational implementation that can be pipelined appropriately for timing considerations
- CoCoTB testbench for functional verification	
	- $make
- CoCoTB-test unit testing to exercise the CoCoTB tests across a range of values for the generic parameters
    - $  SIM=ghdl pytest -n auto -o log_cli=True --junitxml=test-results.xml --cocotbxml=test-cocotb.xml

