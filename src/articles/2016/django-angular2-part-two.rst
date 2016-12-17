

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
place so that ``app.js`` can be made into an angular2 application transpiled from typescript and converted for the
browser. Here I'm using `gulp`_ as primary weapon because I have some familiarity but, as is well known,
there are a number of choices when it comes to javascript build tools.

Caveat Emptor: there's no deep expertise on my part in any of this, it's more a learn as you go exercise.


NodeJS
------

First install `nodejs`_. You could do this via a system package manager or otherwise, but one option that
may suit python developers is to use `nodeenv`_. This is a python utility installable in the usual way:

.. code-block:: bash

    (django-1.10) $ pip install nodeenv

`nodeenv`_ itself can then be used to install a pre-built (the default) or a source-compiled nodejs binary
within the context of the currently active virtual environment, eg.

.. code-block:: bash

    (django-1.10) $ nodeenv -p --node=6.9.1

The ``-p`` option indicates that you want to associate node with a python virtualenv, and ``6.9.1`` being the
latest nodejs LTS at the time of writing.

Now, once the virtual environment is activated, both the ``node`` and the ``npm`` in your ``$PATH`` will
be those associated with that environment, and you can achieve the same essential isolation of javascript
packages as for python packages.

.. code-block:: bash

    (django-1.10) $ which node
    <path to virtualenv>/bin/node
    (django-1.10) $ which npm
    <path to virtualenv>/bin/npm


Typescript
----------

Next install the Typescript compiler ``tsc``:

.. code-block:: bash

    (django-1.10) $ npm -g install typescript
    (django-1.10) $ which tsc
    <path to virtualenv>/bin/tsc

And as a "Hello World" application, let's create an Elizabethan insult generator!

Hello Thou Mewling Flap-mouthed Canker-blossom!!
++++++++++++++++++++++++++++++++++++++++++++++++

Start by creating a ``tsconfig.json`` file:

.. code-block:: bash

    (django-1.10) $ tsc --init
    message TS6071: Successfully created a tsconfig.json file.


Then create the following as ``client/src/insults.ts``

.. code-block:: typescript

    export class Insults {
        static adj1 = [
            "beslubbering", "bawdy", "greasy", "hideous", "knavish", "lazy",
            "mewling", "puny", "reekish", "villainous"
        ];

        static adj2 = [
            "clay-brained", "distempered", "dull-witted", "flap-mouthed", "gorbellied",
            "half-faced", "ill-bred", "lily-livered", "pig-faced", "purple-nosed",
            "shag-eared", "slack-jawed", "sour-faced", "swag-bellied", "whey-faced"
        ];

        static nouns = [
            "boil", "carbuncle", "canker-blossom", "clot", "codpiece", "dog", "dunce",
            "fat guts", "fool", "harpy", "harlot", "lout", "maggot", "malignancy",
            "measle", "miscreant", "mongrel", "mumbler", "scut", "stinkhorn",
            "strumpet", "toad", "weasel"
        ];

        static random() {
            var a = Insults.adj1[Math.floor(Math.random() * Insults.adj1.length)];
            var b = Insults.adj2[Math.floor(Math.random() * Insults.adj2.length)];
            var c = Insults.nouns[Math.floor(Math.random() * Insults.nouns.length)];
            return `${a} ${b} ${c}`
        }
    }

And call this from ``client/src/main.ts``:

.. code-block:: typescript

    import { Insults } from "./insults";

    console.log(Insults.random())

Now compile:

.. code-block:: bash

    (django-1.10) $ tsc

This should have created ``client/src/main.js`` which can be run directly with ``node``:

.. code-block:: bash

    (django-1.10) $ for i in {1..10};do node client/src/main.js; done
    hideous half-faced harlot
    mewling flap-mouthed mumbler
    beslubbering gorbellied malignancy
    bawdy swag-bellied strumpet
    puny shag-eared canker-blossom
    knavish ill-bred varlot
    reekish distempered scut
    villainous purple-nosed harpy
    lewd lily-livered lout
    lazy sour-faced barnacle


Gulp
----

Next install `yarn`_ package manager (an alternative to `npm`_) and the `gulp CLI`_:

.. code-block:: bash

    (django-1.10) $ npm install -g yarn gulp-cli


And create a ``package.json`` for the application. For example, via ``yarn init``:

.. code-block:: bash

    (django-1.10) $ yarn init
    yarn init v0.17.10
    question name (bluebird-app):
    question version (1.0.0): 
    question description: Angular2 demo
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

    "devDependencies": {
      "browserify": "^13.1.1",
      "gulp": "^3.9.1",
      "gulp-sourcemaps": "^1.9.1",
      "gulp-typescript": "^3.1.3",
      "gulp-uglify": "^2.0.0",
      "tsify": "^2.0.3",
      "typescript": "^2.1.4",
      "vinyl-buffer": "^1.0.0",
      "vinyl-source-stream": "^1.1.0"
    }

And install these packages with ``yarn``:

.. code-block:: bash

    (django-1.10) $ yarn install

App Dependencies
++++++++++++++++

For the angular application itself, update ``package.json`` directly with the following ``dependencies``
field taken from the `angular2 quickstart`_:

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

Again, install these packages with ``yarn``:

.. code-block:: bash

    (django-1.10) $ yarn install

.. _Managing and serving static browser assets with Django: {filename}django-angular2-part-one.rst
.. _gulp: http://gulpjs.com/
.. _gulp cli: https://github.com/gulpjs/gulp-cli
.. _yarn: https://yarnpkg.com/
.. _nodejs: https://nodejs.org
.. _npm: https://www.npmjs.com/
.. _typescript gulp docs: https://www.typescriptlang.org/docs/handbook/gulp.html
.. _angular2 quickstart: https://github.com/angular/quickstart
.. _nodeenv: https://pypi.python.org/pypi/nodeenv

