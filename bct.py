# Bitstream Computation Toolkit
#
# Authors: Boisy G. Pitre, Dr. M. Hassan Najafi
# Computer Science Department
# University of Louisiana at Lafayette
# Lafayette, Louisiana

import sys
import unittest

# Unit tests
class BitstreamTest(unittest.TestCase):
	def test_unary(self):
		output = unary(1, .75)
		self.assertEqual(output, '1110')
		output = unary(2, .75)
		self.assertEqual(output, '11111100')
		output = unary(3, .75)
		self.assertEqual(output, '111111111000')

		output = unary(1, .25)
		self.assertEqual(output, '1000')
		output = unary(2, .25)
		self.assertEqual(output, '11000000')
		output = unary(3, .25)
		self.assertEqual(output, '111000000000')

# Unary bitstream generator
# Added Oct 03 2018
#
# e.g. unary(1, .75) -> 1 1 1 0 (1110)
#      unary(2, .75) -> 11 11 11 00 (11111100)
#      unary(3, .75) -> 111 111 111 000 (111111111000)
def unary(n, number):
	result = ''
	numerator, denominator = number.as_integer_ratio()
	for counter in range(denominator):
		for i in range(n):
			if counter < numerator:
				result = result + '1'
			else:
				result = result + '0'
	return result


# perform unit testing if no parameters specified (e.g. python bct.py)
if __name__ == '__main__':
	unittest.main()
