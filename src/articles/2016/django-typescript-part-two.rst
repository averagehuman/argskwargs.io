
Django, Typescript, Gulp (Part Two)
######################################

:date: 2016-12-11 10:00
:category: Javascript
:author: averagehuman
:summary: Integrating typescript compilation and browserification with Django static files handling (Part Two).


.. container:: callout primary

    Combining Typescript compilation with Django static files handling.

    1. `Managing static browser assets with Django`_
    2. Compiling and converting Typescript
    3. `Automating with Gulp`_


So the previous post describes setting up a skeleton Django app serving a placeholder ``app.js``. Now
we set up the tooling required to convert Typescript to browser-ready javascript.

NodeJS
------

First install `nodejs`_. You could do this via a system package manager or otherwise, but one option that
may suit python developers is to use `nodeenv`_. This is a python utility installable in the usual way:

.. code-block:: bash

    (django-1.10) $ pip install nodeenv

`nodeenv`_ can then be used to install a pre-built (the default) or a source-compiled nodejs binary
within the context of the currently active virtual environment, eg.

.. code-block:: bash

    (django-1.10) $ nodeenv -p --node=6.9.1

The ``-p`` option indicates that you want to associate node with a python virtualenv, and ``6.9.1`` is the
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


And create a configuration file for the project (``tsconfig.json``):

.. code-block:: bash

    (django-1.10) $ tsc --init --rootDir ./client/src
    message TS6071: Successfully created a tsconfig.json file.


Now, as a first typescript program, an insult generator!  Start by creating
the following as ``client/src/insults.ts``

.. code-block:: javascript

    export class Insults {
        static adj1 = [
            "beslubbering", "bawdy", "cretinous", "dribbling", "foetid", "greasy",
            "grotesque", "hideous", "knavish", "lazy", "mewling", "puny", "pungent",
            "rank", "reekish", "slimy", "villainous", "weedy"
        ];

        static adj2 = [
            "boil-ridden", "clay-brained", "distempered", "dull-witted", "flap-mouthed",
            "gorbellied", "half-brained", "half-faced", "ill-bred", "lily-livered",
            "pig-faced", "purple-nosed", "shag-eared", "slack-jawed", "sour-faced",
            "swag-bellied", "whey-faced"
        ];

        static nouns = [
            "carbuncle", "canker-blossom", "clot", "codpiece", "dog", "dunce",
            "fat guts", "fool", "harpy", "harlot", "loon", "lout", "maggot",
            "malignancy", "measle", "miscreant", "mongrel", "mumbler", "old cow",
            "scut", "stinkhorn", "strumpet", "old toad", "weasel"
        ];

        static random() {
            var a = Insults.adj1[Math.floor(Math.random() * Insults.adj1.length)];
            var b = Insults.adj2[Math.floor(Math.random() * Insults.adj2.length)];
            var c = Insults.nouns[Math.floor(Math.random() * Insults.nouns.length)];
            return `${a} ${b} ${c}`
        }
    }

And call this from ``client/src/main.ts``:

.. code-block:: javascript

    import { Insults } from "./insults";

    console.log(Insults.random())

Now compile:

.. code-block:: bash

    (django-1.10) $ tsc

This should have created ``client/src/main.js`` which can be run directly with ``node``:

.. code-block:: bash

    (django-1.10) $ node client/src/main.js
    mewling flap-mouthed mumbler
    (django-1.10) $ node client/src/main.js
    beslubbering gorbellied malignancy
    (django-1.10) $ node client/src/main.js
    bawdy swag-bellied strumpet
    (django-1.10) $ node client/src/main.js
    villainous purple-nosed fool
    (django-1.10) $ node client/src/main.js
    hideous half-faced harlot

etc.


Browserify
----------

The javascript created by ``tsc``, while comprehensible to ``node``, will not run directly in the browser.
So to remedy this you need a "browserification" step.

First, change ``main.js`` so that it's easier to check the result, replacing ``console.log`` with ``document.write``:

.. code-block:: javascript

    import { Insults } from "./insults";
    
    var insult = Insults.random();

    document.write(`<h1>${insult}</h1>`);

Next, install ``browserify``:

.. code-block:: bash

    (django-1.10) $ npm -g install browserify
    ...

    (django-1.10) $ which browserify
    <path to virtualenv>/bin/browserify

And run it against ``main.js`` to produce the browser-ready ``app.js``:

.. code-block:: bash

    (django-1.10) $ browserify client/src/main.js -o client/dist/app.js


Now, presuming you still have the Django dev server running from the `earlier post`_ (or have restarted
it with ``python manage.py runserver``), go to localhost:8000 where you should see a new insult displayed
on every page refresh.


.. raw:: html

    <div style="color:blue;text-transform:uppercase;font-size:26px;text-align:center">
        <div>Slimy swag-bellied old toad</div>
        <div>Rank sour-faced maggot</div>
        <div>Reekish half-brained loon</div>
        <div>...</div>
    </div>

The final step then is to `automate this compilation/browserification procedure with Gulp`_.

.. _Managing static browser assets with Django: {filename}django-typescript-part-one.rst
.. _earlier post: {filename}django-typescript-part-one.rst
.. _automating with gulp: {filename}django-typescript-part-three.rst
.. _automate this compilation/browserification procedure with gulp: {filename}django-typescript-part-three.rst
.. _gulp: http://gulpjs.com/
.. _gulp cli: https://github.com/gulpjs/gulp-cli
.. _yarn: https://yarnpkg.com/
.. _nodejs: https://nodejs.org
.. _npm: https://www.npmjs.com/
.. _typescript gulp docs: https://www.typescriptlang.org/docs/handbook/gulp.html
.. _angular2 quickstart: https://github.com/angular/quickstart
.. _nodeenv: https://pypi.python.org/pypi/nodeenv

