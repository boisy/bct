# Performance test
import time
from timeit import default_timer as timer
import unittest
import numpy
import coloredlogs, logging, sys
import re

import bct

# Measure total simulation for (a) window-based method, and (b) total method
# Measure against different Mean Absolute Errors (MAEs)

# Use substreams to minimize the impact of the bitstreams on RAM, and at the same time, compute them piecemeal to see if they fall within our desired accuracy.
class bctTest(unittest.TestCase):
	def test_main(self):
		f = open("results.csv", "w+")
		f.write("total time,sngs,methods_conventional,methods_segmented,precision,bitstream length, segment length,mae,time (conventional),time (segmented),improvement\n")
		f.close()

		segment_length = 1
		for mae in [0.0]:
			precision = 8
			sngs = [bct.sobol_SNG, bct.sobol_SNG, bct.sobol_SNG]
			methods_conventional = [bct.rotate, bct.rotate, bct.rotate]
			methods_segmented = [bct.rotate_bits, bct.rotate_bits, bct.rotate_bits]
			bctTest.multiply_test_comprehensive_3_terms(self, precision, sngs, methods_conventional, methods_segmented, segment_length, mae)

	def multiply_test_comprehensive_2_terms(self, precision, sngs, methods_conventional, methods_segmented, segment_length = 4, mae = 0.0):
		logger = logging.getLogger(__name__)	
		bitstream_length = pow(2, precision)
		run_loops = 1

		total_segmented_time = 0.0
		total_conventional_time = 0.0

		for a in range(1, bitstream_length):
			for b in range(1, bitstream_length):
				term1 = float(a) / bitstream_length
				term2 = float(b) / bitstream_length
				times = bctTest.multiply_bitstreams(self, sngs, methods_conventional, methods_segmented, [term1, term2], precision, bitstream_length, segment_length, mae, run_loops)
				total_conventional_time = total_conventional_time + times[0]
				total_segmented_time = total_segmented_time + times[1]
				logger.critical('total conventional time = %f', total_conventional_time)
				logger.critical('total segmented time = %f', total_segmented_time)

		f = open("results.csv", "a+")

		sng_names = ""
		for s in sngs:
			sng_names = sng_names + s.__name__ + " "

		methods_conventional_names = ""
		for s in methods_conventional:
			methods_conventional_names = methods_conventional_names + s.__name__ + " "

		methods_segmented_names = ""
		for s in methods_segmented:
			methods_segmented_names = methods_segmented_names + s.__name__ + " "

		f.write(str(total_segmented_time + total_conventional_time) + "," + sng_names + "," + methods_conventional_names + "," + methods_segmented_names + "," + str(precision) + "," + str(bitstream_length) + "," + str(segment_length) + "," + str(mae) + "," + str(total_conventional_time) + "," + str(total_segmented_time) + "," + str((1 / (total_segmented_time / total_conventional_time))) + "\n")
		f.close()

	def multiply_test_comprehensive_3_terms(self, precision, sngs, methods_conventional, methods_segmented, segment_length = 4, mae = 0.0):
		logger = logging.getLogger(__name__)	
		bitstream_length = pow(2, precision)
		run_loops = 1

		total_segmented_time = 0.0
		total_conventional_time = 0.0

		for a in range(1, bitstream_length):
			for b in range(1, bitstream_length):
				for c in range(1, bitstream_length):
					term1 = float(a) / bitstream_length
					term2 = float(b) / bitstream_length
					term3 = float(c) / bitstream_length
					times = bctTest.multiply_bitstreams(self, sngs, methods_conventional, methods_segmented, [term1, term2, term3], precision, bitstream_length, segment_length, mae, run_loops)
					total_conventional_time = total_conventional_time + times[0]
					total_segmented_time = total_segmented_time + times[1]
					logger.critical('total conventional time = %f', total_conventional_time)
					logger.critical('total segmented time = %f', total_segmented_time)

		f = open("results.csv", "a+")

		sng_names = ""
		for s in sngs:
			sng_names = sng_names + s.__name__ + " "

		methods_conventional_names = ""
		for s in methods_conventional:
			methods_conventional_names = methods_conventional_names + s.__name__ + " "

		methods_segmented_names = ""
		for s in methods_segmented:
			methods_segmented_names = methods_segmented_names + s.__name__ + " "

		f.write(str(total_segmented_time + total_conventional_time) + "," + sng_names + "," + methods_conventional_names + "," + methods_segmented_names + "," + str(precision) + "," + str(bitstream_length) + "," + str(segment_length) + "," + str(mae) + "," + str(total_conventional_time) + "," + str(total_segmented_time) + "," + str((1 / (total_segmented_time / total_conventional_time))) + "\n")
		f.close()

	def multiply_bitstreams(self, sngs, methods_conventional, methods_segmented, terms, precision=4, bitstream_length=16, segment_length=4, mae = 0.0, run_loops=10):
		logger = logging.getLogger(__name__)	
		coloredlogs.install(level=100)
#		coloredlogs.install(level='CRITICAL')
		logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

		logger.critical("Start of segmented multiplication of %s\n    %s SNGs\n    %s methods\n    %d-bit precision\n    %d-bitstream length\n    %d-bit segment length\n    %d run loops\n    %f MAE", terms, sngs, methods_segmented, precision, bitstream_length, segment_length, run_loops, mae)
		segmented_time = 0.0
		for j in range(0, run_loops):
			start = timer()
			self.multiply(sngs, methods_segmented, terms, precision, bitstream_length, segment_length, mae)
			end = timer()
			segmented_time = segmented_time + (end - start)
		segmented_time = segmented_time / run_loops 
		logger.critical("End of segmented multiplication, time is %f seconds", segmented_time)		


		logger.critical("Start of conventional multiplication of %s\n    %d-bit precision\n    %d-bitstream length\n    %d-bit segment length\n    %d run loops", terms, precision, bitstream_length, segment_length, run_loops)
		start = timer()
		self.multiply_conventional(sngs, methods_conventional, terms, precision, bitstream_length, mae)
		end = timer()
		conventional_time = end - start
		logger.critical("End of conventional multiplication, time is %f seconds", conventional_time)
		logger.critical("Segmented multiplication is %.2fX faster", 1 / (conventional_time / segmented_time))
		return (conventional_time, segmented_time)

	def multiply_conventional(self, sngs, methods, terms, precision, bitstream_length, mae = 0.0, debug = 0):
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


	def multiply(self, sngs, methods, terms, precision, bitstream_length, segment_length = 0, mae = 0.0, debug = 0):
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

			if mae != 0.0:
				error = abs(result_float - true_result)
				logger.info("True result = %f, result_float = %f (%d/%d), error = %f", true_result, result_float, accumulated_result, accumulated_result_length, error)
				if error <= mae:
					logger.error("True result = %f, result_float = %f (%d/%d), error = %f", true_result, result_float, accumulated_result, accumulated_result_length, error)
					logger.error("result is within error after %d bits (%d steps)", accumulated_result_length, int(accumulated_result_length / segment_length))
					return
				else:
					logger.error("not accurate enough with %d bits", accumulated_result_length)


# perform unit testing if no parameters specified (e.g. python bct.py)
if __name__ == '__main__':
        unittest.main()
