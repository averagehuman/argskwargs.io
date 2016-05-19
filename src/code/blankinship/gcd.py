#!/usr/bin/env python3
###############################################################################
#
# Python Euclidean algorithm.
#
# Copyright (c) 2016 Gerard Flanagan. BSD licensed.
###############################################################################

from __future__ import print_function
import itertools as itools
try:
    from math import gcd
except ImportError:
    # python < 3.5
    from fractions import gcd


def idivide(a, b):
    """
    The original Euclidean method of finding a Greatest Common Divisor using
    repeated subtraction rather than applying the 'mod' operator directly.

    To divide 'b' into 'a' is to find the 'q' and 'r' such that:

        a = b.q + r

    and this is done by repeatedly subtracting 'b'.

    This is an iterator which yields 'b' each time it is subtracted from the
    associated 'a', up until the point that 'a' becomes less than 'b', and then
    the 'b' becomes the new 'a', and the remainder 'r' becomes the new 'b', and
    the subtraction continues. Stop when there is no remainder. (For convenience,
    also yield the first a).

    So with input a=1071 and b=462, the sequence generated is:

        [1071, 462, 462, 147, 147, 147, 21, 21, 21, 21, 21, 21, 21]

    ie. 462 is taken from 1071 twice (q=2), 147 is taken from 462 three times (q=3),
    and 21 is taken from 147 seven times (q=7).
    """
    a = int(a)
    b = int(b)
    if a <= 0 or b <= 0:
        raise ValueError("Invalid input. Expecting two positive integers")
    if a < b:
        a, b = b, a
    yield a
    r = 0
    while a != b:
        r = a - b
        if r > 0:
            a = r
            yield b
        else:
            b = -r
            yield a
    if r:
        yield abs(r)


def gcd_naive(x1, x2):
    return list(idivide(x1, x2))[-1]


def blankinship(x, y):
    """
    The blankinship algorithm extends the identity matrix with the values of
    the elements for which the gcd is required, then uses a form of row
    reduction to determine, in addition to the gcd, the unique numbers 'u'
    and 'v' such that 'ux + vy = gcd'.
    """
    x = int(x)
    y = int(y)
    if x <= 0 or y <= 0:
        raise ValueError("Invalid input. Expecting two positive integers")
    a,b,c,d = 1,0,0,1
    while x>0 and y>0:
        if x >= y:
            q = x // y
            x = x - y * q
            a = a - q * c
            b = b - q * d
        else:
            q = y // x
            y = y - x * q
            c = c - q * a
            d = d - q * b
    if x > 0:
        gcd, u, v = x, a, b
    else:
        gcd, u, v = y, c, d
    return gcd, u, v


def print_gcd(x1, x2):
    """
    Print each step in the Euclidean division algorithm for calculating the GCD of two integers.
    Also prints the total number of subtractions required to get the result.

    """
    divisors = []
    steps = -1
    hline = '-' * 80
    print(':' * 80)
    print('')
    # Use 'groupby' to collect together runs of dividers in the idivide sequence.
    for key, grouper in itools.groupby(idivide(x1, x2)):
        # count is the 'q' in each step in the algorithm, ie. the number of times
        # a particular 'b' was subtracted from the associated 'a'
        count = len(list(grouper))
        divisors.append((key, count))
        steps += count
    if len(divisors) == 1:
        assert x1 == x2 == divisors[0][0]
        print(hline)
        print("gcd(%s, %s) = %s" % (x1, x2, x1))
        print(hline)
        print("")
        return
    divisors.append((0, 0)) # idivide doesn't provide the final remainder which is always 0
    # format the output depending on the length of the longest digit
    padding = max([len(str(x1)), len(str(x2))])
    format_string = "%%%(pad)dd  = %%4d  x  %%-%(pad)dd" % {'pad': padding}
    for i in range(len(divisors)-2):
        a, b, q, r = divisors[i][0], divisors[i+1][0], divisors[i+1][1], divisors[i+2][0]
        print(format_string % (a, q, b), end="")
        if r:
            print(" with remainder %d" % r)
        else:
            # there is no remainder, so this is the last step in the algorithm and 'b' is the GCD
            assert b == gcd(x1, x2) == blankinship(x1, x2)[0]
            print("")
            print(hline)
            if b == 1:
                print("    %d and %d are coprime" % (x1, x2), end='')
            else:
                print("    gcd(%d, %d) = %d" % (x1, x2, b), end='')
            print(". Number of Subtractions: %s" % steps)
            print(hline)
            print("")
            print("")
            break


print_gcd(9, 3)
print_gcd(12, 9)
print_gcd(99, 7)
print_gcd(1071, 462)
print_gcd(10171, 462)
print_gcd(520117, 1462)
print_gcd(1216342683557601535506312, 436522681849110124616457)

