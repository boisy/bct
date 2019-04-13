# Performance test
import time
from timeit import default_timer as timer
import unittest
import numpy
import coloredlogs, logging, sys
import re
import random

import bct

# Measure total simulation for (a) window-based method, and (b) total method
# Measure against different Mean Absolute Errors (MAEs)

# Use substreams to minimize the impact of the bitstreams on RAM, and at the same time, compute them piecemeal to see if they fall within our desired accuracy.
class bctTest(unittest.TestCase):
	filename = "results.csv"

	def test_main(self):
		logger = logging.getLogger(__name__)	
		coloredlogs.install(level=100)
		bctTest.filename = "results.csv"
		f = open(bctTest.filename, "w+")
		f.write("total time,terms,sngs,methods,precision,bitstream length,result length,segment length,mae,# of operations\n")
		f.close()

		terms = []
		precision = 4
		bitstream_length = pow(2, precision)
#		for i in range(5):
#			terms.append(random.randrange(1, bitstream_length - 1) / bitstream_length)
		terms = [0.4375, 0.8125, 0.5, 0.375]
#		terms = [0.75, 0.125, 0.75, 0.5, 0.625]
		bctTest.perfTest(self, precision, terms, 128)

	def perfTest(self, precision, terms, segment_length = 64):

		for mae in [0.0]:
			sngs = []
			methods = []
			term_count = len(terms)

			for i in range(term_count):
				sngs.append(bct.unary_SNG)
				methods.append(bct.clockdiv_bits)
#				methods.append(bct.rotate_bits)
			bctTest.multiply_test_segmented(self, terms, precision, sngs, methods, segment_length, mae)

			sngs = []
			methods = []
			for i in range(term_count):
				sngs.append(bct.unary_SNG)
				methods.append(bct.clockdiv)
#				methods.append(bct.rotate)
#			bctTest.multiply_test_conventional(self, terms, precision, sngs, methods, mae)

	def multiply_test_conventional(self, terms, precision, sngs, methods, mae = 0.0):
		logger = logging.getLogger(__name__)	
		bitstream_length = pow(2, precision)
		result_length = pow(bitstream_length, len(terms))
		run_loops = 1

		total_time = 0.0
		number_of_operations = 0

		time = bctTest.multiply_bitstreams_conventional(self, sngs, methods, terms, precision, bitstream_length, mae, run_loops)
		total_time = total_time + time
		number_of_operations = number_of_operations + 1
		logger.critical('total time = %f', total_time)

		f = open(bctTest.filename, "a+")

		sng_names = ""
		for s in sngs:
			sng_names = sng_names + s.__name__ + " "

		method_names = ""
		for s in methods:
			method_names = method_names + s.__name__ + " "

		terms_str = ""
		for t in terms:
			terms_str = terms_str + str(t) + " "
		f.write(str(total_time) + "," + terms_str + "," + sng_names + "," + method_names + "," + str(precision) + "," + str(bitstream_length) + "," + str(result_length) + "," + "," + str(mae) + "," + str(number_of_operations) + "\n")
		f.close()

	def multiply_test_segmented(self, terms, precision, sngs, methods, segment_length, mae = 0.0):
		logger = logging.getLogger(__name__)	
		bitstream_length = pow(2, precision)
		result_length = pow(bitstream_length, len(terms))
		run_loops = 1

		total_time = 0.0
		number_of_operations = 0

		time = bctTest.multiply_bitstreams_segmented(self, sngs, methods, terms, precision, bitstream_length, segment_length, mae, run_loops)
		total_time = total_time + time
		number_of_operations = number_of_operations + 1
		logger.critical('total time = %f', total_time)

		f = open(bctTest.filename, "a+")

		sng_names = ""
		for s in sngs:
			sng_names = sng_names + s.__name__ + " "

		method_names = ""
		for s in methods:
			method_names = method_names + s.__name__ + " "

		term_names = ""
		for t in terms:
			term_names = term_names + str(t) + " "

		f.write(str(total_time) + "," + term_names + "," + sng_names + "," + method_names + "," + str(precision) + "," + str(bitstream_length) + "," + str(result_length) + "," + str(segment_length) + "," + str(mae) + "," + str(number_of_operations) + "\n")
		f.close()

	def multiply_bitstreams_conventional(self, sngs, methods, terms, precision=4, bitstream_length=16, mae = 0.0, run_loops=10):
		logger = logging.getLogger(__name__)	
		logger.critical("Start of conventional multiplication of %s\n    %s SNGs\n    %s methods\n    %d-bit precision\n    %d-bitstream length\n    %d run loops\n    %f MAE", terms, sngs, methods, precision, bitstream_length, run_loops, mae)
		time = 0.0
		for j in range(0, run_loops):
			start = timer()
			self.multiply_conventional(sngs, methods, terms, precision, bitstream_length, mae)
			end = timer()
			time = time + (end - start)
		time = time / run_loops 
		logger.critical("End of conventional multiplication, time is %f seconds", time)		
		return time


	def multiply_bitstreams_segmented(self, sngs, methods, terms, precision=4, bitstream_length=16, segment_length=4, mae = 0.0, run_loops=10):
		logger = logging.getLogger(__name__)	
		logger.critical("Start of segemnted multiplication of %s\n    %d-bit precision\n    %d-bitstream length\n    %d-bit segment length\n    %d run loops", terms, precision, bitstream_length, segment_length, run_loops)
		time = 0.0
		for j in range(0, run_loops):
			start = timer()
			self.multiply_segmented(sngs, methods, terms, precision, bitstream_length, segment_length, mae)
			end = timer()
			time = time + (end - start)
		time = time / run_loops
		logger.critical("End of segmented multiplication, time is %f seconds", time)
		return time

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


	def multiply_segmented(self, sngs, methods, terms, precision, bitstream_length, segment_length = 0, mae = 0.0, debug = 0):
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
