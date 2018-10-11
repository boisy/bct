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
# Parameters:
#  stream_length: length, in bits, of the desired output bitstream
#  number: the floating point number (0 <=n < 1) to represent as a bitstream
#
# e.g. unary_sng(4, .75) -> 1 1 1 0 (1110)
#      unary_sng(8, .75) -> 11 11 11 00 (11111100)
#      unary_sng(12, .75) -> 111 111 111 000 (111111111000)
def unary_sng(stream_length, number):
	result = ''
	compare2 = number * stream_length
	for counter in range(stream_length):
		compare1 = counter
		if compare1 < compare2:
			result = result + '1'
		else:
			result = result + '0'
	return result

# Clock division method
# Extends a bitstream through clock divison
#
# Parameters:
#  order: the operational order of the bitstream 
#  bitstream: the bitstream to use
#  total_inputs: the total number of inputs
#
# e.g. clockdiv(1, '1110', 2) -> '1110 1110 1110 1110'
#      clockdiv(2, '1001', 2) -> '11 00 00 11 11 00 00 11'
#      clockdiv(2, '1001', 3) -> '11 00 00 11' (repeated to 4^3 bits)
def clockdiv(order, bitstream, total_inputs):
	result = ''
	repeat_count = pow(len(bitstream), order - 1)
	
	for counter2 in range(len(bitstream)):
		for counter3 in range(order):
			bit = bitstream[counter2]
			result = result + bit
		
	entire_length = pow(len(bitstream), total_inputs)
	while len(result) < entire_length:
		result = result + result

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

# NOT operation on bitstreams
def not_op(bitstream):
	result = ''

	for x in range(len(bitstream)):
		if bitstream[x] == '0':
			result = result + '1'
		else:
			result = result + '0'

	return result
	
# AND operation on bitstreams
def and_op(bitstream1, bitstream2):
	result = ''

	for x in range(len(bitstream1)):
		bs1 = int(bitstream1[x])
		bs2 = int(bitstream2[x])
		bsr = bs1 & bs2
		result = result + str(bsr)

	return result
	
# NAND operation on bitstreams
def nand_op(bitstream1, bitstream2):
	and_result = and_op(bitstream1, bitstream2)
	result = not_op(and_result)

	return result
	
# OR operation on bitstreams
def or_op(bitstream1, bitstream2):
	result = ''

	for x in range(len(bitstream1)):
		bs1 = int(bitstream1[x])
		bs2 = int(bitstream2[x])
		bsr = bs1 | bs2
		result = result + str(bsr)

	return result

# NOR operation on bitstreams
def nor_op(bitstream1, bitstream2):
	or_result = or_op(bitstream1, bitstream2)
	result = not_op(or_result)

	return result
	
# XOR operation on bitstreams
def xor_op(bitstream1, bitstream2):
	result = ''

	for x in range(len(bitstream1)):
		bs1 = int(bitstream1[x])
		bs2 = int(bitstream2[x])
		bsr = bs1 ^ bs2
		result = result + str(bsr)

	return result
# NXOR operation on bitstreams
def nxor_op(bitstream1, bitstream2):
	xor_result = xor_op(bitstream1, bitstream2)
	result = not_op(xor_result)

	return result

# NOR operation on bitstreams
# Convert a bitstream to a float
def to_float(bitstream):
	result = 0

	for a in bitstream:
		if a == '1':
			result = result + 1

	return float(result) / float(len(bitstream))


# Unit tests
class bctTest(unittest.TestCase):
	def test_clockdiv(self):
		result = clockdiv(1, '1110', 2)
		self.assertEqual(result, '1110111011101110')
		result = clockdiv(2, '1001', 2)
		self.assertEqual(result, '1100001111000011')
		result = clockdiv(2, '1001', 3)
		self.assertEqual(result, '1100001111000011110000111100001111000011110000111100001111000011')

	def test_unary_sng(self):
		result = unary_sng(4, .75)
		self.assertEqual(result, '1110')
		result = unary_sng(8, .75)
		self.assertEqual(result, '11111100')
		result = unary_sng(12, .75)
		self.assertEqual(result, '111111111000')

		result = unary_sng(4, .25)
		self.assertEqual(result, '1000')
		result = unary_sng(8, .25)
		self.assertEqual(result, '11000000')
		result = unary_sng(12, .25)
		self.assertEqual(result, '111000000000')

	def test_unary_sng(self):
		result = unary_sng(4, .75)
		self.assertEqual(result, '1110')
		result = unary_sng(8, .75)
		self.assertEqual(result, '11111100')
		result = unary_sng(12, .75)
		self.assertEqual(result, '111111111000')

		result = unary_sng(4, .25)
		self.assertEqual(result, '1000')
		result = unary_sng(8, .25)
		self.assertEqual(result, '11000000')
		result = unary_sng(12, .25)
		self.assertEqual(result, '111000000000')

		result = unary_sng(8, .125)
		self.assertEqual(result, '10000000')
		result = unary_sng(16, .125)
		self.assertEqual(result, '1100000000000000')
		result = unary_sng(24, .125)
		self.assertEqual(result, '111000000000000000000000')


	def test_rotate(self):
		result = rotate('10')
		self.assertEqual(result, '1001')

	def test_to_float(self):
		result = to_float('10001001')
		self.assertEqual(result, 0.375)

	def test_not(self):
		result = not_op('100100')
		self.assertEqual(result, '011011')

	def test_and(self):
		result = and_op('100', '001')
		self.assertEqual(result, '000')

	def test_nand(self):
		result = nand_op('101', '011')
		self.assertEqual(result, '110')

	def test_or(self):
		result = or_op('111', '001')
		self.assertEqual(result, '111')
		
	def test_nor(self):
		result = nor_op('111', '001')
		self.assertEqual(result, '000')

	def test_xor(self):
		result = xor_op('101', '011')
		self.assertEqual(result, '110')

	def test_nxor(self):
		result = nxor_op('101', '011')
		self.assertEqual(result, '001')
		
# perform unit testing if no parameters specified (e.g. python bct.py)
if __name__ == '__main__':
	unittest.main()
