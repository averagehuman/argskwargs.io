
Mathematical Induction
======================

:date: 2013-04-27
:author: averagehuman
:category: maths


A good informal analogy of mathematical induction is a line
of up-ended dominos - if you can show that both of the following are true:

1. If **any** one of the dominos fall, then the next domino will also fall
2. The first domino must fall

then you can say with certainty that **all the dominos will fall**.

The "line of dominos" here is in fact some sequence of mathematical statements.
For example, to assert the truth of the binomial theorem:

.. math::

    (x + y)^n = \sum_{i=0}^{n} {n \choose i} x^iy^{n-i}, n = 0, 1, 2, \dots

is to assert the truth of each item of the sequence:

.. math::

    \begin{array}
    \\
    (x + y)^0 &= \sum_{i=0}^{0} {0 \choose i} x^iy^{0-i} \\
    (x + y)^1 &= \sum_{i=0}^{1} {1 \choose i} x^iy^{1-i} \\
    (x + y)^2 &= \sum_{i=0}^{2} {2 \choose i} x^iy^{2-i} \\
    \end{array}

and so on. So if you can:

+ Show that **IF** the \\(k\\)th item in the sequence is true, then
  the \\(k + 1\\)th case must also be true
+ **AND** show that the first item in the sequence is true (when \\(n = 0\\))

then it can be said that the proposed theorem is true for all \\(n \\in \\mathbb{N} \\).


Strong Induction
~~~~~~~~~~~~~~~~

The two parts of an Inductive proof are the **base case** and the **inductive
step**. The base case is, as stated, the proof of the given statement for the
first item in the sequence - typically when \\(n = 0\\) but, in general, when
\\(n\\) is some lowest positive integer. And the inductive step is the assumption
of the \\(k\\)th case and the subsequent proof of the \\(k+1\\)th case.

It may be the case that assumption of the \\(k\\)th case is insufficient in
achieving the inductive step, and so invoking **strong induction** is called
for. With strong induction you assume, not just the \\(k\\)th case, but each case
up to and including the \\(k\\)th.

:see also: `Wikipedia`_, `NRICH`_, `The Method of Descent`_, `proofwiki.org`_

.. _a more nuanced description: https://en.wikipedia.org/wiki/Inductive_reasoning
.. _Wikipedia: https://en.wikipedia.org/wiki/Mathematical_induction
.. _NRICH: http://nrich.maths.org/4718
.. _The Method of Descent: http://mathcircle.berkeley.edu/BMC4/Handouts/induct/node7.html
.. _proofwiki.org: http://www.proofwiki.org/wiki/Equivalence_of_Well-Ordering_Principle_and_Induction


