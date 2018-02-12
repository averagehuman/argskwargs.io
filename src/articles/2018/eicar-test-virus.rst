
Testing Anti-Virus Software With EICAR
######################################

:date: 2018-02-12 14:00
:category: Testing
:author: averagehuman
:summary: Quickly sanity check that anti-virus scanners are active


.. container:: callout primary

    How to check that anti-virus software is active using the EICAR test virus


The EICAR Test Virus is a short text file developed by the `European Institute for Computer Anti-Virus Research (EICAR)`_
for testing anitvirus software. It is a valid DOS program and produces sensible
results when run (it prints EICAR-STANDARD-ANTIVIRUS-TEST-FILE!), but it is
entirely safe.

All correctly functioning virus scanners should flag EICAR as a malicious file. 
Whether a file that only *contains* the test virus text will be considered
malicious may be product-dependent, but I have observed that Sophos will do so
at least.


The EICAR virus is:

.. code-block:: bash

    X5O!P%@AP[4\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*


(The third character is a capital letter O not a zero).

Programmatic Checks
-------------------

There may be a slight difficulty when using the EICAR virus in a program or script because
the script itself, once written to disk, can then be deleted or quarantined by
the very virus scanner that you are trying to check...  But this is easy enough to work
around: store the EICAR text in encoded form and decode on the fly as needs be.


For example, in bash say, decode from ROT13 as follows:

.. code-block:: bash

    $ echo 'K5B!C%@NC[4\CMK54(C^)7PP)7}$RVPNE-FGNAQNEQ-NAGVIVEHF-GRFG-SVYR!$U+U*' | tr '[A-Za-z]' '[N-ZA-Mn-za-m]' > EICAR.COM


And to test uploading malicious files to a web server, get curl to
read the decoded file from stdin rather than disk:


.. code-block:: bash

    $ EICAR=$(echo 'K5B!C%@NC[4\CMK54(C^)7PP)7}$RVPNE-FGNAQNEQ-NAGVIVEHF-GRFG-SVYR!$U+U*' | tr '[A-Za-z]' '[N-ZA-Mn-za-m]')
    $ echo -n "$EICAR" | curl -s -i -X POST -F "file=@-;filename=image.png" http://<SOME URL>

The key here is ``file=@-``, which causes curl to read from stdin. 'file' is just the name
of the form field expected by the web server.



.. _European Institute for Computer Anti-Virus Research (EICAR): http://www.eicar.org

