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
		term1 = bct.unary_sng(4, .75)
		term2 = bct.unary_sng(4, .25)
		term1 = bct.clockdiv(1, term1, 2)
		term2 = bct.clockdiv(2, term2, 2)
		print(term1 + " x " + term2)
		product = bct.and_op(term1, term2)
		self.assertEqual(product, '1110000000000000')

		term1 = bct.unary_sng(4, .25)
		term2 = bct.unary_sng(4, .25)
		term3 = bct.unary_sng(4, .25)
		term1 = bct.clockdiv(1, term1, 3)
		term2 = bct.clockdiv(2, term2, 3)
		term3 = bct.clockdiv(3, term3, 3)
		product = bct.and_op(term1, term2)
		product = bct.and_op(product, term3)
		self.assertEqual(product, '1000000000000000000000000000000000000000000000000000000000000000')
				
		term1 = bct.unary_sng(32, .5)
		term2 = bct.unary_sng(32, .125)
		term3 = bct.unary_sng(32, .625)
		term1 = bct.clockdiv(1, term1, 3)
		term2 = bct.clockdiv(2, term2, 3)
		term3 = bct.clockdiv(3, term3, 3)
		product = bct.and_op(term1, term2)
		product = bct.and_op(product, term3)

		expected_value = .5 * .125 * .625
		number_of_1s = bct.number_of_1(product)
		calculated_value = number_of_1s / len(product)
		print("expected_value = " + str(expected_value))
		print("calculated_value = " + str(calculated_value))

		term1 = bct.unary_sng(32, .75)
		term2 = bct.unary_sng(32, .25)
		term3 = bct.unary_sng(32, .125)
		term1 = bct.rotate(1, term1, 3)
		term2 = bct.rotate(2, term2, 3)
		term3 = bct.rotate(3, term3, 3)
		product = bct.and_op(term1, term2)
		product = bct.and_op(product, term3)

		expected_value = .75 * .25 * .125
		number_of_1s = bct.number_of_1(product)
		calculated_value = number_of_1s / len(product)
		print("expected_value = " + str(expected_value))
		print("calculated_value = " + str(calculated_value))

# perform unit testing if no parameters specified (e.g. python bct.py)
if __name__ == '__main__':
	unittest.main()
