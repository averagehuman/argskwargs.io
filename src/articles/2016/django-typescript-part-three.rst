
Django, Typescript, Gulp (Part Three)
########################################

:date: 2016-12-30 18:00
:category: Javascript
:author: averagehuman
:summary: Integrating typescript compilation and browserification with Django static files handling (Part Three).


.. container:: callout primary

    Combining Typescript compilation with Django static files handling.

    1. `Managing static browser assets with Django`_
    2. `Compiling and converting Typescript`_
    3. Automating with Gulp


The goal now is to set up a build pipeline to run the Typescript to Browser conversion process,
and to have this pipeline run automatically whenever any source file changes. Here I'm using `gulp`_ but,
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


gulpfile.js
-----------

Now create the config file required to drive gulp - ``gulpfile.js``. This can be tailored to taste,
but a minimal working example is:

.. code-block:: bash

    var gulp = require("gulp");
    var browserify = require("browserify");
    var source = require('vinyl-source-stream');
    var tsify = require("tsify");


    var build = function(cfg) {
        return browserify({
            basedir: '.',
            debug: cfg.debug,
            entries: ['client/src/main.ts'],
            cache: {},
            packageCache: {}
        })
        .plugin(tsify)
        .bundle()
        .pipe(source('app.js'))
        .pipe(gulp.dest("client/dist"));
    }


    gulp.task("debug", function () {
        return build({debug: true})
    });


    gulp.task("build", function () {
        return build({debug: false})
    });

(All these config files - tsconfig.json, package.json and gulpfile.js - should be in the same directory as manage.py).

Now calling either ``gulp build`` or ``gulp debug`` will run the Typescript to Javascript conversion to
produce the required ``client/dist/app.js``.


Rebuild on changes
------------------

To re-run the build when any Typescript file changes, create a further file watch task:

.. code-block:: bash

    gulp.task("watch", function () {
        gulp.watch(['client/src/**/*.ts'], ['debug']);
    });


which says: if any Typescript file in any directory in the source hierarchy changes, then run the debug build.

Also create a default task which will run an initial build before starting the watch task:

.. code-block:: bash

    gulp.task("default", ["debug"], function() {
        gulp.start('watch')
    });


So now a plain ``gulp`` command will begin the build/rebuild cycle:

.. code-block:: bash

    (django-1.10) [git:master] $ gulp
    [10:36:51] Using gulpfile ~/working/blog.git/src/code/django-static/bluebird-app/gulpfile.js
    [10:36:51] Starting 'debug'...
    [10:36:53] Finished 'debug' after 1.45 s
    [10:36:53] Starting 'default'...
    [10:36:53] Starting 'watch'...
    [10:36:53] Finished 'watch' after 13 ms
    [10:36:53] Finished 'default' after 14 ms
    ...


And you are now free to hack on the Typescript app without having to manually go through the
compile/browserify steps.


Live Browser Reload
-------------------

A final development nicety is live-reload, ie. whenever any static file being served by the Django/whitenoise
server changes, it would be good to have the browser automatically refresh in order to pick
up the new file.

First install the `gulp-livereload`_ package:

.. code-block:: bash

    $ yarn add gulp-livereload --dev

And require this in the gulpfile:

.. code-block:: bash

    var livereload = require('gulp-livereload');

Next, update the ``watch`` task to start the livereload server listening on a particular port and watch
the built javascript bundle ``app.js``:

.. code-block:: bash

    gulp.task("watch", function () {
        livereload.listen(32700);
        gulp.watch(['client/dist/app.js']).on('change', livereload.changed)
        gulp.watch(['client/src/**/*.ts'], ['debug']);
    });

And update the ``index.html`` template with a script tag as follows:

.. code-block:: htmldjango

    {% load static %}
    <!DOCTYPE html>
    <html>
        <head>
            <title>Bluebird</title>
            <link rel="stylesheet" href="{% static 'app.css' %}" />
            <script type="text/javascript" src="http://127.0.0.1:32700/livereload.js"></script>
            <script src="{% static 'app.js' %}"></script>
        </head>
        <body>
        </body>
    </html>

Now any change to a Typescript file should run the build *and* reload any browser page viewing this page.

(There are also livereload browser extensions and desktop integrations if you want to avoid the script tag).

The final ``gulpfile.js``:

.. code-block:: javascript

    var gulp = require("gulp");
    var browserify = require("browserify");
    var source = require('vinyl-source-stream');
    var tsify = require("tsify");
    var livereload = require('gulp-livereload');


    var build = function(cfg) {
        return browserify({
            basedir: '.',
            debug: cfg.debug,
            entries: ['client/src/main.ts'],
            cache: {},
            packageCache: {}
        })
        .plugin(tsify)
        .bundle()
        .pipe(source('app.js'))
        .pipe(gulp.dest("client/dist"));
    }


    gulp.task("debug", function () {
        return build({debug: true})
    });


    gulp.task("build", function () {
        return build({debug: false})
    });


    gulp.task("watch", function () {
        livereload.listen(32700);
        gulp.watch(['client/src/**/*.ts'], ['debug']);
        gulp.watch(['client/dist/app.js']).on('change', livereload.changed)
    });


    gulp.task("default", ["debug"], function() {
        gulp.start('watch')
    });

See Also
--------

+ https://blog.mozilla.org/webdev/2016/05/27/django-pipeline-and-gulp/
+ http://www.revsys.com/blog/2014/oct/21/ultimate-front-end-development-setup/


.. _Managing static browser assets with Django: {filename}django-typescript-part-one.rst
.. _Compiling and converting Typescript: {filename}django-typescript-part-two.rst
.. _gulp: http://gulpjs.com/
.. _gulp cli: https://github.com/gulpjs/gulp-cli
.. _yarn: https://yarnpkg.com/
.. _nodejs: https://nodejs.org
.. _npm: https://www.npmjs.com/
.. _typescript gulp docs: https://www.typescriptlang.org/docs/handbook/gulp.html
.. _angular2 quickstart: https://github.com/angular/quickstart
.. _gulp-livereload: https://github.com/vohof/gulp-livereload

