# Bitstream Computation Toolkit
#
# Authors: Boisy G. Pitre, Dr. M. Hassan Najafi
# Computer Science Department
# University of Louisiana at Lafayette
# Lafayette, Louisiana

import sys
import unittest

# Number of 1's in a bitstream
# Added Oct 17 2018
def number_of_1(bitstream):
	counter = 0
	for i in range(len(bitstream)):
		if bitstream[i] == '1':
			counter = counter + 1

	return counter
	
# Number of 0's in a bitstream
# Added Oct 17 2018
def number_of_0(bitstream):
	counter = 0
	for i in range(len(bitstream)):
		if bitstream[i] == '0':
			counter = counter + 1

	return counter
	
# Unary bitstream generator
# Added Oct 03 2018
#
# Parameters:
#  stream_length: length, in bits, of the desired output bitstream
#  number: the floating point number (0 <= n < 1) to represent as a bitstream
#
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
# e.g. clockdiv(2, '1110', 2) -> '1111 1111 1111 0000'
def clockdiv(order, bitstream, total_inputs):
	result = ''
	repeat_count = pow(len(bitstream), order - 1)
	
	for counter2 in range(len(bitstream)):
		for counter3 in range(repeat_count):
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
def rotate(order, bitstream, total_inputs):
	result = ''
	stall_count = pow(len(bitstream), order - 1)
	entire_length = pow(len(bitstream), total_inputs)
	count = 0
	currentBit = ''
	while len(result) < entire_length:
		currentBit = bitstream[count % len(bitstream)]
		count = count + 1
		result = result + currentBit
		if stall_count != 1 and len(result) % stall_count == 0 and len(result) < entire_length:
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
		result = rotate(1, '1000', 1)
		self.assertEqual(result, '1000')
		result = rotate(1, '1000', 3)
		self.assertEqual(result, '1000100010001000100010001000100010001000100010001000100010001000')
		result = rotate(2, '1000', 3)
		self.assertEqual(result, '1000010000100001100001000010000110000100001000011000010000100001')

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
		
	def test_clockdiv(self):
		result = clockdiv(2, '1000', 2)
		self.assertEqual(result, '1111000000000000')
		
	def test_number_of_1(self):
		result = number_of_1('1000')
		self.assertEqual(result, 1)
		
	def test_number_of_0(self):
		result = number_of_0('1000')
		self.assertEqual(result, 3)
		
# perform unit testing if no parameters specified (e.g. python bct.py)
if __name__ == '__main__':
	unittest.main()
