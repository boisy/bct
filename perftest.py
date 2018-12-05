# Performance test
import time
import timeit
import unittest
import numpy

import bct

# Use substreams to minimize the impact of the bitstreams on RAM, and at the same time, compute them piecemeal to see if they fall within our desired accuracy.
class bctTest(unittest.TestCase):
	def test_multiply_n_bitstreams(self):
		terms = [.25, .5]
		encoded_terms = []
		number_of_terms = len(terms)
		true_result = 1.0
		for t in terms:
			true_result *= t

		accumulated_result = 0
		accumulated_result_length = 0
		epsilon = 0.0

		precision = 4
		bitstream_length = pow(2, precision)

		print("Multiply", number_of_terms, "terms:", terms)
		print("Precision =", precision, ", bitstream length =", bitstream_length)
		print("=====================================================")

		# use appropriate SNG for encoding floating point terms
		for i in range(number_of_terms):
			term = terms[i]
			if i == 0:
				encoded_terms.append(bct.unary_SNG(precision, bitstream_length, term))
			else:	
				encoded_terms.append(bct.lfsr_SNG(precision, bitstream_length, term))

	
		# compute 'segment_length' bits at a time
		segment_length = bitstream_length
		for segment in range(1, segment_length + 1):
			expanded_terms = []
			segment_start_bit = bitstream_length * (segment - 1)
			for j in range(number_of_terms):
				segment_offset = (segment - 1) * segment_length
				cdterm = bct.clockdiv_bits(j + 1, encoded_terms[j], number_of_terms, segment_offset, segment_length)
				expanded_terms.append(cdterm)
			result = numpy.ones(segment_length)
			for i in range(number_of_terms):
				print("term", i + 1, "=", expanded_terms[i])
				result = bct.and_op(result, expanded_terms[i])
			print("result =", result)

			accumulated_result = accumulated_result + bct.number_of_1(result)
			accumulated_result_length += bitstream_length
			result_float = accumulated_result / accumulated_result_length

			error = abs(result_float - true_result)
			print("True result = ", true_result, ", result_float = ", result_float, " (", accumulated_result, "/", accumulated_result_length, "), error = ", error)
			if error <= epsilon:
				print("result is within error after", accumulated_result_length, "bits (", int(accumulated_result_length / bitstream_length), "tries ).")
				return
			else:
				print("not accurate enough with", accumulated_result_length, "bits... try with", bitstream_length, "more bits.")




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
#				print(offset)
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
