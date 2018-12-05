# Performance test
import time
import timeit
import unittest
import numpy

import bct

#iterations = 10000
#for n in range(1, iterations):
#	n1 = bct.unary_SNG(4, 16, .5)

#end = time.time()
#print(iterations, "X -- unary_SNG(4, 16, .5) =", end - start)

#start = time.time()

#iterations = 1000
#for n in range(1, iterations):
#	n1 = bct.lfsr_SNG(4, 16, .5)

#end = time.time()
#print(iterations, "X -- unary_SNG(4, 16, .5) =", end - start)


def multiply(n1, n2):
	result = bct.and_op(n1, n2)
	return result

# Pass 1
# 1110 
# 0101

# Pass 2 - AND and check result
# 1110 1110 1110 1110
# 0000 1111 0000 1111 
# ------------------- <- AND
# 0000 1110 0000 1110 <- evaluate in chunks step by step (0/0, 3/8, 3/12, 6/16)

# Use substreams to minimize the impact of the bitstreams on RAM, and at the same time, compute them piecemeal to see if they fall within our desired accuracy.
 

class bctTest(unittest.TestCase):
	def test_multiply_two_bitstreams(self):
		# Measure multiplication of two bit streams
		accumulated_result = 0
		accumulated_result_length = 0
		epsilon = 0.0

		precision = 4
		bitstream_length = pow(2, precision)

		term1 = .5
		term2 = .5
		n1 = bct.unary_SNG(precision, bitstream_length, term1)
		n2 = bct.lfsr_SNG(precision, bitstream_length, term2)

		print("n1 = ", n1, ", n2 = ", n2)

		for part in range(1, bitstream_length + 1):
			cdn1 = numpy.zeros(0)
			cdn2 = numpy.zeros(0)
			major = bitstream_length * (part - 1)
			for i in range(1, bitstream_length + 1):
				offset = major + i
				print(offset)
				cdn1 = numpy.append(cdn1, bct.clockdiv_bit(1, n1, 2, offset))
				cdn2 = numpy.append(cdn2, bct.clockdiv_bit(2, n2, 2, offset))

			print("cdn1 = ", cdn1)
			print("cdn2 = ", cdn2)
	
			cdn1Xcdn2 = bct.and_op(cdn1, cdn2)
			print("cdn1Xcdn2 = cdn1 x cdn2 = ", cdn1Xcdn2)

			accumulated_result = accumulated_result + bct.number_of_1(cdn1Xcdn2)
			accumulated_result_length += bitstream_length
			result_float = accumulated_result / accumulated_result_length

			true_result = term1 * term2
			error = abs(result_float - true_result)
			print("true_result = ", true_result, ", result_float = ", result_float, ", error = ", error)
			if error <= epsilon:
				print("result is within error.")
				return
		
# perform unit testing if no parameters specified (e.g. python bct.py)
if __name__ == '__main__':
        unittest.main()
