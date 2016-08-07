
Belfast Trees Database (Part Two)
#################################

:date: 2016-05-31 08:00
:category: Postgres
:author: averagehuman
:tags: opendatani


A Foreign Data Wrapper (FDW) in `postgres`_ is a way of making an external data
source appear to be an internal database table. Some FDWs, in addition to making
the external data readable, also allow updating the data source (if that makes
sense and if privileges permit).

There are some builtin FDWs, for example, `postgres-fdw`_ which allows access to
other postgres servers, and `file-fdw`_ which enables read-access to CSV files.

Some third-party Foreign Data Wrappers include `mongo_fdw`_ for mongodb, `pg-es-fdw`_
for Elasticsearch and `www_fdw`_ for accessing JSON and XML webservices. These
require separate compilation.

Trees CSV as a Foreign Data Wrapper
===================================

As an example of accessing a CSV file as an external data source, we can use the
Belfast Trees catalogue from `a previous post`_.

Create a new database called *nidata* and in the **psql** shell create the
required extensions:

.. code-block:: sql

	==> \connect nidata;
	==> CREATE EXTENSION file_fdw;
	==> CREATE EXTENSION cube;
	==> CREATE EXTENSION earthdistance;

On debian/ubuntu, if these extensions aren't available then you may need to install
the postgresql-contrib package:

.. code-block:: bash

    $ sudo apt-get install postgresql-contrib

Next create a foreign server connection called *nidata_files*:

.. code-block:: sql

	==> CREATE SERVER nidata_files FOREIGN DATA WRAPPER file_fdw;

and some custom enumerations:

.. code-block:: sql

	==> CREATE TYPE tree_condition AS ENUM ('N/A', 'Dead', 'Dying', 'Very Poor', 'Poor', 'Fair', 'Good');
	==> CREATE TYPE tree_age AS ENUM ('Juvenile', 'Young', 'Young Mature', 'Semi-Mature', 'Mature', 'Fully Mature');
	==> CREATE TYPE tree_vigour AS ENUM ('N/A', 'Low', 'Normal');

Now create the foreign table, assuming the tree database is called 'trees.csv' and
has a header row:

.. code-block:: sql

	==> CREATE FOREIGN TABLE belfast_trees (
	==>     typeoftree VARCHAR(50), speciestype VARCHAR(30), species VARCHAR(80),
	==>     age tree_age, description VARCHAR(140), treesurround VARCHAR(80),
	==>     vigour tree_vigour, condition tree_condition, diameter REAL,
	==>     spreadradius REAL, longitude REAL, latitude REAL, treetag INTEGER,
	==>     treeheight REAL)
	==> SERVER nidata_files
	==> OPTIONS (format 'csv', header 'true', filename 'trees.csv', delimiter ',', null '');

Queries
=======

Now you can query the data and ask questions.

Order trees by distance from city centre (54.596787, -5.930106)
---------------------------------------------------------------

.. code-block:: sql

    ==> SELECT age,
               speciestype,
               earth_distance(ll_to_earth(latitude, longitude), ll_to_earth(54.596787, -5.930106)) as radius
        FROM belfast_trees
        ORDER BY radius ASC

Where is the tree furthest from the city centre?
------------------------------------------------

.. code-block:: sql

    ==> SELECT age,
               speciestype,
               earth_distance(ll_to_earth(latitude, longitude), ll_to_earth(54.596787, -5.930106)) as radius
        FROM belfast_trees
        ORDER BY radius DESC
        LIMIT 1;

        latitude | longitude |      radius      
        ----------+-----------+------------------
        54.5352 |  -5.98286 | 7654.26520668973

(which Google maps gives as the Upper Malone Road at Drumbeg).

How many dead trees?
--------------------

.. code-block:: sql

    ==> select count(*) from belfast_trees where condition = 'Dead';
    count 
    -------
    35

How many trees are Very Poor, Poor, Dying or Dead?
--------------------------------------------------

.. code-block:: sql

    ==> select count(*) from belfast_trees where condition < 'Fair' and condition > 'N/A';
    count 
    -------
    1184

How does condition relate to age?
---------------------------------

.. code-block:: sql

    ==> select count(*) from belfast_trees where age <= 'Young' and condition < 'Fair';
    count 
    -------
    535

    ==> select count(*) from belfast_trees where age >= 'Mature' and condition < 'Fair';
    count 
    -------
    174

So there are more Young trees in poor condition than Mature or Fully Mature trees in poor
condition.

And so on.

.. _postgres: https://www.postgresql.org/
.. _postgres-fdw: https://www.postgresql.org/docs/9.3/static/postgres-fdw.html
.. _file-fdw: https://www.postgresql.org/docs/9.3/static/file-fdw.html
.. _mongo_fdw: https://github.com/EnterpriseDB/mongo_fdw
.. _pg-es-fdw: https://github.com/Mikulas/pg-es-fdw
.. _www_fdw: https://github.com/cyga/www_fdw
.. _pgxn.org: http://pgxn.org/tag/fdw/
.. _opendatani: https://www.opendatani.gov.uk/
.. _a previous post: {filename}belfast-trees-part-one.rst

