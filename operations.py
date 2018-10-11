# Bitstream Computation Toolkit
# Operations
#
# Authors: Boisy G. Pitre, Dr. M. Hassan Najafi
# Computer Science Department
# University of Louisiana at Lafayette
# Lafayette, Louisiana

import bct
import unittest

# Unit tests
class bctTest(unittest.TestCase):
	def test_multiply_two_numbers(self):
		multiplier = bct.unary_sng(4, .75)
		multiplicand = bct.unary_sng(4, .25)
		multiplier = bct.clockdiv(1, multiplier, 2)
		multiplicand = bct.clockdiv(2, multiplicand, 2)
		print(multiplier + " x " + multiplicand)
		product = bct.and_op(multiplier, multiplicand)
		self.assertEqual(product, '111')

				
# perform unit testing if no parameters specified (e.g. python bct.py)
if __name__ == '__main__':
	unittest.main()
