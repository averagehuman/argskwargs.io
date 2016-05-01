
Development Blog


+ A static blog built with `pelican`_
+ Build harness based on `Zurb Foundation for Sites Template`_ (sass, gulp, ...)
+ Auto-rebuild and live browser reload when content, templates or styles change.
+ Hosted via `Amazon Cloudfront CDN`_ and `S3`_


Setup
=====

Download and install nodejs, create a virtualenv, install node and python requirements::

   make install


Editing
=======

Build site, watch files and launch nodejs server on localhost:8079::

    make develop


Publishing
==========

Publish site::

    make publish


.. _pelican: http://blog.getpelican.com/
.. _zurb foundation for sites template: https://github.com/zurb/foundation-zurb-template
.. _amazon cloudfront cdn: https://aws.amazon.com/cloudfront/
.. _s3: https://aws.amazon.com/s3/
