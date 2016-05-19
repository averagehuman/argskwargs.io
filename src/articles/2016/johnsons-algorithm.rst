
Johnson-Trotter Algorithm (Python)
##################################

:date: 2016-05-19 08:00
:category: Python
:author: gmflanagan


.. container:: callout primary

    When I was learning Python, one of the first things that I wrote was
    an implementation of the Johnson-Trotter algorithm. It was based on some Pascal
    code from the book `Programming for Mathematicians`_ and written for `Python 2.5.1`_
    (2007!) I've made a few improvements and it will run on Python 2 and 3, but
    the basic approach is the same.

Name rings a bell...
====================

What wikipedia calls the `Steinhaus-Johnson-Trotter Algorithm`_ is a method of generating
all permutations of a given sequence and was apparently known to 17th Century bell ringers!
A feature of the algorithm is that each successive permutation differs from the previous
permutation by a single transposition (one element is swapped with another), and these
repeated transpositions follow a fairly natural pattern:

.. code-block:: bash

    ['A', 'B', 'C', 'D']
    ['A', 'B', 'D', 'C']
    ['A', 'D', 'B', 'C']
    ['D', 'A', 'B', 'C']
    ['D', 'A', 'C', 'B']
    ['A', 'D', 'C', 'B']
    ['A', 'C', 'D', 'B']
    ['A', 'C', 'B', 'D']
    ['C', 'A', 'B', 'D']
    ['C', 'A', 'D', 'B']
    ['C', 'D', 'A', 'B']
    ['D', 'C', 'A', 'B']
    ['D', 'C', 'B', 'A']
    ['C', 'D', 'B', 'A']
    ['C', 'B', 'D', 'A']
    ['C', 'B', 'A', 'D']
    ['B', 'C', 'A', 'D']
    ['B', 'C', 'D', 'A']
    ['B', 'D', 'C', 'A']
    ['D', 'B', 'C', 'A']
    ['D', 'B', 'A', 'C']
    ['B', 'D', 'A', 'C']
    ['B', 'A', 'D', 'C']
    ['B', 'A', 'C', 'D']

So it is easy to imagine how this pattern may have been discovered by `Change Ringers`_ ringing
massive church bells in sequence:

.. pull-quote::

    The physical constraint of the mass of the bells means they can only be slightly
    delayed or advanced in the striking order, so they cannot be omitted from a sequence,
    and can only be made to change by one position in successive sequences.

    -- Wikipedia, Change Ringers

The Algorithm
=============

Take the case n = 4 say, so we want to generate all permutations of the set {1, 2, 3, 4}.
Each element of the set is given a flag - 'left' or 'right' - which determines the direction
that an element is "looking". You start off with the sequence:

.. epigraph::

    ['left',1], ['left',2], ['left',3], ['left',4]

So all elements are initially looking left. Then in the course of the algorithm, you may
have the situation:

.. epigraph::

    ['left',3], ['right',2], ['right',1], ['left',4]

in which case, you say:

+ 1 sees 4
+ 2 sees 1
+ 3 sees nothing
+ 4 sees 1

The direction flag is obviously a boolean quantity, but it simplifies calculations if it
is represented by 1 or -1, rather than 0 or 1, because then you can determine which element
another element "sees" by using *element's index + element's flag*.

An element is said to be **mobile** if it is looking at a smaller number. eg. in the sequence
above, both 2 and 4 are mobile.

Then the algorithm is:

- find the highest mobile; if none exists, stop
- swap this mobile with the element it sees
- reverse the direction flags of any element larger than the mobile

In coding the algorithm (following Seroul), sentinels with value 1 bigger than n are added
at either end of the sequence, this means that any element which ends up at the beginning
looking left, or at the end looking right, will always see a larger element and so will
never be considered mobile. This removes the need to treat the left and rightmost
elements as special cases in every loop. 

Python Implementation
=====================

A generator function.

.. code-block:: python

    def jpermute(iterable):
        """
        Use the Johnson-Trotter algorithm to return all permutations of iterable.
        """
        sequence = list(iterable)
        length = len(sequence)
        indices = range(1, length+1)
        # the list of directed integers: [-1, 1], [-1, 2], ...
        state = [[-1, idx] for idx in indices]
        # add sentinels at the beginning and end
        state = [[-1, length+1]] + state + [[-1, length+1]]
        # the first permutation is the sequence itself
        yield sequence
        mobile_index = mobile_direction = direction = value = None
        while True:
            # 1. find the highest mobile
            mobile = -1
            for idx in indices:
                direction, value = state[idx]
                if value > mobile and value > state[idx+direction][1]:
                    # value is mobile and greater than the previous mobile
                    mobile = value
                    mobile_index = idx
                    mobile_direction = direction
                    if mobile == length:
                        # no point in continuing as mobile is as large as it can be.
                        break
            if mobile == -1:
                break
            
            # 2. swap the mobile with the element it 'sees'
            sees = mobile_index + mobile_direction
            state[mobile_index], state[sees] = state[sees], state[mobile_index]
            sequence[mobile_index-1], sequence[sees-1] = sequence[sees-1], sequence[mobile_index-1]
            
            # 3. switch the direction of elements greater than mobile
            if mobile < length:
                for idx in indices:
                    if state[idx][1] > mobile:
                        state[idx][0] = -state[idx][0]
            yield sequence
 
Speed
-----

This is quicker than my original code but nowhere near competive with
`itertools.permutations`_ which is implemented in C.

.. code-block:: bash

    $ python2 -m timeit 'from jpermutation import jpermute;list(jpermute("ABC"))'
    100000 loops, best of 3: 7.55 usec per loop
    $ python2 -m timeit 'from jpermutation import jpermute;list(jpermute("ABCD"))'
    10000 loops, best of 3: 23.1 usec per loop
    $ python2 -m timeit 'from jpermutation import jpermute;list(jpermute("ABCDE"))'
    10000 loops, best of 3: 108 usec per loop
    $ python2 -m timeit 'from jpermutation import jpermute;list(jpermute("ABCDEF"))'
    1000 loops, best of 3: 658 usec per loop

Compare to:

.. code-block:: bash

    $ python2 -m timeit 'from itertools import permutations;list(permutations("ABC"))'
    100000 loops, best of 3: 2.01 usec per loop
    $ python2 -m timeit 'from itertools import permutations;list(permutations("ABCD"))'
    100000 loops, best of 3: 3.22 usec per loop
    $ python2 -m timeit 'from itertools import permutations;list(permutations("ABCDE"))'
    100000 loops, best of 3: 8.88 usec per loop
    $ python2 -m timeit 'from itertools import permutations;list(permutations("ABCDEF"))'
    10000 loops, best of 3: 44.9 usec per loop

Notes
-----

The original code returned a new list for each permutation but there was a big speedup
by returning the same mutated list each time.

There was also a minor speed improvement by writing:

.. code-block:: python

    direction, value = state[idx]

rather than the original:

.. code-block:: python

    direction = state[idx][0]
    value = state[idx][1]


.. _programming for mathematicians: https://www.amazon.co.uk/Programming-Mathematicians-Raymond-Translated-January/dp/B00MMQ77L0/ref=sr_1_3
.. _python 2.5.1: https://www.python.org/download/releases/2.5.1/
.. _change ringers: https://en.wikipedia.org/wiki/Change_ringing
.. _steinhaus-johnson-trotter algorithm: https://en.wikipedia.org/wiki/Steinhaus%E2%80%93Johnson%E2%80%93Trotter_algorithm
.. _itertools.permutations: https://docs.python.org/3/library/itertools.html#itertools.permutations

