import numpy
import bct

# Parameters:
# value: 0 <= n < 1
# method: bitstream generation method
# degree: number of terms
# precision: number of bits
# coefficients: numpy array with 'degree' values
def gamma(value, method, SNG, degree, precision, coefficients):
	# convert coefficients to bitstreams
	coefficients_encoded = numpy.array([])
	for i in range(len(coefficients)):
		a = SNG(precision, coefficients[i])
		x = method(i + 1, a, degree + 1)
		if len(coefficients_encoded) == 0:
			coefficients_encoded = x
		else:
			coefficients_encoded = numpy.vstack((coefficients_encoded, x))

	total = numpy.zeros(pow(precision, degree))
	for i in range(degree):
		p = method(i + 1, SNG(precision, value), degree)
		total = numpy.add(total, p)

	result = numpy.zeros(0)
	for i in range(len(total)):
		pos = int(total[i])
		index = int(pos)
		bit = coefficients_encoded[index][i]
		result = numpy.append(result, bit)

	return result

bernstein_values = numpy.array([2.0/8.0, 5.0/8.0, 3.0/8.0, 6.0/8.0])
result = gamma(4.0/8.0, bct.clockdiv, bct.unary_SNG, 3, 8, bernstein_values)
numOf1 = bct.number_of_1(result)
total = numOf1 / pow(8, 3)
print(total)

