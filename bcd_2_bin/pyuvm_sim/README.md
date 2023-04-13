![example workflow](https://github.com/npatsiatzis/bcd_bin_conv/actions/workflows/regression_pyuvm_bcd_2_bin.yml/badge.svg)
![example workflow](https://github.com/npatsiatzis/bcd_bin_conv/actions/workflows/coverage_pyuvm_bcd_2_bin.yml/badge.svg)

### RTL implementation for conversion from bcd to binary and vice versa


- run pyuvm testbench
    - $ make
- run unit testing of the pyuvm testbench
    - $  SIM=ghdl pytest -n auto -o log_cli=True --junitxml=test-results.xml --cocotbxml=test-cocotb.xml

