# Bitstream Computation Toolkit

Bitstream Computation Toolkit (BCT) is a collection of bitstream conversion and computation functions in Python to aid stochastic computing research.

## Getting Started

BCT has tools for converting numbers between 0 and 1 into bitstreams. For example, one possible bitstream representation of: 0.25 is 1000. Also, 0.125 is 10000000
  
To convert a number to a bitstream:

```
import bct

bst = bct.unary(1, 0.5)
print(bst) # prints 10
```
 
It is possible to extend the number of bits used in the representation by changing the first parameter:

```
import bct

bst = bct.unary(2, 0.25)
print(bst) # prints 11000000
```

### Using the Toolkit

### Primitives
BCT offers a number of primitives that work on bitstreams:

not_op(bitstream): takes a bitstream and returns the complement of each of the bits (e.g. not_op('10001') -> '01110')
or_op(bitstream1, bitstream2): takes two bitstreams and returns the OR result of the bits (e.g. or_op('1101', '1001') -> '1101')
nor_op(bitstream1, bitstream2): takes two bitstreams and returns the NOR result of the bits (e.g. or_op('1101', '1001') -> '0010')
and_op(bitstream1, bitstream2): takes two bitstreams and returns the AND result of the bits (e.g. or_op('1101', '1001') -> '1001')
nand_op(bitstream1, bitstream2): takes two bitstreams and returns the NAND result of the bits (e.g. or_op('1101', '1001') -> '0110')
xor_op(bitstream1, bitstream2): takes two bitstreams and returns the XOR result of the bits (e.g. or_op('1101', '1001') -> '0100')
nxor_op(bitstream1, bitstream2): takes two bitstreams and returns the NXOR result of the bits (e.g. or_op('1101', '1001') -> '1011')

### Running Unit Tests
To run unit tests:

```python bct.py```

## Attributions

Authors: Boisy G. Pitre and Dr. M. Hassan Najafi

SCHOOL OF COMPUTING & INFORMATICS
University of Louisiana at Lafayette
