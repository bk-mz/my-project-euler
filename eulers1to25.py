from math import sqrt

def problem1():
	print(sum([x for x in range(1000) if x % 3 == 0 or x % 5 == 0]))

def problem2():
	N = 4000000
	def fib():
		a, b = 0, 1
		while 1:
			yield a
			a, b = b, a + b
	gen = fib()
	sum = 0
	elem = next(gen)
	while elem < N:
		if elem % 2 == 0:
			sum += elem
		elem = next(gen)
	print(sum)

def problem3():
	N = 600851475143
	def factors(x):
		"""
		http://en.wikipedia.org/wiki/Primality_test
		"""
		if x % 2 == 0: yield 2
		if x % 3==0: yield 3
		k = 1
		sqrtx = sqrt(x)
		while True:
			factor1 = 6*k+1
			factor2 = 6*k-1
			if x % factor1 == 0:
				yield factor1
			if x % factor2 == 0:
				yield factor2
			if factor2 > sqrtx or factor1 > sqrtx:
				break
			k += 1

	gen_factors = factors(N)
	known_factors = list(gen_factors)
	# there is a chance we missed last maximum divisor
	last_factor = int(N / known_factors[-1])
	if last_factor > known_factors[-1]:
		known_factors.append(last_factor)

	known_factors.reverse() # start with maximum factor
	for factor in known_factors:
		l = list(factors(factor))
		if not l: #empty list means factor is prime
			print('largest prime factor is {}'.format(factor))
			break

problem3()

