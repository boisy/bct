# Bitstream Computation Toolkit

Bitstream Computation Toolkit (BCT) is a collection of bitstream conversion and computation functions in Python to aid stochastic computing research.

## Getting Started

BCT has tools for converting numbers between 0 and 1 into bitstreams. For example, one possible bitstream representation of:

  0.25
 
is:

  1000
  
Another example:

  0.125

is:

  10000000
  
Converting such a number to a bitstream is possible with the following code:

```import bct

bst = bct.unary(1, 0.125)
print(bst)
```
 
### Using the Toolkit

### Running Unit Tests
To run unit tests:

```python bct.py```

## Attributions

Authors: Boisy G. Pitre and Dr. M. Hassan Najafi

SCHOOL OF COMPUTING & INFORMATICS
University of Louisiana at Lafayette
