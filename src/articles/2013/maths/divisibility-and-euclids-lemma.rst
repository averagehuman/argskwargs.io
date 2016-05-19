
Divisibility and Euclid's Lemma
===============================

:date: 2013-05-11
:author: averagehuman
:category: Maths
:tags: Number Theory
:attribution: Cohn

**Attribution:** P. M. Cohn

Basic Definitions
-----------------

Divisibility
::::::::::::

For non-zero integers \\(a\\) and \\(b\\), one says \\(a\\) **divides** \\(b\\) and writes:

.. math::

    a \mid b


whenever \\(a\\) is a **factor** of \\(b\\), which is to say

.. math::

    \exists k \in \mathbb{Z} \text{ such that } b = ka

Greatest Common Divisor
:::::::::::::::::::::::

The **Greatest Common Divisor (GCD)** of two numbers is the largest positive
integer that divides both numbers. We write \\(gcd(a,b)\\) for the GCD of
\\(a\\) and \\(b\\).

Primes
::::::

A **prime number** is an integer \\(p\\) greater than \\(1\\) whose only
positive factors are \\(p\\) and \\(1\\).

Two integers \\(a\\) and \\(b\\) are said to be **coprime** (or **relatively prime**)
and \\(a\\) is said to be prime to \\(b\\), if there is no integer other than
\\(\\pm 1\\) dividing both \\(a\\) and \\(b\\).
For example \\(12\\) and \\(25\\) are coprime though neither is prime.
Clearly, if \\(a\\) and \\(b\\) are coprime, then \\(gcd(a, b) = 1\\).

It may be said that a prime number \\(p\\) is characterised by:

+ \\(p > 1\\)
+ \\(p\\) is relatively prime to all postive integers less than \\(p\\)

Note also that \\(a\\) and \\(0\\) are coprime precisely when \\(a = \\pm 1\\).
This implies in particular that two coprime numbers cannot both be \\(0\\).

Elementary Rules
::::::::::::::::

+ \\(c \\mid b \\text{ and } b \\mid a \\Rightarrow c \\mid a \\text{ (Transitivity)}\\)
+ \\(a \\mid a \\text{ for all } a \\in \\mathbb{Z}\\)
+ \\(a \\mid b \\text{ and } b \\mid a \\Rightarrow a = \\pm{b}\\)
+ \\(b \\mid a_1 \\text{ and } b \\mid a_2 \\Rightarrow b \\mid (a_1 + a_2) \\text{ and } b \\mid (a_1 - a_2)\\)
+ \\(b \\mid a \\Rightarrow b \\mid ac \\text{ for any } c \\in \\mathbb{Z}\\)

Euclid's Lemma
--------------

Euclid's Lemma relates to an integer's prime divisors. To prove it requires a preliminary
theorem.

**Theorem.** Given two integers, \\(a\\) and \\(b\\), there exist integers \\(u\\)
and \\(v\\) such that

.. math::

    au + bv = 1 \iff a \text{ and } b \text{ are coprime}

**Proof.** If \\(au + bv = 1\\) for some \\(u\\) and \\(v\\), then \\(a\\) and \\(b\\) are
necessarily coprime, for any factor common to \\(a\\) and \\(b\\) must, by the
elementary rules above, also divide \\(au + bv = 1\\) and so must be \\(\\pm 1\\).

Conversely, if \\(a\\) and \\(b\\) are coprime, they are not both \\(0\\), and therefore
the set \\(S = \\{am + bn \\mid m,n \\in \\mathbb{Z}\\}\\) contains positive integers,
for example \\(a^2 + b^2\\). Let \\(d\\) be the least positive integer in \\(S\\), say
\\(d = ax + by\\), then the result follows if it can be proved that \\(d = 1\\).

Divide \\(a\\) by \\(d\\) using the `division algorithm`_:

.. math::

    a = dq + r, 0 \leq r < d

Then

.. math::

    r = a - dq = a - (ax + by)q = a(1 -xq) + b(-yq) \in S
    
So \\(r \\in S\\) and \\(0 \\leq r < d\\) and \\(d\\) is the least postive element
in \\(S\\) by definition, therefore it must be that \\(r = 0\\).
This means \\(a = dq\\), ie. \\(d \\mid a\\).

It can similarly be shown that \\(d \\mid b\\), so \\(d\\) is a common factor of \\(a\\)
and \\(b\\), and therefore, since \\(a\\) and \\(b\\) are coprime, \\(d = 1\\). \\(\\Box\\)


**Theorem (Euclid's Lemma)** Let \\(p\\) be prime and \\(a_1, a_2,\\dots,a_n \\in \\mathbb{Z}\\)
such that \\(p \\mid a_1a_2\\cdots a_n\\) then \\(p \\mid a_i\\) for some \\(i=1,\\dots,n\\).

**Proof [P. M. Cohn]:** We prove the contrapositive, ie. if \\(p \\nmid a_i\\) for
\\(i=1,\\dots,n\\) then \\(p \\nmid a_1a_2 \\cdots a_n\\).

For \\(n=1\\) there is nothing to prove, so begin with the case \\(n=2\\). Let
\\(a_1\\) and \\(a_2\\) be given such that \\(p \\nmid a_1\\) and \\(p \\nmid a_2\\), we want
to show that \\(p \\nmid a_1a_2\\).

Since \\(p\\) is prime, it is coprime with both \\(a_1\\) and \\(a_2\\), and therefore by
the previous theorem:

.. math::

    a_1x + py = a_2u + pv = 1

for some \\(x, y, u,v \\in \\mathbb{Z}\\), and so:

.. math::

    1 = (a_1x + py)(a_2u + pv) = a_1a_2xu + p(a_2yu + a_1xv + ypv)

which shows, again by the previous theorem, that \\(a_1a_2\\) and \\(p\\) are coprime,
and so \\(p \\nmid a_1a_2\\) as required.

To demonstrate the general case use induction on \\(n\\), that is, assume \\(n>2\\)
and that the result has been proved for values less than \\(n\\). Now, by
assumption, we have that \\(p \\nmid a_i \\text{ for } i=1,\\dots,n\\), and so:

+ \\(p \\nmid a_n\\) is given
+ \\(p \\nmid a_1 \\cdots a_{n-1}\\) by the induction hypothesis

and it therefore follows by the already proven case \\(n=2\\) that
\\(p \\nmid a_1a_2 \\cdots a_n\\). \\(\\Box\\)

.. _division algorithm: {filename}/articles/2013/maths/euclidean-division.rst

