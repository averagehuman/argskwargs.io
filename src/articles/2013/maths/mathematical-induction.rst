
Mathematical Induction
======================

:date: 2013-04-27
:author: averagehuman
:category: maths

Scientific Inference
--------------------

Deduction reasons from the general to the particular, while induction or inference
reasons from the particular to the general.

Deduction
~~~~~~~~~

Given that:

1. All men are mortal [General Truth]
2. Socrates is a man [Particular Truth]

Then a further truth - that Socrates is mortal - necessarily follows.

Induction
~~~~~~~~~

Given that a particular truth holds for each element in a given subset of a
collection, it may be reasonable to induce or infer the probability that the truth
is universal, ie. that it likely holds for every element in the collection.

1. If all the biological life forms that we know of depend on liquid water to exist.
2. It is likely that all biological life depends on liquid water to exist.

One difference between the two forms of reasoning is that a deductive
argument can be proved or disproved, but an inductive argument can only
be disproved since, no matter how many facts are gathered supporting a
thesis, there is always the possibility of new evidence which goes against
it.


Mathematical Induction
----------------------

Mathematical Induction has a stricter definition and shouldn't be confused
with the more general scientific method. A good informal analogy is a line
of up-ended dominos - if you can show that:

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


