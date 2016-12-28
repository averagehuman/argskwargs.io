

Django, Typescript, Gulp (Part Three)
########################################

:date: 2016-12-18 18:00
:category: Javascript
:author: averagehuman
:summary: Integrating typescript compilation and browserification with Django static files handling (Part Three).


.. container:: callout primary

    Combining Typescript compilation with Django static files handling.

    1. `Managing static browser assets with Django`_
    2. `Compiling and converting Typescript`_
    3. Automating with Gulp


The goal now is to set up a build pipeline to run the Typescript to Browser conversion process, and to have this
pipeline run automatically whenever any source file changes. Here I'm using `gulp`_ to do the heavy lifting but,
as is well known, there are other javascript build tools.


Yarn and package.json
---------------------

Install `yarn`_ package manager (an alternative to `npm`_) and the `gulp CLI`_:

.. code-block:: bash

    (django-1.10) $ npm install -g yarn gulp-cli


And create a ``package.json`` for the application. For example, via ``yarn init``:

.. code-block:: bash

    (django-1.10) $ yarn init
    yarn init v0.17.10
    question name (bluebird-app):
    question version (1.0.0): 
    question description: Typescript Demo
    question entry point (index.js):
    question git repository: 
    question author: argskwargs
    question license (MIT): 
    success Saved package.json

Dev Dependencies
++++++++++++++++

Following the `typescript gulp docs`_, the build machinery can be installed by adding a ``devDependencies``
field to ``package.json`` such as:

.. code-block:: bash

    {
      "name": "bluebird-client",
      "version": "1.0.0",
      "description": "Typescript Demo",
      "main": "main.js",
      "author": "argskwargs",
      "license": "MIT",
      "devDependencies": {
          "browserify": "^13.1.1",
          "gulp": "^3.9.1",
          "gulp-sourcemaps": "^1.9.1",
          "gulp-typescript": "^3.1.3",
          "tsify": "^2.0.3",
          "typescript": "^2.1.4",
          "vinyl-buffer": "^1.0.0",
          "vinyl-source-stream": "^1.1.0"
        }
    }

Then install all these packages together with:

.. code-block:: bash

    (django-1.10) $ yarn install

.. _Managing static browser assets with Django: {filename}django-typescript-part-one.rst
.. _Compiling and converting Typescript: {filename}django-typescript-part-two.rst
.. _gulp: http://gulpjs.com/
.. _gulp cli: https://github.com/gulpjs/gulp-cli
.. _yarn: https://yarnpkg.com/
.. _nodejs: https://nodejs.org
.. _npm: https://www.npmjs.com/
.. _typescript gulp docs: https://www.typescriptlang.org/docs/handbook/gulp.html
.. _angular2 quickstart: https://github.com/angular/quickstart
