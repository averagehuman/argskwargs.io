

Django Angular2 Basic Setup (Part Two)
######################################

:date: 2016-12-11 10:00
:category: Javascript
:author: averagehuman
:tags: javascript, angular
:summary: Angular2 typescript compilation and browserification with Django static files handling (Part Two).


.. container:: callout primary

    Integrating angular2 typescript compilation and browserification with Django static files handling.

    1. `Managing and serving static browser assets with Django`_
    2. Typescript processing with gulp and yarn


So the previous post describes setting up a skeleton Django app with a placeholder ``app.js`` being served from
the project's ``STATIC_ROOT``. Next comes the descent into madness ;-) where the build infrastucture is put in
place so that we can make ``app.js`` an angular2 application transpiled from typescript and converted for the
browser. Here I'm using `gulp`_ as the primary weapon because I have some familiarity but, as is well known,
there are a number of choices when it comes to javascript build tools.

Caveat Emptor: there's no deep expertise on my part in any of this, it's more a learn as you go exercise.


nodeenv
-------

First install `nodejs`_. You could do this via a system package manager or otherwise, but one option that
may suit python developers is to use `nodeenv`_. This is a python utility installable in the usual way:

.. code-block:: bash

    (django-1.10) $ pip install nodeenv

`nodeenv`_ itself can then be used to install a pre-built (the default) or a source-compiled nodejs binary
within the context of the currently active virtual environment, eg.

.. code-block:: bash

    (django-1.10) $ nodeenv --python-virtualenv --node=6.9.1

``6.9.1`` being the latest nodejs LTS as of the time of writing.

Now, once the virtual environment is activated, both the ``node`` and the ``npm`` in your ``$PATH`` will
be those associated with that environment, and you achieve the same essential isolation of javascript
packages as for python packages.


Requirements
------------

Global Dependencies
+++++++++++++++++++

There are two required global packages: `yarn`_ package manager and the `gulp CLI`_:

.. code-block:: bash

    (django-1.10) $ npm install -g yarn gulp-cli


Dev Dependencies
++++++++++++++++

Following the `typescript gulp docs`_, the build machinery can now be installed with:

.. code-block:: bash

    (django-1.10) $ yarn add --dev typescript gulp gulp-typescript gulp-uglify gulp-sourcemaps
    (django-1.10) $ yarn add --dev typescript browserify tsify vinyl-source-stream vinyl-buffer


App Dependencies
++++++++++++++++

And based on the `angular2 quickstart code`_ app dependencies can be added directly to ``package.json``:

.. code-block:: bash

    "dependencies": {
      "@angular/common": "^2.3.0",
      "@angular/compiler": "^2.3.0",
      "@angular/core": "^2.3.0",
      "@angular/forms": "^2.3.0",
      "@angular/http": "^2.3.0",
      "@angular/platform-browser": "^2.3.0",
      "@angular/platform-browser-dynamic": "^2.3.0",
      "@angular/router": "^3.3.0",
      "angular-in-memory-web-api": "~0.1.17",
      "systemjs": "0.19.40",
      "core-js": "^2.4.1",
      "reflect-metadata": "^0.1.8",
      "rxjs": "5.0.0-rc.4",
      "zone.js": "^0.7.2"
    }

Followed by:

.. code-block:: bash

    (django-1.10) $ yarn install

.. _Managing and serving static browser assets with Django: {filename}django-angular2-part-one.rst
.. _gulp: http://gulpjs.com/
.. _gulp cli: https://github.com/gulpjs/gulp-cli
.. _yarn: https://yarnpkg.com/
.. _nodejs: https://nodejs.org
.. _typescript gulp docs: https://www.typescriptlang.org/docs/handbook/gulp.html
.. _angular2 quickstart code: https://github.com/angular/quickstart
.. _nodeenv: https://pypi.python.org/pypi/nodeenv

