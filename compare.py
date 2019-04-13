import time
import bct
import numpy
from timeit import default_timer as timer

def perftest(s):
	# 3 input test
	c0 = 0.25
	c1 = 0.75
	c2 = 0.5
	p = 8 # number of bits of precision
	bitstream_c0 = numpy.zeros(0)
	bitstream_c1 = numpy.zeros(0)
	bitstream_c2 = numpy.zeros(0)
	iterations = 0
	answer = numpy.zeros(0)

	start = timer()

	for c2_counter in range(0, pow(2,p)):
		for c1_counter in range(0, pow(2,p)):
			for c0_counter in range(0, pow(2,p)):
				if (c0_counter < c0 * pow(2,p)):
					bitstream_c0 = numpy.append(bitstream_c0, 1)
				else:
					bitstream_c0 = numpy.append(bitstream_c0, 0)
	
				if (c1_counter < c1 * pow(2,p)):
					bitstream_c1 = numpy.append(bitstream_c1, 1)
				else:
					bitstream_c1 = numpy.append(bitstream_c1, 0)
	
				if (c2_counter < c2 * pow(2,p)):
					bitstream_c2 = numpy.append(bitstream_c2, 1)
				else:
					bitstream_c2 = numpy.append(bitstream_c2, 0)
				iterations = iterations + 1
				if (iterations % s == 0):
					answer = numpy.append(answer, numpy.logical_and(numpy.logical_and(bitstream_c0, bitstream_c1), bitstream_c2))
					bitstream_c0 = numpy.zeros(0)
					bitstream_c1 = numpy.zeros(0)
					bitstream_c2 = numpy.zeros(0)


	end = timer()
	time = (end - start)
	print("time for " + str(s) + ": " + str(time) + "s")

	# verify answer is correct
	tl = pow(2,3*p)
	if (bct.number_of_1(answer) / tl == c0 * c1 * c2):
		print("Answer matches")
	else:
		print("Answer DOES NOT MATCH")


perftest(64)
perftest(128)
perftest(256)
perftest(512)
perftest(1024)
perftest(1024)
perftest(2048)
perftest(4096)
perftest(8192)
perftest(16384)
perftest(32768)
perftest(65536)


