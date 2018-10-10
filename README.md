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

#### NOT operation
Takes a bitstream and returns the complement of each of the bits
```
result = not_op('10001')
print(result)
01110
```

### OR operation
Takes two bitstreams and returns the NOR result of the bits
```
result = nor_op('1101', '1001')
print(result)
1101
```

### NOR operation
Takes two bitstreams and returns the OR result of the bits
```
result = or_op('1101', '1001')
print(result)
0010
```

### AND operation
Takes two bitstreams and returns the AND result of the bits
```
result = and_op('1101', '1001')
print(result)
1001
```

### NAND operation
Takes two bitstreams and returns the NAND result of the bits
```
result = nand_op('1101', '1001')
print(result)
0110
```

### XOR operation
Takes two bitstreams and returns the XOR result of the bits
```
result = xor_op('1101', '1001')
print(result)
0100
```

### NXOR operation
Takes two bitstreams and returns the NXOR result of the bits
```
result = nxor_op('1101', '1001')
print(result)
1011
```

### Running Unit Tests
To run unit tests:

```python bct.py```

## Attributions

Authors: Boisy G. Pitre and Dr. M. Hassan Najafi

SCHOOL OF COMPUTING & INFORMATICS
University of Louisiana at Lafayette
