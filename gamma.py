import numpy
import bct

# Parameters:
# value: 0 <= n < 1
# method: bitstream generation method
# degree: number of terms
# precision: number of bits
# coefficients: numpy array with 'degree' values
def gamma(value, method, degree, precision, coefficients):
	# convert coefficients to bitstreams
	coefficients_encoded = numpy.array([])
	for i in range(len(coefficients)):
		a = bct.unary_sng(precision, coefficients[i])
		x = method(i + 1, a, degree + 1)
		if len(coefficients_encoded) == 0:
			coefficients_encoded = x
		else:
			coefficients_encoded = numpy.vstack((coefficients_encoded, x))

	total = numpy.zeros(pow(precision, degree))
	for i in range(degree):
		p = method(i + 1, bct.unary_sng(precision, value), degree)
		total = numpy.add(total, p)

	result = numpy.zeros(0)
	for i in range(len(total)):
		pos = int(total[i])
		index = int(pos)
		bit = coefficients_encoded[index][i]
		result = numpy.append(result, bit)

	return result

bernstein_values = numpy.array([0.0955, 0.7207, 0.3476, 0.9988, 0.7017, 0.9695, 0.9939])
result = gamma(3.0/4.0, bct.clockdiv, 6, 4, bernstein_values)
print(result)
numOf1 = bct.number_of_1(result)
total = numOf1 / pow(4, 6)
print(total)

