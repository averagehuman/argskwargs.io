
Belfast Trees Database (Part One)
#################################

:date: 2016-05-30 08:00
:category: Postgres
:author: averagehuman
:tags: opendatani


Being but men, we catalogue trees.

To get a csv list of around 38000 Belfast trees from the `opendatani`_ web site you
can simulate clicking the download button with curl:

.. code-block:: bash

    $ curl -G -L -A "Mozilla/5.0 (X11; Linux x86_64)" \
          http://www.belfastcity.gov.uk/nmsruntime/saveasdialog.aspx?lID=14543&sID=2430

or use the data api, sending a query such as:

.. code-block:: bash

    {'sql': 'SELECT * from "b501ba21-e26d-46d6-b854-26a95db78dd9"'}

as an encoded querystring parameter to the api endpoint.

The returned data is in JSON format so there needs to be further processing to convert
to CSV - see the script below. The point of converting to CSV is so that the file can
be used as a `Foreign Data Wrapper`_ in postgres; there are FDWs for JSON web
apis but these need separate compilation, whereas the CSV data wrapper is builtin.

Visualisation
=============

The Open Data Institute has a map visualisation of all the trees:
http://belfast.theodi.org/2015/07/29/city-open-data/


get_belfast_trees_csv.py
========================

[[ gist averagehuman:baadeb24e717231b2acdd1d86b861769 ]]


In the `next post`_ the csv file is set up as a `foreign data wrapper`_ so that it can be
more easily queried.

.. _being but men: http://www.poemhunter.com/best-poems/dylan-thomas/being-but-men/
.. _opendatani: https://www.opendatani.gov.uk/
.. _foreign data wrapper: https://wiki.postgresql.org/wiki/Foreign_data_wrappers
.. _next post: {filename}belfast-trees-part-two.rst

