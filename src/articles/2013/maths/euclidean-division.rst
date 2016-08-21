
Euclidean Division
==================

:date: 2013-05-08
:author: averagehuman
:category: Maths
:tags: Number Theory


Given any two integer quantities \\(a\\) and \\(b\\), with \\(a > b\\), we can
ask what repeated addition of \\(b\\) will give us \\(a\\). Or, equivalently,
into what multiple of \\(b\\) can \\(a\\) be divided.

For example, \\(6 = 2 \\times 3\\) so six divided by three is two, and
\\(7 = 2\\times3 + 1\\) so seven divided by three is two "with one over".

This is a basic notion but its formal statement is important as it provides the foundation
for the `Euclidean Division Algorithm`_, `Euclid's Lemma`_ and `Bezout's Identity`_,
all of which are basic tools for studying divisibility and factorisation
in \\(\\mathbb{Z}\\).


**Theorem (Euclidean Division):** Let \\(a\\) and \\(b\\) be integers. If
\\(b > 0\\), then there exist \\(q, r\\), also integers, such that

.. math::

    a = bq + r  \text{ where } 0 \leq r < b \label{a}\tag{1}

**Proof [P. M. Cohn]** It is easy to establish the result using rational numbers:
let \\(q\\) be \\(\\lfloor \\frac{a}{b} \\rfloor\\) the largest integer not exceeding
\\(\\frac{a}{b}\\), then

.. math::

    0 \leq \left(\frac{a}{b}\right) - q < 1

and so

.. math::

    0 \leq a - bq < b

Hence the number \\(r\\) given by \\(r = a - bq\\) satisfies \\((1)\\).

But rather than invoking rational numbers, the result can also be proved via
the `Principle of Least Element`_. Let \\(S\\) be the
set of all non-negative integers of the form \\(a - bn\\). The set \\(S\\) is not empty
- for example, take \\(n = -a^2\\), then

.. math::

    a - bn = a + a^2b \geq 0

Therefore \\(S\\) has a least element \\(r = a - bq\\) say. By definition, \\(r \\geq 0\\),
and so we must only show that \\(r < b\\). Suppose on the contrary that \\(r \\geq b\\),
then

.. math::

    r - b = a - bq - b = a - b(q +1)

which is an element of \\(S\\) smaller then \\(r\\), a contradiction. \\(\\Box\\)

:See Also: An alternative proof `on wikipedia`_.


.. _Euclid: http://en.wikipedia.org/wiki/Euclid
.. _Euclid's Lemma: {filename}/articles/2013/maths/divisibility-and-euclids-lemma.rst
.. _Bezout's Identity: http://en.wikipedia.org/wiki/B%C3%A9zout%27s_identity
.. _Euclidean Division Algorithm: http://en.wikipedia.org/wiki/Euclidean_algorithm
.. _integer floor: http://en.wikipedia.org/wiki/Floor_and_ceiling_functions
.. _rational numbers: http://en.wikipedia.org/wiki/Rational_number
.. _principle of least element: https://en.wikipedia.org/wiki/Well-order
.. _on wikipedia: http://en.wikipedia.org/wiki/Euclidean_division


