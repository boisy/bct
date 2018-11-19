# Performance test
import time

import bct

start = time.time()

iterations = 10000
for n in range(1, iterations):
	n1 = bct.unary_SNG(4, 16, .5)

end = time.time()
print(iterations, "X -- unary_SNG(4, 16, .5) =", end - start)

start = time.time()

iterations = 1000
for n in range(1, iterations):
	n1 = bct.lfsr_SNG(4, 16, .5)

end = time.time()
print(iterations, "X -- unary_SNG(4, 16, .5) =", end - start)

