# Bitstream Computation Toolkit
#
# Authors: Boisy G. Pitre, Dr. M. Hassan Najafi
# Computer Science Department
# University of Louisiana at Lafayette
# Lafayette, Louisiana

import sys
import unittest

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


# Rotate the passed bitstream
#
# e.g. rotate('10') -> 10 01
#       rotate('1010') -> 1010 0101 1010 0101
def rotate(bitstring):
	result = ''
	count = 0
	currentBit = ''
	targetSize = len(bitstring) * len(bitstring)
	while len(result) < targetSize:
		currentBit = bitstring[count % len(bitstring)]
		count = count + 1
		result = result + currentBit
		if len(result) % len(bitstring) == 0 and len(result) < targetSize:
			# we have arrived at a position where the last bit needs to be repeated
			result = result + currentBit

	return result

# Convert a bitstream to a float
def to_float(bitstream):
	result = 0

	for a in bitstream:
		if a == '1':
			result = result + 1

	return float(result) / float(len(bitstream))


# Unit tests
class bctTest(unittest.TestCase):
	def test_unary(self):
		result = unary(1, .75)
		self.assertEqual(result, '1110')
		result = unary(2, .75)
		self.assertEqual(result, '11111100')
		result = unary(3, .75)
		self.assertEqual(result, '111111111000')

		result = unary(1, .25)
		self.assertEqual(result, '1000')
		result = unary(2, .25)
		self.assertEqual(result, '11000000')
		result = unary(3, .25)
		self.assertEqual(result, '111000000000')

		result = unary(1, .125)
		self.assertEqual(result, '10000000')
		result = unary(2, .125)
		self.assertEqual(result, '1100000000000000')
		result = unary(3, .125)
		self.assertEqual(result, '111000000000000000000000')


	def test_rotate(self):
		result = rotate('10')
		self.assertEqual(result, '1001')

	def test_to_float(self):
		result = to_float('10001001')
		self.assertEqual(result, 0.375)

		
# perform unit testing if no parameters specified (e.g. python bct.py)
if __name__ == '__main__':
	unittest.main()
