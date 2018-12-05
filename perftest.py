# Performance test
import time
import timeit
import unittest
import numpy

import bct
import clockdiv as cd

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
	def test_multiply_five_8bitstreams(self):
		# Measure multiplication of five 8 bit streams (result is 8^5 bits long)
		accumulated_result = numpy.zeros(0)
		epsilon = .01

		n1 = bct.unary_SNG(4, 16, .25)
		n2 = bct.lfsr_SNG(4, 16, .25, 1, 3)
		n3 = bct.lfsr_SNG(4, 16, .5, 1, 3)
		n4 = bct.lfsr_SNG(4, 16, .5, 1, 3)
		n5 = bct.lfsr_SNG(4, 16, .25, 1, 3)

		cdn1 = cd.clockdiv(1, n1, 5)
		print(cdn1.info())
		cdn2 = cd.clockdiv(2, n2, 5)
		print(cdn2.info())
		cdn3 = cd.clockdiv(3, n3, 5)
		print(cdn3.info())
		cdn4 = cd.clockdiv(4, n4, 5)
		print(cdn4.info())
		cdn5 = cd.clockdiv(5, n5, 5)
		print(cdn5.info())

		for part in range(1, 17):
			start = time.time()
			end = time.time()
			n1 = cdn1.pulse(part)
			print("n1 = cd.clockdiv : ", end - start, 'seconds, n1 =', n1, ', len(n1) =', len(cdn1))
	
			start = time.time()
			n2 = cdn2.pulse(part)
			end = time.time()
			print("n2 = cd.clockdiv : ", end - start, 'seconds, n2 =', n2, ', len(n2) =', len(cdn2))
	
			start = time.time()
			n3 = cdn3.pulse(part)
			end = time.time()
			print("n3 = cd.clockdiv : ", end - start, 'seconds, n3 =', n3, ', len(n3) =', len(cdn3))
	
			start = time.time()
			n4 = cdn4.pulse(part)
			end = time.time()
			print("n4 = cd.clockdiv : ", end - start, 'seconds, n4 =', n4, ', len(n4) =', len(cdn4))
	
			start = time.time()
			n5 = cdn5.pulse(part)
			end = time.time()
			print("n5 = cd.clockdiv : ", end - start, 'seconds, n5 =', n5, ', len(n5) =', len(cdn5))

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
		# Measure multiplication of two 4 bit streams (result is 4^2 bits long)
		accumulated_result = numpy.zeros(0)
		epsilon = .00000001

		term1 = .25
		term2 = .25
		n1 = bct.unary_SNG(4, 16, term1)
		n2 = bct.lfsr_SNG(4, 16, term2, 1, 1)

		print("n1 = ", n1, ", n2 = ", n2)

		cdn1 = cd.clockdiv_part(1, n1, 2)
		cdn2 = cd.clockdiv_part(2, n2, 2)

		for part in range(1, 15):
			n1 = cdn1.pulse(part)
			print("n1 = ", n1)
	
			n2 = cdn2.pulse(part)
			print("n2 = ", n2)
	
			n1Xn2 = cd.and_op(n1, n2)
			print("n1Xn2 = n1 x n2 = ", n1Xn2)

			accumulated_result = numpy.append(accumulated_result, n1Xn2)
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
