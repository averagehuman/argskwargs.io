
What is it?
===========

+ A static blog built with `pelican`_
+ Automated build and asset processing via gulp.


Requirements
============

+ npm
+ python

Setup
=====

1. Create and activate a python virtual environment.

   pip install -r requirements.txt

2. Install gulp and associated dependencies:


   npm install


Editing
=======

Build site, watch files and launch nodejs server on localhost:8000::

    make develop


Publishing
==========

Publish site::

    make publish


.. _pelican: http://blog.getpelican.com/
.. _zurb foundation for sites template: https://github.com/zurb/foundation-zurb-template
.. _amazon cloudfront cdn: https://aws.amazon.com/cloudfront/
.. _s3: https://aws.amazon.com/s3/
