import numpy
import bct

# Parameters:
# value: 0 <= n < 1
# BGM: bitstream generation method
# degree: number of terms
# precision: number of bits
# coefficients: numpy array with 'degree' values
def gamma(value, BGM, SNG, degree, precision, stream_length, coefficients):
	# convert coefficients to bitstreams
	coefficients_encoded = numpy.array([])
	for i in range(len(coefficients)):
		a = SNG(precision, stream_length, coefficients[i])
		x = BGM(i + 1, a, degree + 1)
		if len(coefficients_encoded) == 0:
			coefficients_encoded = x
		else:
			coefficients_encoded = numpy.vstack((coefficients_encoded, x))

	# add value to each coefficient
	total = numpy.zeros(pow(stream_length, degree))
	for i in range(degree):
		a = SNG(precision, stream_length, value)
		x = BGM(i + 1, a, degree)
		total = numpy.add(total, x)

	result = numpy.zeros(0)
	for i in range(len(total)):
		pos = int(total[i]) - 1
		index = int(pos)
		bit = coefficients_encoded[index][i]
		result = numpy.append(result, bit)

	return result

precision = 3
stream_length = pow(2, precision)
bernstein_values = numpy.array([2.0/stream_length, 5.0/stream_length, 3.0/stream_length, 6.0/stream_length])
result = gamma(4.0/stream_length, bct.clockdiv, bct.unary_SNG, len(bernstein_values), precision, stream_length, bernstein_values)
numOf1 = bct.number_of_1(result)
total = numOf1 / pow(16, 3)
print(total)

