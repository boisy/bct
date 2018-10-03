# Bitstream Computation Toolkit

Bitstream Computation Toolkit (BCT) is a collection of bitstream conversion and computation functions in Python to aid stochastic computing research.

## Getting Started

BCT has tools for converting numbers between 0 and 1 into bitstreams. For example, one possible bitstream representation of: 0.25 is 1000. Also, 0.125 is 10000000
  
To convert a number to a bistream:

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

### Running Unit Tests
To run unit tests:

```python bct.py```

## Attributions

Authors: Boisy G. Pitre and Dr. M. Hassan Najafi

SCHOOL OF COMPUTING & INFORMATICS
University of Louisiana at Lafayette
