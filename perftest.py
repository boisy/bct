# Performance test
import multiprocessing as mp
import time
import timeit
import unittest

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
	def test_multiply(self):
# Measure multiplication of five 8 bit streams (result is 8^5 bits long)
		start = time.time()
		n1 = bct.unary_SNG(4, 16, .25)
		end = time.time()
		print("n1 = bct.unary_SNG : ", end - start, 'seconds')

		start = time.time()
		n2 = bct.lfsr_SNG(4, 16, .25, 1, 3)
		end = time.time()
		print("n2 = bct.lfsr_SNG : ", end - start, 'seconds')

		start = time.time()
		n3 = bct.lfsr_SNG(4, 16, .5, 1, 3)
		end = time.time()
		print("n3 = bct.lfsr_SNG : ", end - start, 'seconds')

		start = time.time()
		n4 = bct.lfsr_SNG(4, 16, .5, 1, 3)
		end = time.time()
		print("n4 = bct.lfsr_SNG : ", end - start, 'seconds')

		start = time.time()
		n5 = bct.lfsr_SNG(4, 16, .25, 1, 3)
		end = time.time()
		print("n5 = bct.lfsr_SNG : ", end - start, 'seconds')

		start = time.time()
		n1 = bct.clockdiv(1, n1, 5)
		end = time.time()
		print("n1 = bct.clockdiv : ", end - start, 'seconds')

		start = time.time()
		n2 = bct.clockdiv(2, n2, 5)
		end = time.time()
		print("n2 = bct.clockdiv : ", end - start, 'seconds')

		start = time.time()
		n3 = bct.clockdiv(3, n3, 5)
		end = time.time()
		print("n3 = bct.clockdiv : ", end - start, 'seconds')

		start = time.time()
		n4 = bct.clockdiv(4, n4, 5)
		end = time.time()
		print("n4 = bct.clockdiv : ", end - start, 'seconds')

		start = time.time()
		n5 = bct.clockdiv(5, n5, 5)
		end = time.time()
		print("n5 = bct.clockdiv : ", end - start, 'seconds')

		print("n1Xn2 = n1 x n2")
		n1Xn2 = bct.and_op(n1, n2)
		print("n1Xn2Xn3 = n1Xn2 x n3")
		n1Xn2Xn3 = bct.and_op(n1Xn2, n3)
		print("n1Xn2Xn3Xn4 = n1Xn2Xn3 x n4")
		n1Xn2Xn3Xn4 = bct.and_op(n1Xn2Xn3, n4)
		print("n1Xn2Xn3Xn4Xn5 = n1Xn2Xn3Xn4 x n5")
		n1Xn2Xn3Xn4Xn5 = bct.and_op(n1Xn2Xn3Xn4, n5)
		end = time.time()
		result_float = bct.to_float(n1Xn2Xn3Xn4Xn5)
		print(end - start, 'seconds')
		self.assertEqual(result_float, .25 * .25 * .5 * .5)

	def test_multiply_parallel(self):
		output = mp.Queue()
		start = time.time()
		n1 = bct.unary_SNG(4, 16, .25)
		n2 = bct.lfsr_SNG(4, 16, .25, 1, 3)
		n3 = bct.lfsr_SNG(4, 16, .5, 1, 3)
		n4 = bct.lfsr_SNG(4, 16, .5, 1, 3)
		n1 = bct.clockdiv(1, n1, 4)
		n2 = bct.clockdiv(2, n2, 4)
		n3 = bct.clockdiv(3, n3, 4)
		n4 = bct.clockdiv(4, n4, 4)
#		processes = [mp.Process(target=multiply, args=(n1, n2)) for x in range(2)]
		processes = []
		t = mp.Process(target=multiply, args=(n1, n2))
		processes.append(t)
		t = mp.Process(target=multiply, args=(n3, n4))
		processes.append(t)
		for p in processes:
			p.start()

		# Exit the completed processes
		for p in processes:
			p.join()

		# Get process results from the output queue
#		results = [output.get() for p in processes]

		for p in processes:
			p.print()
		end = time.time()
		print(end - start, 'seconds')


# perform unit testing if no parameters specified (e.g. python bct.py)
if __name__ == '__main__':
        unittest.main()
