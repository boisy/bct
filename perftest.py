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
	def XXXtest_multiply_five_8bitstreams(self):
		# Measure multiplication of five 8 bit streams (result is 8^5 bits long)
		accumulated_result = numpy.zeros(0)
		epsilon = .01

		n1 = bct.unary_SNG(4, 16, .25)
		n2 = bct.lfsr_SNG(4, 16, .25, 1, 3)
		n3 = bct.lfsr_SNG(4, 16, .5, 1, 3)
		n4 = bct.lfsr_SNG(4, 16, .5, 1, 3)
		n5 = bct.lfsr_SNG(4, 16, .25, 1, 3)

		for part in range(1, 17):
			cdn1 = numpy.zeros(0)
			cdn2 = numpy.zeros(0)
			cdn3 = numpy.zeros(0)
			cdn4 = numpy.zeros(0)
			cdn5 = numpy.zeros(0)
			for i in range(1, 5):
				cdn1.append(n1,  bct.clockdiv(1, n1, 5, i))
				cdn2.append(n2,  bct.clockdiv(1, n1, 5, i))
				cdn3.append(n3,  bct.clockdiv(1, n1, 5, i))
				cdn4.append(n4,  bct.clockdiv(1, n1, 5, i))
				cdn5.append(n5,  bct.clockdiv(1, n1, 5, i))

			n1Xn2 = bct.and_op(n1, n2)
			print("n1Xn2 = n1 x n2 = ", n1Xn2)
			n1Xn2Xn3 = bct.and_op(n1Xn2, n3)
			print("n1Xn2Xn3 = n1Xn2 x n3 = ", n1Xn2Xn3)
			n1Xn2Xn3Xn4 = bct.and_op(n1Xn2Xn3, n4)
			print("n1Xn2Xn3Xn4 = n1Xn2Xn3 x n4 = ", n1Xn2Xn3Xn4)
			n1Xn2Xn3Xn4Xn5 = bct.and_op(n1Xn2Xn3Xn4, n5)
			print("n1Xn2Xn3Xn4Xn5 = n1Xn2Xn3Xn4 x n5 = ", n1Xn2Xn3Xn4Xn5)
			end = time.time()
			print(end - start, 'seconds')

			accumulated_result = numpy.append(accumulated_result, n1Xn2Xn3Xn4Xn5)
			result_float = bct.to_float(accumulated_result)

			true_result = .25 * .25 * .5 * .5 * .25
			error = abs(result_float - true_result)
			print("true_result = ", true_result, ", result_float = ", result_float, ", error = ", error)
			if error < epsilon:
				print("result is within error.")
				return
		
#			self.assertEqual(result_float, .25 * .25 * .5 * .5 * .25)

	def test_multiply_two_4bitstreams(self):
		# Measure multiplication of two 16 bit streams (result is 16^2 bits long)
		accumulated_result = numpy.zeros(0)
		epsilon = .00000000

		term1 = .25
		term2 = .25
		n1 = bct.unary_SNG(4, 16, term1)
		n2 = bct.lfsr_SNG(4, 16, term2, 1, 1)

		print("n1 = ", n1, ", n2 = ", n2)

		cdn1 = numpy.zeros(0)
		cdn2 = numpy.zeros(0)

		for part in range(1, 9):
			major = 16 * (part - 1)
			for i in range(1, 17):
				offset = major + i
				print(offset)
				cdn1 = numpy.append(cdn1, bct.clockdiv_bit(1, n1, 2, offset))
				cdn2 = numpy.append(cdn2, bct.clockdiv_bit(1, n1, 2, offset))

			print("cdn1 = ", cdn1)
	
			print("cdn2 = ", cdn2)
	
			cdn1Xcdn2 = bct.and_op(cdn1, cdn2)
			print("cdn1Xcdn2 = cdn1 x cdn2 = ", cdn1Xcdn2)

			accumulated_result = numpy.append(accumulated_result, cdn1Xcdn2)
			result_float = bct.to_float(accumulated_result)

			true_result = term1 * term2
			error = abs(result_float - true_result)
			print("true_result = ", true_result, ", result_float = ", result_float, ", error = ", error)
			if error < epsilon:
				print("result is within error.")
				return
		
# perform unit testing if no parameters specified (e.g. python bct.py)
if __name__ == '__main__':
        unittest.main()
