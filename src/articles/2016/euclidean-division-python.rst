
Greatest Common Divisor (Python)
################################

:date: 2016-05-17 13:00
:category: Python
:tags: Number Theory
:author: gmflanagan


The **gcd (Greatest Common Divisor)** function prior to Python version 3.5 is a pure
python function found in the standard library's `fractions`_ module. It uses the common
algorithm:

.. code-block:: python

    def gcd(a, b):
        while b:
            a, b = b, a % b
        return a

Since v3.5, there is an implementation in C that uses `Lehmer's Algorithm`_ when the
input numbers are large, but falls back to the standard method for smaller inputs. The
basic loop in the simple case is as above:

.. code-block:: c

    while (y != 0) {
        t = y;
        y = x % y;
        x = t;
    }

This new **gcd** function can now be found in the `math`_ module and `fractions.gcd`_
is deprecated.  (The python issue is `22486`_ and the implementation is
`here <https://hg.python.org/cpython/file/tip/Objects/longobject.c#l4480>`_).


Blankinship Algorithm
=====================

One problem with the standard algorithm is that it throws away intermediate results, so
it doesn't help if you want to determine, in addition to the GCD of \\(a\\) and
\\(b\\), those unique integers \\(u\\) and \\(v\\)
such that:

.. math::

   ua + vb = GCD

(See `Bezout's Identity`_). For this you can use the `Blankinship Algorithm`_ for
solving linear congruences. Roughly, this augments the identity matrix with the values
for which the GCD is sought, and uses a form of row reduction to find the above identity.
In general, this method can be used to find the GCD of \\(n >= 2\\) integers.

Here is some code to solve the \\(n = 2\\) case:

.. code-block:: python

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


Simple Euclidean Algorithm
==========================

Another problem with the standard algorithm from a didactic point of view is that
it isn't immediately clear how it relates back to the theory of Euclidean division.
Using the modulus operator is a computational convenience but it makes the process
slightly opaque. Below is a naive implementation that uses repeated subtraction
as Euclid's original method describes. (Not that I'm claiming to have read Euclid!).

Once you see that process outlined, then it may be more clear that the only point of
the repeated subtraction is to determine the remainder, and that you can find that
in a single step by using the modulus.

.. code-block:: python

    def gcd_naive(x1, x2):
        """
        Determine the GCD of two positive integers by applying the Euclidean division algorithm.
        """
        return list(idivide(x1, x2))[-1]


    def idivide(a, b):
        """
        The original Euclidean method of finding a Greatest Common Divisor using
        repeated subtraction rather than applying the 'mod' operator directly.

        To divide 'b' into 'a' is to find the 'q' and 'r' such that:

            a = b.q + r

        and this is done by repeatedly subtracting 'b'.

        This is an iterator which yields 'b' each time it is subtracted from the
        associated 'a', up until the point that 'a' becomes less than 'b'. Then
        'b' becomes the new 'a', and the remainder 'r' becomes the new 'b', and
        the process repeated. Stop when there is no remainder. (For convenience,
        also yield the first a).

        The final element in the sequence is the GCD.

        So with input a=1071 and b=462, the sequence generated is:

            [1071, 462, 462, 147, 147, 147, 21, 21, 21, 21, 21, 21, 21]

        ie. 462 is taken from 1071 twice (q=2), 147 is taken from 462 three times (q=3),
        and 21 is taken from 147 seven times (q=7). But insofar as you only want
        to calculate the GCD, the actual value of q isn't important.

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


Test Method
-----------

.. code-block:: python

    from __future__ import print_function
    import itertools as itools
    try:
        from math import gcd
    except ImportError:
        # python < 3.5
        from fractions import gcd


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
        # idivide doesn't provide the final remainder which is always 0
        divisors.append((0, 0))
        # format the output depending on the length of the longest digit
        padding = max([len(str(x1)), len(str(x2))])
        format_string = "%%%(pad)dd  = %%4d  x  %%-%(pad)dd" % {'pad': padding}
        for i in range(len(divisors)-2):
            a, b, q, r = divisors[i][0], divisors[i+1][0], divisors[i+1][1], divisors[i+2][0]
            print(format_string % (a, q, b), end="")
            if r:
                print(" with remainder %d" % r)
            else:
                # no remainder, so we're done and 'b' is the GCD
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



Test Output
-----------

.. code-block:: bash

    print_gcd(9, 3)
    ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

    9  =    3  x  3
    --------------------------------------------------------------------------------
        gcd(9, 3) = 3. Number of Subtractions: 3
    --------------------------------------------------------------------------------

.. code-block:: bash

    print_gcd(12, 9)
    ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

    12  =    1  x  9  with remainder 3
     9  =    3  x  3
    --------------------------------------------------------------------------------
        gcd(12, 9) = 3. Number of Subtractions: 4
    --------------------------------------------------------------------------------

.. code-block:: bash

    print_gcd(99, 7)
    ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

    99  =   14  x  7  with remainder 1
     7  =    7  x  1
    --------------------------------------------------------------------------------
        99 and 7 are coprime. Number of Subtractions: 21
    --------------------------------------------------------------------------------

.. code-block:: bash

    print_gcd(1071, 462)
    ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

    1071  =    2  x  462  with remainder 147
     462  =    3  x  147  with remainder 21
     147  =    7  x  21
    --------------------------------------------------------------------------------
        gcd(1071, 462) = 21. Number of Subtractions: 12
    --------------------------------------------------------------------------------

.. code-block:: bash

    print_gcd(10171, 462)
    ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

    10171  =   22  x  462   with remainder 7
      462  =   66  x  7
    --------------------------------------------------------------------------------
        gcd(10171, 462) = 7. Number of Subtractions: 88
    --------------------------------------------------------------------------------

.. code-block:: bash

    print_gcd(520117, 1462)
    ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

    520117  =  355  x  1462   with remainder 1107
      1462  =    1  x  1107   with remainder 355
      1107  =    3  x  355    with remainder 42
       355  =    8  x  42     with remainder 19
        42  =    2  x  19     with remainder 4
        19  =    4  x  4      with remainder 3
         4  =    1  x  3      with remainder 1
         3  =    3  x  1
    --------------------------------------------------------------------------------
        520117 and 1462 are coprime. Number of Subtractions: 377
    --------------------------------------------------------------------------------


.. code-block:: bash

    print_gcd(1216342683557601535506312, 436522681849110124616457)
    ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

    1216342683557601535506312  =    2  x  436522681849110124616457  with remainder 343297319859381286273398
     436522681849110124616457  =    1  x  343297319859381286273398  with remainder 93225361989728838343059
     343297319859381286273398  =    3  x  93225361989728838343059   with remainder 63621233890194771244221
      93225361989728838343059  =    1  x  63621233890194771244221   with remainder 29604128099534067098838
      63621233890194771244221  =    2  x  29604128099534067098838   with remainder 4412977691126637046545
      29604128099534067098838  =    6  x  4412977691126637046545    with remainder 3126261952774244819568
       4412977691126637046545  =    1  x  3126261952774244819568    with remainder 1286715738352392226977
       3126261952774244819568  =    2  x  1286715738352392226977    with remainder 552830476069460365614
       1286715738352392226977  =    2  x  552830476069460365614     with remainder 181054786213471495749
        552830476069460365614  =    3  x  181054786213471495749     with remainder 9666117429045878367
        181054786213471495749  =   18  x  9666117429045878367       with remainder 7064672490645685143
          9666117429045878367  =    1  x  7064672490645685143       with remainder 2601444938400193224
          7064672490645685143  =    2  x  2601444938400193224       with remainder 1861782613845298695
          2601444938400193224  =    1  x  1861782613845298695       with remainder 739662324554894529
          1861782613845298695  =    2  x  739662324554894529        with remainder 382457964735509637
           739662324554894529  =    1  x  382457964735509637        with remainder 357204359819384892
           382457964735509637  =    1  x  357204359819384892        with remainder 25253604916124745
           357204359819384892  =   14  x  25253604916124745         with remainder 3653890993638462
            25253604916124745  =    6  x  3653890993638462          with remainder 3330258954293973
             3653890993638462  =    1  x  3330258954293973          with remainder 323632039344489
             3330258954293973  =   10  x  323632039344489           with remainder 93938560849083
              323632039344489  =    3  x  93938560849083            with remainder 41816356797240
               93938560849083  =    2  x  41816356797240            with remainder 10305847254603
               41816356797240  =    4  x  10305847254603            with remainder 592967778828
               10305847254603  =   17  x  592967778828              with remainder 225395014527
                 592967778828  =    2  x  225395014527              with remainder 142177749774
                 225395014527  =    1  x  142177749774              with remainder 83217264753
                 142177749774  =    1  x  83217264753               with remainder 58960485021
                  83217264753  =    1  x  58960485021               with remainder 24256779732
                  58960485021  =    2  x  24256779732               with remainder 10446925557
                  24256779732  =    2  x  10446925557               with remainder 3362928618
                  10446925557  =    3  x  3362928618                with remainder 358139703
                   3362928618  =    9  x  358139703                 with remainder 139671291
                    358139703  =    2  x  139671291                 with remainder 78797121
                    139671291  =    1  x  78797121                  with remainder 60874170
                     78797121  =    1  x  60874170                  with remainder 17922951
                     60874170  =    3  x  17922951                  with remainder 7105317
                     17922951  =    2  x  7105317                   with remainder 3712317
                      7105317  =    1  x  3712317                   with remainder 3393000
                      3712317  =    1  x  3393000                   with remainder 319317
                      3393000  =   10  x  319317                    with remainder 199830
                       319317  =    1  x  199830                    with remainder 119487
                       199830  =    1  x  119487                    with remainder 80343
                       119487  =    1  x  80343                     with remainder 39144
                        80343  =    2  x  39144                     with remainder 2055
                        39144  =   19  x  2055                      with remainder 99
                         2055  =   20  x  99                        with remainder 75
                           99  =    1  x  75                        with remainder 24
                           75  =    3  x  24                        with remainder 3
                           24  =    8  x  3
    --------------------------------------------------------------------------------
        gcd(1216342683557601535506312, 436522681849110124616457) = 3. Number of Subtractions: 204
    --------------------------------------------------------------------------------


.. _math: https://docs.python.org/3/library/math.html
.. _fractions: https://docs.python.org/3/library/fractions.html
.. _fractions.gcd: https://docs.python.org/2/library/fractions.html#fractions.gcd
.. _22486: https://bugs.python.org/issue22486
.. _lehmer's algorithm: https://en.wikipedia.org/wiki/Lehmer%27s_GCD_algorithm
.. _blankinship algorithm: http://mathworld.wolfram.com/BlankinshipAlgorithm.html
.. _bezout's identity: https://en.wikipedia.org/wiki/B%C3%A9zout%27s_identity


