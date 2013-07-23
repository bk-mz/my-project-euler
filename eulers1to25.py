import copy
from functools import reduce
from itertools import chain, combinations
from math import sqrt, floor
from timeit import default_timer, itertools


def sieve():
    """
    Yields the sequence of prime numbers via the Sieve of Eratosthenes.
    http://stackoverflow.com/questions/1628949/to-find-first-n-prime-numbers-in-python
    """
    D = {}  # map composite integers to primes witnessing their compositeness
    q = 2   # first integer to test for primality
    while True:
        if q not in D:
            yield q        # not marked composite, must be prime
            D[q * q] = [q]   # first multiple of q not already marked
        else:
            for p in D[q]: # move each witness to its next multiple
                D.setdefault(p + q, []).append(p)
            del D[q]       # no longer need D[q], free memory
        q += 1


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
    summ = 0
    elem = next(gen)
    while elem < N:
        if elem % 2 == 0:
            summ += elem
        elem = next(gen)
    print(summ)


def problem3():
    N = 600851475143

    def factors(x):
        """
        http://en.wikipedia.org/wiki/Primality_test
        """
        if x % 2 == 0: yield 2
        if x % 3 == 0: yield 3
        k = 1
        sqrtx = sqrt(x)
        while True:
            factor1 = 6 * k + 1
            factor2 = 6 * k - 1
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


def problem4():
    M = 900
    N = 1000

    palyndroms = []
    for i in reversed(range(M, N)):
        for j in reversed(range(i, N)):
            s = str(i * j)
            if s == s[::-1]:
                palyndroms.append(s)
    print(palyndroms)
    print(max(palyndroms))


def problem5():
    """
    we got a hint that tells us that [1,2,3,4,5,6,7,8,9,10] all
    divide 2520 with no remainder. 2520 is also divisible by [12,14,15,18,20] with no remainder.
    16 is left. But, 2520 * 2 = 5040 is divisible by 16 with no reminder.
    That means, [1,2,3,4,5,6,7,8,9,10,12,14,15,16,17,18,20] have smallest number 5040 evenly divisible
    by all of them. Only prime divisors are left [11,13,17,19]. Least common multiple for these prime
    numbers is 11 * 13 * 17 * 19.
    So, the smallest number divisible by all of range(1,21) is 11 * 13 * 17 * 19 * 5040 = 232792560
    """

    # BUT THAT DOES NOT SOLVE THE COMMON PROBLEM
    # find the smallest number N divisible by all range(2, K).
    # see http://en.wikipedia.org/wiki/Prime_factor
    print(232792560)


def problem6():
    # okay, I know from Knuth that sum of all squares for N is n*(n+1)(2n+1)/6
    # okay, I know that linear sum of all range(1, N) is N*(1+N)/2
    N = 100

    def all_squares(x):
        return x * (x + 1) * (2 * x + 1) / 6

    def just_sum(x):
        return x * (1 + x) / 2

    sm = int(just_sum(N))
    squares = int(all_squares(N))
    print('Answer is {}'.format(sm * sm - squares))


def problem7():
    gen = sieve()
    N = 10001
    prime = 0
    for i in range(1, N + 1):
        prime = next(gen)
    print(prime)


def problem8():
    """
    More elegant solution
    s = '731...450'
    d = map(int, list(s))
    print max([reduce(lambda x, y: x*y, d[i:i+5]) for i in xrange(len(s)-4)])
    """
    string = "73167176531330624919225119674426574742355349194934" + \
             "96983520312774506326239578318016984801869478851843" + \
             "85861560789112949495459501737958331952853208805511" + \
             "12540698747158523863050715693290963295227443043557" + \
             "66896648950445244523161731856403098711121722383113" + \
             "62229893423380308135336276614282806444486645238749" + \
             "30358907296290491560440772390713810515859307960866" + \
             "70172427121883998797908792274921901699720888093776" + \
             "65727333001053367881220235421809751254540594752243" + \
             "52584907711670556013604839586446706324415722155397" + \
             "53697817977846174064955149290862569321978468622482" + \
             "83972241375657056057490261407972968652414535100474" + \
             "82166370484403199890008895243450658541227588666881" + \
             "16427171479924442928230863465674813919123162824586" + \
             "17866458359124566529476545682848912883142607690042" + \
             "24219022671055626321111109370544217506941658960408" + \
             "07198403850962455444362981230987879927244284909188" + \
             "84580156166097919133875499200524063689912560717606" + \
             "05886116467109405077541002256983155200055935729725" + \
             "71636269561882670428252483600823257530420752963450"

    length = len(string)
    window = 5
    windows = {}
    odds = range(0, 7) # we don't need smaller digits
    for i in range(0, length - window + 1):
        cur_window = string[i:i + window]
        windows[cur_window] = 1
        for j in range(0, window):
            int1 = int(string[i + j:i + j + 1])
            if int1 in odds:
                del windows[cur_window]
                break
            windows[cur_window] *= int1

    print(max(windows.values()))


def problem9():
    N = 1000
    n = 200
    for b in range(n, N):
        for a in range(n, b):
            c = N - b - a
            if c <= b or c <= 0:
                break
            diff = c * c - b * b - a * a
            if diff is 0:
                print("abc = {}".format(a * b * c))
                return


def problem10():
    gen = sieve()
    N = 2000000
    summ = 0
    while True:
        prime = next(gen)
        if prime < N:
            summ += prime
        else:
            break
    print(summ)


def problem11():
    strings = [
        "08 02 22 97 38 15 00 40 00 75 04 05 07 78 52 12 50 77 91 08",
        "49 49 99 40 17 81 18 57 60 87 17 40 98 43 69 48 04 56 62 00",
        "81 49 31 73 55 79 14 29 93 71 40 67 53 88 30 03 49 13 36 65",
        "52 70 95 23 04 60 11 42 69 24 68 56 01 32 56 71 37 02 36 91",
        "22 31 16 71 51 67 63 89 41 92 36 54 22 40 40 28 66 33 13 80",
        "24 47 32 60 99 03 45 02 44 75 33 53 78 36 84 20 35 17 12 50",
        "32 98 81 28 64 23 67 10 26 38 40 67 59 54 70 66 18 38 64 70",
        "67 26 20 68 02 62 12 20 95 63 94 39 63 08 40 91 66 49 94 21",
        "24 55 58 05 66 73 99 26 97 17 78 78 96 83 14 88 34 89 63 72",
        "21 36 23 09 75 00 76 44 20 45 35 14 00 61 33 97 34 31 33 95",
        "78 17 53 28 22 75 31 67 15 94 03 80 04 62 16 14 09 53 56 92",
        "16 39 05 42 96 35 31 47 55 58 88 24 00 17 54 24 36 29 85 57",
        "86 56 00 48 35 71 89 07 05 44 44 37 44 60 21 58 51 54 17 58",
        "19 80 81 68 05 94 47 69 28 73 92 13 86 52 17 77 04 89 55 40",
        "04 52 08 83 97 35 99 16 07 97 57 32 16 26 26 79 33 27 98 66",
        "88 36 68 87 57 62 20 72 03 46 33 67 46 55 12 32 63 93 53 69",
        "04 42 16 73 38 25 39 11 24 94 72 18 08 46 29 32 40 62 76 36",
        "20 69 36 41 72 30 23 88 34 62 99 69 82 67 59 85 74 04 36 16",
        "20 73 35 29 78 31 90 01 74 31 49 71 48 86 81 16 23 57 05 54",
        "01 70 54 71 83 51 54 69 16 92 33 48 61 43 52 01 89 19 67 48"]

    mtx = [[int(x) for x in y.split()] for y in strings]
    v_mirrored = [[int(col) for col in list(reversed(rows))] for rows in mtx]
    W = 4

    def max_in_series(r):
        return max([reduce(lambda x, y: x * y, r[i:i + W]) for i in range(len(r) - W + 1)])

    def diag_cuts(_):
        return [[_[row - col][col] for col in range(0, row + 1)] for row in range(W - 1, len(mtx))]

    def maxx(_):
        return max(map(max_in_series, _))

    print(max([
        #rows
        maxx(mtx),
        #cols
        maxx(list(zip(*mtx))),
        # okay, now diagonal cuts
        #diag upper triangle
        maxx(diag_cuts(mtx)),
        #diag lower triangle
        maxx(diag_cuts(list(reversed(mtx)))),
        # okay, now to other bias (we should vertically mirror matrix and apply same functions as above)
        maxx(diag_cuts(v_mirrored)),
        maxx(diag_cuts(list(reversed(v_mirrored))))]))


def sieve2(limit):
    yield 2
    sievebound = int((limit - 1) / 2)
    sieve = [False for i in range(0, sievebound)]
    crosslimit = int((floor(sqrt(limit)) - 1) / 2)
    for i in range(1, crosslimit):
        if not sieve[i]:
            for j in range(2 * i * (i + 1), sievebound, 2 * i + 1):
                sieve[j] = True

    for i in range(1, sievebound):
        if not sieve[i]:
            yield 2 * i + 1


def problem12():
    x = 36

    def prime_factors(value):
        crosslimit = int(floor(sqrt(value)) - 1) if x > 100 else value
        primes = sieve2(crosslimit)
        d = []
        prod = 1
        while True:
            if prod == value:
                break
            y = value
            try:
                p = next(primes)
            except StopIteration:
                if prod < value:
                    d.append(int(value / prod))
                    break
            while y % p == 0:
                y /= p
                d.append(p)
                prod *= p
        return d

    factors = set(prime_factors(x))
    print(factors)
    print([d for d in range(1, x + 1) if x % d == 0])

    def get_div_count(x):
        factors = set(prime_factors(x))
        return len([d for d in range(1, x + 1) if x % d == 0 and any(d % factor for factor in factors)])

    x = 1
    while True:
        s = int(x * (x + 1) * 0.5)
        div_count = get_div_count(s)
        print('{} : {} divisors'.format(s, div_count))
        if div_count > 500:
            print('Found number with divisors = {}'.format(s))
            return
        x += 1


start = default_timer()

problem12()

print('Elapsed:{}'.format(default_timer() - start))

