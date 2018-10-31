# Bitstream Computation Toolkit
#
# Authors: Boisy G. Pitre, Dr. M. Hassan Najafi
# Computer Science Department
# University of Louisiana at Lafayette
# Lafayette, Louisiana

import numpy
import sys
import unittest
from lfsr import LFSR

# Count the number of 1's in a bitstream
# Added Oct 17 2018
def number_of_1(bitstream):
	counter = 0
	for i in range(len(bitstream)):
		if bitstream[i] == 1:
			counter = counter + 1

	return counter
	
# Count the number of 0's in a bitstream
# Added Oct 17 2018
def number_of_0(bitstream):
	counter = 0
	for i in range(len(bitstream)):
		if bitstream[i] == 0:
			counter = counter + 1

	return counter
	
# Repeat bitstream
def repeat(bitstream, repeat_count):
	result = ''
	for i in range(repeat_count):
		result = result + bitstream

	return result

# LFSR maximal period psuedo (4 bit, 5 bit, 6 bit, etc)
# precision = number of bits
# position in tap file
# seed = starting value
def lfsr_SNG(precision, position_in_tap_file, seed):
	# open tap file
	filename = str(precision) + ".txt"
	file = open(filename, "r")
	# get "position_in_tap_file"th value
	for i in range(position_in_tap_file):
		tap = file.readline()
	file.close()
	# build combination from tap
	tap = int(tap, 16)
	combination = []
	for t in reversed(range(precision)):
		if tap & (1 << t):
			combination.append(t + 1)

	npseed = numpy.empty(0)
	# build numpy array of binary from seed
	for t in reversed(range(precision)):
		if seed & (1 << t):
			npseed = numpy.append(npseed, 1)
		else:
			npseed = numpy.append(npseed, 0)

	# create LFSR
	L = LFSR(combination, npseed)
	# for maximal period, collect values
	result = []
	for t in range(pow(2, precision) - 1):
		v = L.runKCycle(precision)
		# convert v to int
		value = 0
		for i in range(len(v)):
			if v[i] == 1:
				value = value + pow(2, precision - i - 1)
		result.append(value)

	# convert v to an integer
	# return maximal period array
	return result


# Unary bitstream generator
# Added Oct 03 2018
#
# Parameters:
#  stream_length: length, in bits, of the desired output bitstream
#  number: the floating point number (0 <= n < 1) to represent as a bitstream
#
def unary_SNG(stream_length, number):
	result = numpy.zeros(0)
	compare2 = number * stream_length
	for counter in range(stream_length):
		compare1 = counter
		if compare1 < compare2:
			result = numpy.append(result, 1)
		else:
			result = numpy.append(result, 0)
	return result

# Clock division method
# Extends a bitstream through clock divison
#
# Parameters:
#  order: the operational order of the bitstream 
#  bitstream: the bitstream to use
#  total_inputs: the total number of inputs
#
# e.g. clockdiv(2, [1, 1, 1, 0], 2) -> [1, 1, 1, 1,  1, 1, 1, 1,  1, 1, 1, 1,  0, 0, 0, 0]
def clockdiv(order, bitstream, total_inputs):
	result = numpy.zeros(0)
	repeat_count = pow(len(bitstream), order - 1)
	
	for counter2 in range(len(bitstream)):
		for counter3 in range(repeat_count):
			bit = bitstream[counter2]
			result = numpy.append(result, bit)
		
	entire_length = pow(len(bitstream), total_inputs)
	while len(result) < entire_length:
		result = numpy.append(result, result)

	return result
	
# Rotate the passed bitstream
#
# e.g. rotate([1, 0]) -> [1, 0,  0, 1]
#       rotate([1, 0, 1, 0]) -> [1, 0, 1, 0,  0, 1, 0, 1,  1, 0, 1, 0,  0, 1, 0, 1]
def rotate(order, bitstream, total_inputs):
	result = numpy.zeros(0)
	stall_count = pow(len(bitstream), order - 1)
	entire_length = pow(len(bitstream), total_inputs)
	count = 0
	currentBit = 0
	while len(result) < entire_length:
		currentBit = bitstream[count % len(bitstream)]
		count = count + 1
		result = numpy.append(result, currentBit)
		if stall_count != 1 and len(result) % stall_count == 0 and len(result) < entire_length:
			# we have arrived at a position where the last bit needs to be repeated
			result = numpy.append(result, currentBit)

	return result

# Relatively prime
#def relprim(order, bitstream, total_inputs):

# NOT operation on bitstreams
def not_op(bitstream):
	result = numpy.zeros(0)

	for x in range(len(bitstream)):
		if bitstream[x] == 0:
			result = numpy.append(result, 1)
		else:
			result = numpy.append(result, 0)

	return result
	
# AND operation on bitstreams
def and_op(bitstream1, bitstream2):
	result = numpy.zeros(0)

	for x in range(len(bitstream1)):
		bs1 = int(bitstream1[x])
		bs2 = int(bitstream2[x])
		bsr = bs1 & bs2
		result = numpy.append(result, bsr)

	return result
	
# NAND operation on bitstreams
def nand_op(bitstream1, bitstream2):
	and_result = and_op(bitstream1, bitstream2)
	result = not_op(and_result)

	return result
	
# OR operation on bitstreams
def or_op(bitstream1, bitstream2):
	result = numpy.zeros(0)

	for x in range(len(bitstream1)):
		bs1 = int(bitstream1[x])
		bs2 = int(bitstream2[x])
		bsr = bs1 | bs2
		result = numpy.append(result, bsr)

	return result

# NOR operation on bitstreams
def nor_op(bitstream1, bitstream2):
	or_result = or_op(bitstream1, bitstream2)
	result = not_op(or_result)

	return result
	
# XOR operation on bitstreams
def xor_op(bitstream1, bitstream2):
	result = numpy.zeros(0)

	for x in range(len(bitstream1)):
		bs1 = int(bitstream1[x])
		bs2 = int(bitstream2[x])
		bsr = bs1 ^ bs2
		result = numpy.append(result, bsr)

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
		if a == 1:
			result = result + 1

	return float(result) / float(len(bitstream))


# Unit tests
class bctTest(unittest.TestCase):
	def test_clockdiv(self):
		result = clockdiv(2, [1, 0, 0, 0], 2)
		numpy.testing.assert_equal(result, [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
		result = clockdiv(1, [1, 1, 1, 0], 2)
		numpy.testing.assert_equal(result, [1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0])
		result = clockdiv(2, [1, 0, 0, 1], 2)
		numpy.testing.assert_equal(result, [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1])
		result = clockdiv(2, [1, 0, 0, 1], 3)
		numpy.testing.assert_equal(result, [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1])

	def test_unary_SNG(self):
		result = unary_SNG(4, .75)
		numpy.testing.assert_equal(result, [1, 1, 1, 0])
		result = unary_SNG(8, .75)
		numpy.testing.assert_equal(result, [1, 1, 1, 1, 1, 1, 0, 0])
		result = unary_SNG(12, .75)
		numpy.testing.assert_equal(result, [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0])

		result = unary_SNG(4, .25)
		numpy.testing.assert_equal(result, [1, 0, 0, 0])
		result = unary_SNG(8, .25)
		numpy.testing.assert_equal(result, [1, 1, 0, 0, 0, 0, 0, 0])
		result = unary_SNG(12, .25)
		numpy.testing.assert_equal(result, [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0])

		result = unary_SNG(8, .125)
		numpy.testing.assert_equal(result, [1, 0, 0, 0, 0, 0, 0, 0])
		result = unary_SNG(16, .125)
		numpy.testing.assert_equal(result, [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
		result = unary_SNG(24, .125)
		numpy.testing.assert_equal(result, [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

	def test_rotate(self):
		result = rotate(1, [1, 0, 0, 0], 1)
		numpy.testing.assert_equal(result, [1, 0, 0, 0])
		result = rotate(1, [1, 0, 0, 0], 3)
		numpy.testing.assert_equal(result, [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0])
		result = rotate(2, [1, 0, 0, 0], 3)
		numpy.testing.assert_equal(result, [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1])


	def test_to_float(self):
		result = to_float([1, 0, 0, 0, 1, 0, 0, 1])
		self.assertEqual(result, 0.375)

	def test_not(self):
		result = not_op([1, 0, 0, 1, 0, 0])
		numpy.testing.assert_equal(result, [0, 1, 1, 0, 1, 1])

	def test_and(self):
		result = and_op([1, 0, 0], [0, 0, 1])
		numpy.testing.assert_equal(result, [0, 0, 0])

	def test_nand(self):
		result = nand_op([1, 0, 1], [0, 1, 1])
		numpy.testing.assert_equal(result, [1, 1, 0])

	def test_or(self):
		result = or_op([1, 1, 1], [0, 0, 1])
		numpy.testing.assert_equal(result, [1, 1, 1])
		
	def test_nor(self):
		result = nor_op([1, 1, 1], [0, 0, 1])
		numpy.testing.assert_equal(result, [0, 0, 0])

	def test_xor(self):
		result = xor_op([1, 0, 1], [0, 1, 1])
		numpy.testing.assert_equal(result, [1, 1, 0])

	def test_nxor(self):
		result = nxor_op([1, 0, 1], [0, 1, 1])
		numpy.testing.assert_equal(result, [0, 0, 1])
		
	def test_number_of_1(self):
		result = number_of_1([1, 0, 0, 0])
		self.assertEqual(result, 1)
		
	def test_number_of_0(self):
		result = number_of_0([1, 0, 0, 0])
		self.assertEqual(result, 3)
		
	def test_lfsr_sng(self):
		result = lfsr_SNG(8, 1, 0x42)
		print(result)

# perform unit testing if no parameters specified (e.g. python bct.py)
if __name__ == '__main__':
	unittest.main()
