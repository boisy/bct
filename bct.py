# Bitstream Computation Toolkit
#
# Authors: Boisy G. Pitre, Dr. M. Hassan Najafi
# Computer Science Department
# University of Louisiana at Lafayette
# Lafayette, Louisiana

import numpy
import random
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
#  precision: bit width
#  stream_length: length, in bits, of the desired output bitstream
#  input_number_float: the floating point number (0 <= n < 1) to represent as a bitstream
def lfsr_SNG(precision, stream_length, input_number_float, position_in_tap_file = 0, seed = 0):
	result = numpy.zeros(0)

	# call lfsr_RNG
	maximal_period_array = lfsr_RNG(precision, 0, 0)
	ln = pow(2, precision)
	v = input_number_float * ln
	for n in maximal_period_array:
		if n < v:
			result = numpy.append(result, 1)
		else:
			result = numpy.append(result, 0)
			
	return result

# LFSR Random Number Generator
#  precision: bit width
#  position_in_tap_file: position in tap file
#  seed = starting value
# NOTE: we are adding 0 at the beginning of the result to keep the size correct
def lfsr_RNG(precision, position_in_tap_file, seed):
	if position_in_tap_file == 0:
		if precision == 4:
				position_in_tap_file = random.randrange(1, 2)
		if precision == 5:
				position_in_tap_file = random.randrange(1, 6)
		if precision == 8:
				position_in_tap_file = random.randrange(1, 16)
		if precision == 12:
				position_in_tap_file = random.randrange(1, 144)
		if precision == 16:
				position_in_tap_file = random.randrange(1, 2048)

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

	if seed == 0:
		# choose a random number
		seed = random.randrange(1, pow(2,precision) - 1)

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

	result = [0]

	for t in range(pow(2, precision) - 1):
		v = L.runKCycle(precision)
		# convert v to int
		value = 0
		for i in range(len(v)):
			if v[i] == 1:
				value = value + pow(2, precision - i - 1)
		result.append(value)

	# return maximal period array
	return result


# Unary bitstream generator
# Added Oct 03 2018
#
# Parameters:
#  precision: bit width
#  stream_length: length, in bits, of the desired output bitstream
#  input_number_float: the floating point number (0 <= n < 1) to represent as a bitstream
#
def unary_SNG(precision, stream_length, input_number_float):
	result = numpy.zeros(0)
	compare2 = input_number_float * pow(2,precision)
	for counter in range(stream_length):
		compare1 = counter
		if compare1 < compare2:
			result = numpy.append(result, 1)
		else:
			result = numpy.append(result, 0)
	return result

# Clock division method that returns one bit
# This method returns the bit (0 or 1) at position 'offset' (1 <= pos <= pow(len(bitstream), total_inputs))
def clockdiv_bit(order, bitstream, total_inputs, offset):
	total_length = pow(len(bitstream), total_inputs)
	# check if offset is valid
	if (offset < 1 or offset > total_length):
		raise Exception('Out of range')
	# determine repeat count
	repeat = pow(len(bitstream), order - 1)
	bit_offset = int((offset - 1) / repeat)
	bit_offset = bit_offset % len(bitstream)
	return bitstream[bit_offset]

def clockdiv_bits(order, bitstream, total_inputs, offset, length):
	result = numpy.zeros(0)
	for i in range(offset, offset + length):
		result = numpy.append(result, clockdiv_bit(order, bitstream, total_inputs, i))
	return result	

# Clock division method
# This method returns the clock divided bitstream based on its order and total inputs
#   order: the order of the operation (1, 2, 3, ...)
#   bitstream: the bitstream to clock divide
#   total_inputs: the total number of inputs in the operation
def clockdiv(order, bitstream, total_inputs):
	entire_length = pow(len(bitstream), total_inputs)
	return clockdiv_bits(order, bitstream, total_inputs, 1, entire_length)

# Rotation method that returns one bit
# This method returns the bit (0 or 1) at position 'offset' (1 <= pos <= pow(len(bitstream), total_inputs))
# Notes:
# - length of bitstream impacts rotation frequency
#   e.g. rotate(2, [1, 0], 3) -> array([1., 0., 0., 1., 1., 0., 0., 1.])
def rotate_bit(order, bitstream, total_inputs, offset):
	# concrete example: order = 2, bitstream = [1, 0, 1, 1], so  group size = 4^(2-1):
	# after group 0, last bit (1) repeats in first bit of group 1, offset = 1 / 4
	# after group 1, next to last bit (1) repeats in first bit of group 2, offset = 2 / 4
	# after group 2, next to next to last bit (0) repeats in first bit of group 3, offset = 3 / 4
	# after group 3, next to next to next to last (1) bit repeats in first bit of group 4, offset = 4 / 4
	# and so on... 
	# ((offset - 1) / group size) = group (0 based)
	# ((offset - 1) % group size) = bit in group (0 based)
	# 
	
	total_length = pow(len(bitstream), total_inputs)

	# check if offset is valid
	if (offset < 1 or offset > total_length):
		raise Exception('Out of range')

	group_size = pow(len(bitstream), order - 1)
	if (group_size == 1):
		group = 0
	else:
		group = int((offset - 1) / group_size)

	bit_to_return = ((offset - 1) - group) % len(bitstream)

	return bitstream[bit_to_return]

def rotate_bits(order, bitstream, total_inputs, offset, length):
	result = numpy.zeros(0)
	for i in range(offset, offset + length):
		result = numpy.append(result, rotate_bit(order, bitstream, total_inputs, i))
	return result	

def rotate(order, bitstream, total_inputs):
	entire_length = pow(len(bitstream), total_inputs)
	return rotate_bits(order, bitstream, total_inputs, 1, entire_length)

# Rotate the passed bitstream
#
# e.g. rotate(1, [1, 0], 1) -> array([1., 0.])
# e.g. rotate(1, [1, 0], 2) -> array([1., 0., 1., 0.])
# e.g. rotate(2, [1, 0], 2) -> array([1., 0., 0., 1.])
# e.g. rotate(1, [1, 0], 3) -> array([1., 0., 1., 0., 1., 0., 1., 0.])
# e.g. rotate(2, [1, 0], 3) -> array([1., 0., 0., 1., 1., 0., 0., 1.])
# e.g. rotate(3, [1, 0], 3) -> array([1., 0., 1., 0., 0., 1., 0., 1.])
# e.g. rotate(3, [1, 0], 4) -> array([1., 0., 1., 0.,  0., 1., 0., 1.,  1., 0., 1., 0.,  0., 1., 0., 1.])
def rotate_suboptimal(order, bitstream, total_inputs):
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
# Added Nov 14 2018
def relatively_prime_bit(bitstream, entire_length, offset):
	number_of_repeats = int(entire_length / len(bitstream))
	if (offset < 1 or offset > number_of_repeats * len(bitstream)):
		raise Exception('Out of range')
	bit_to_return = (offset - 1) % len(bitstream)

	return bitstream[bit_to_return]

def relatively_prime_bits(bitstream, entire_length, offset, length):
	result = numpy.zeros(0)
	for i in range(offset, offset + length):
		result = numpy.append(result, relatively_prime_bit(bitstream, entire_length, i))
	return result	

def relatively_prime(bitstream, entire_length):
	number_of_repeats = int(entire_length / len(bitstream))
	return relatively_prime_bits(bitstream, entire_length, 1, number_of_repeats * len(bitstream))

def relatively_prime_suboptimal(bitstream, entire_length):
	result = numpy.zeros(0)
	number_of_repeats = entire_length / len(bitstream)
	for x in range(int(number_of_repeats)):
		result = numpy.append(result, bitstream)

	return result

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
		result = clockdiv(3, [1, 0], 3)
		numpy.testing.assert_equal(result, [1, 1, 1, 1, 0, 0, 0, 0])
		result = clockdiv(2, [1, 0], 3)
		numpy.testing.assert_equal(result, [1, 1, 0, 0, 1, 1, 0, 0])
		result = clockdiv(1, [1, 0], 3)
		numpy.testing.assert_equal(result, [1, 0, 1, 0, 1, 0, 1, 0])
		result = clockdiv(1, [1, 1, 1, 0], 2)
		numpy.testing.assert_equal(result, [1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0])
		result = clockdiv(2, [1, 1, 1, 0], 2)
		numpy.testing.assert_equal(result, [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0])
		result = clockdiv(2, [1, 0, 0, 1], 2)
		numpy.testing.assert_equal(result, [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1])
		result = clockdiv(1, [1, 0, 0, 1], 3)
		numpy.testing.assert_equal(result, [
		1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1,
		1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1,
		1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1,
		1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1,
		])
		result = clockdiv(2, [1, 0, 0, 1], 3)
		numpy.testing.assert_equal(result, [
		1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1,
		1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1,
		1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1,
		1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1
		])
		result = clockdiv(3, [1, 0, 0, 1], 3)
		numpy.testing.assert_equal(result, [
		1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
		0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
		0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
		1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
		])
		result = clockdiv(1, [1, 0], 3)
		numpy.testing.assert_equal(result, [1, 0, 1, 0, 1, 0, 1, 0])
		result = clockdiv(2, [1, 0], 3)
		numpy.testing.assert_equal(result, [1, 1, 0, 0, 1, 1, 0, 0])
		result = clockdiv(3, [1, 0], 3)
		numpy.testing.assert_equal(result, [1, 1, 1, 1, 0, 0, 0, 0])

	def test_multiply(self):
		# multiply .25 * .25
		n1 = unary_SNG(4, 16, .25)
		n2 = lfsr_SNG(4, 16, .25, 1, 3)
		n1 = clockdiv(1, n1, 2)
		n2 = clockdiv(2, n2, 2)
		result = and_op(n1, n2)
		result_float = to_float(result)
		self.assertEqual(result_float, 0.25 * 0.25)

		# multiply .25 * .25
		n1 = unary_SNG(4, 16, .25)
		n2 = lfsr_SNG(4, 16, .25, 1, 3)
		n1 = clockdiv(1, n1, 2)
		n2 = rotate(2, n2, 2)
		result = and_op(n1, n2)
		result_float = to_float(result)
		self.assertEqual(result_float, 0.25 * 0.25)

		# multiply .5 * .25
		n1 = unary_SNG(4, 16, .5)
		n2 = lfsr_SNG(4, 16, .25, 1, 3)
		n1 = clockdiv(1, n1, 2)
		n2 = rotate(2, n2, 2)
		result = and_op(n1, n2)
		result_float = to_float(result)
		self.assertEqual(result_float, .5 * .25)

		# multiply .5 * .25
		n1 = unary_SNG(4, 16, .5)
		n2 = lfsr_SNG(4, 16, .25, 1, 3)
		n1 = rotate(1, n1, 2)
		n2 = rotate(2, n2, 2)
		result = and_op(n1, n2)
		result_float = to_float(result)
		self.assertEqual(result_float, .5 * .25)

	def test_unary_SNG(self):
		result = unary_SNG(4, 16, .75)
		numpy.testing.assert_equal(result, [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0])
		result = unary_SNG(8, 256, .75)
		numpy.testing.assert_equal(result, [
		1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
		1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
		1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
		1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
		1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
		1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
		1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
		1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
		1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
		1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
		1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
		1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
		0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
		0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
		0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
		0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
		])

		result = unary_SNG(4, 16, .25)
		numpy.testing.assert_equal(result, [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
		result = unary_SNG(8, 256, .25)
		numpy.testing.assert_equal(result, [
		1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
		1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
		1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
		1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
		0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
		0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
		0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
		0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
		0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
		0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
		0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
		0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
		0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
		0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
		0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
		0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
		])

		result = unary_SNG(8, 256, .125)
		numpy.testing.assert_equal(result, [
		1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
		1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
		0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
		0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
		0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
		0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
		0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
		0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
		0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
		0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
		0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
		0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
		0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
		0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
		0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
		0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
		])

	def test_rotate(self):
		result = rotate(1, [1, 0, 0, 0], 1)
		numpy.testing.assert_equal(result, [1, 0, 0, 0])
		result = rotate(1, [1, 0, 0, 0], 3)
		numpy.testing.assert_equal(result, [
		1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0,
		1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0,
		1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0,
		1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0
		])
		result = rotate(2, [1, 0, 0, 0], 3)
		numpy.testing.assert_equal(result, [
		1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1,
		1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1,
		1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1,
		1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1])


	def test_relatively_prime(self):
		result = relatively_prime([1, 0, 0, 0], 12)
		numpy.testing.assert_equal(result, [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0])
		result = relatively_prime([1, 1, 0], 12)
		numpy.testing.assert_equal(result, [1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0])

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
		result = lfsr_SNG(8, 16, .25)

# perform unit testing if no parameters specified (e.g. python bct.py)
if __name__ == '__main__':
	unittest.main()
