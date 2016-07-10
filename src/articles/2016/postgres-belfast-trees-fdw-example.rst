
Postgres Foreign Data Wrapper Example
#####################################

:date: 2016-05-31 08:00
:category: Postgres
:author: gmflanagan
:draft: true


Examples
--------

.. code-block:: sql

    SELECT earth_distance(ll_to_earth(latitude, longitude), ll_to_earth())
    FROM belfast_trees
    WHERE speciestype = 'Tulip';


