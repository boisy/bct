# Performance test
import time
from timeit import default_timer as timer
import unittest
import numpy
import coloredlogs, logging, sys

import bct

# Measure total simulation for (a) window-based method, and (b) total method
# Measure against different epsilons

# Use substreams to minimize the impact of the bitstreams on RAM, and at the same time, compute them piecemeal to see if they fall within our desired accuracy.
class bctTest(unittest.TestCase):
	def test_main(self):
		bctTest.multiply_test_comprehensive(self)

	def multiply_test_1(self):
		precision = 6
		bitstream_length = pow(2, precision)
		run_loop = 1
		term1 = (bitstream_length - 1) / bitstream_length
		term2 = (bitstream_length - 1) / bitstream_length
		bctTest.multiply_bitstreams(self, bct.clockdiv, bct.clockdiv_bits, [term1, term2], precision, bitstream_length, 128, run_loop)

		term1 = 1.0 / bitstream_length
		term2 = 1.0 / bitstream_length
		bctTest.multiply_bitstreams(self, bct.clockdiv, bct.clockdiv_bits, [term1, term2], precision, bitstream_length, 128, run_loop)

	def multiply_test_comprehensive(self):
		logger = logging.getLogger(__name__)	
		precision = 7
		bitstream_length = pow(2, precision)
		run_loop = 1
		sngs = [bct.unary_SNG, bct.unary_SNG]
		methods_non_opt = [bct.rotate, bct.rotate]
		methods_opt = [bct.rotate_bits, bct.rotate_bits]

		total_optimized_time = 0.0
		total_non_optimized_time = 0.0

		for a in range(1, bitstream_length):
			for b in range(a, bitstream_length):
				term1 = a / bitstream_length
				term2 = b / bitstream_length
				times = bctTest.multiply_bitstreams(self, sngs, methods_non_opt, methods_opt, [term1, term2], precision, bitstream_length, 128, run_loop)
				total_non_optimized_time = total_non_optimized_time + times[0]
				total_optimized_time = total_optimized_time + times[1]
				logger.critical('total non-optimized time = %f', total_non_optimized_time)
				logger.critical('total optimized time = %f', total_optimized_time)

	def multiply_bitstreams(self, sngs, methods_non_opt, methods_opt, terms, precision=4, bitstream_length=16, segment_length=4, run_loops=10):
		logger = logging.getLogger(__name__)	
		coloredlogs.install(level='CRITICAL')
		logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

		logger.critical("Start of optimized multiplication of %s\n    %s SNGs\n    %s methods\n    %d-bit precision\n    %d-bitstream length\n    %d-bit segment length\n    %d run loops", terms, sngs, methods_opt, precision, bitstream_length, segment_length, run_loops)
		optimized_time = 0.0
		for j in range(0, run_loops):
			start = timer()
			self.multiply(sngs, methods_opt, terms, precision, bitstream_length, segment_length, 0.0)
			end = timer()
			optimized_time = optimized_time + (end - start)
		optimized_time = optimized_time / run_loops 
		logger.critical("End of optimized multiplication, time is %f seconds", optimized_time)		


		logger.critical("Start of non-optimized multiplication of %s\n    %d-bit precision\n    %d-bitstream length\n    %d-bit segment length\n    %d run loops", terms, precision, bitstream_length, segment_length, run_loops)
		start = timer()
		self.multiply_non_opt(sngs, methods_non_opt, terms, precision, bitstream_length)
		end = timer()
		non_optimized_time = end - start
		logger.critical("End of non-optimized multiplication, time is %f seconds", non_optimized_time)
		logger.critical("Optimized multiplication is %.2fX faster", non_optimized_time / optimized_time)
		return (non_optimized_time, optimized_time)

	def multiply_non_opt(self, sngs, methods, terms, precision, bitstream_length, epsilon = 0.0, debug = 0):
		logger = logging.getLogger(__name__)	
		encoded_terms = []
		number_of_terms = len(terms)
		final_bitstream_length = pow(bitstream_length, number_of_terms)
		true_result = 1.0
		for t in terms:
			true_result *= t

		# use appropriate SNG for encoding floating point terms
		for i in range(number_of_terms):
			term = terms[i]
			s = sngs[i]
			encoded_term = s(precision, bitstream_length, term)
			m = methods[i]
			t = m(i + 1, encoded_term, number_of_terms)
			encoded_terms.append(t)

		result = numpy.ones(final_bitstream_length)
		for j in range(number_of_terms):
			result = bct.and_op(result, encoded_terms[j])

		num_1s = bct.number_of_1(result)
		result_float = num_1s / final_bitstream_length
		error = abs(result_float - true_result)
		logger.error("True result = %f, result_float = %f (%d/%d), error = %f", true_result, result_float, num_1s, final_bitstream_length, error)


	def multiply(self, sngs, methods, terms, precision, bitstream_length, segment_length = 0, epsilon = 0.0, debug = 0):
		logger = logging.getLogger(__name__)
		encoded_terms = []
		number_of_terms = len(terms)
		final_bitstream_length = pow(bitstream_length, number_of_terms)
		true_result = 1.0
		for t in terms:
			true_result *= t

		accumulated_result = 0
		accumulated_result_length = 0

		logger.info("Multiply %d terms: %s", number_of_terms, terms)
		logger.info("Methods = %s, precision = %d, bitstream length = %d, total length = %d", methods, precision, bitstream_length, final_bitstream_length)
		logger.info("=====================================================")

		# use appropriate SNG for encoding floating point terms
		for i in range(number_of_terms):
			term = terms[i]
			s = sngs[i]
			encoded_terms.append(s(precision, bitstream_length, term))
	
		# if 0, compute 'segment_length' bits at a time
		if (segment_length == 0):
			segment_length = bitstream_length

		count = int(final_bitstream_length / segment_length)
		for segment in range(1, count + 1):
			expanded_terms = []
			segment_start_bit = segment_length * segment
			for j in range(number_of_terms):
				segment_offset = (segment - 1) * segment_length + 1
				m = methods[j]
				cdterm = m(j + 1, encoded_terms[j], number_of_terms, segment_offset, segment_length)
				expanded_terms.append(cdterm)
			result = numpy.ones(segment_length)
			for i in range(number_of_terms):
				logger.debug("term %d = %s", i + 1, expanded_terms[i])
				result = bct.and_op(result, expanded_terms[i])
			logger.debug("result = %s", result)

			accumulated_result = accumulated_result + bct.number_of_1(result)
			accumulated_result_length += segment_length
			result_float = accumulated_result / accumulated_result_length

			error = abs(result_float - true_result)
			logger.info("True result = %f, result_float = %f (%d/%d), error = %f", true_result, result_float, accumulated_result, accumulated_result_length, error)
			if error <= epsilon:
				logger.error("True result = %f, result_float = %f (%d/%d), error = %f", true_result, result_float, accumulated_result, accumulated_result_length, error)
				logger.error("result is within error after %d bits (%d steps)", accumulated_result_length, int(accumulated_result_length / segment_length))
				return
			else:
				logger.error("not accurate enough with %d bits", accumulated_result_length)




	def XXXtest_multiply_two_bitstreams(self):
		# Measure multiplication of two bit streams
		accumulated_result = 0
		accumulated_result_length = 0
		epsilon = 0.0

		precision = 4
		bitstream_length = pow(2, precision)

		term1 = .5
		term2 = .5
		true_result = term1 * term2
		n1 = bct.unary_SNG(precision, bitstream_length, term1)
		n2 = bct.lfsr_SNG(precision, bitstream_length, term2)

		print("Multiply ", n1, "by", n2)
		print("True result is", true_result)
		print("=====================================================")

		for part in range(1, bitstream_length + 1):
			cdn1 = numpy.zeros(0)
			cdn2 = numpy.zeros(0)
			major = bitstream_length * (part - 1)
			for i in range(1, bitstream_length + 1):
				offset = major + i
				cdn1 = numpy.append(cdn1, bct.clockdiv_bit(1, n1, 2, offset))
				cdn2 = numpy.append(cdn2, bct.clockdiv_bit(2, n2, 2, offset))

			print("term 1 =", cdn1)
			print("term 2 =", cdn2)
	
			cdn1Xcdn2 = bct.and_op(cdn1, cdn2)
			print("term 1 X term 2 =", cdn1Xcdn2)

			accumulated_result = accumulated_result + bct.number_of_1(cdn1Xcdn2)
			accumulated_result_length += bitstream_length
			result_float = accumulated_result / accumulated_result_length

			error = abs(result_float - true_result)
			print("true_result = ", true_result, ", result_float = ", result_float, ", error = ", error)
			if error <= epsilon:
				print("result is within error after", accumulated_result_length, "bits.")
				return
			else:
				print("not accurate enough... try with", bitstream_length, "more bits.")
	
		
# perform unit testing if no parameters specified (e.g. python bct.py)
if __name__ == '__main__':
        unittest.main()
