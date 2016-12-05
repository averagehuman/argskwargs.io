
Django Angular2 Basic Setup (Part One)
######################################

:date: 2016-12-05 10:00
:category: Django
:author: averagehuman
:tags: javascript, angular


.. container:: callout primary

    Integrating angular2 typescript compilation and browserification with Django static files handling.


A two part post describing an end to end asset production flow for a django/angular2 application.

The first part sets out the django side of managing and serving static browser assets, and the second
part will describe the nodejs tooling required to produce those assets.

Note that this first part outlines a generic approach to handling static files with Django, there's
nothing particular to angular or typescript at this point.

Tested with python3.

Requirements
------------

Create and activate a virtualenv:

.. code-block:: bash

    $ virtualenv --python=python3 django-1.10
    $ source django-1.10/bin/activate

Install django:

.. code-block:: bash

    (django-1.10) $ pip install django<1.11


Django project setup
--------------------

Let's call the project **bluebird** and run the following commands:

.. code-block:: bash

    (django-1.10) $ mkdir bluebird-app && django-admin startproject instance bluebird-app
    (django-1.10) $ cd bluebird-app    && django-admin startapp bluebird

This should have created the following structure:

.. code-block:: bash

    - bluebird-app
        manage.py
        - bluebird
            __init__.py
            models.py
            views.py
        - instance
            __init__.py
            settings.py
            urls.py
            wsgi.py


Client Assets
-------------

Now create the client asset directories:

.. code-block:: bash

    (django-1.10) $ mkdir client/{sass,angular2,dist}

and the django STATIC_ROOT directory:

.. code-block:: bash

    (django-1.10) $ mkdir instance/assets

The directory **client/dist** is where the transpiled sass and typescript files will ultimately
end up as browser-ready css and javascript files. And **instance/assets** is where compressed
and minified versions of these files will be copied by django's collectstatic command.

To support this, update **settings.py** as follows:

.. code-block:: bash

    # source directories containing static files
    STATICFILES_DIRS = [
        os.path.join(BASE_DIR, 'client', 'dist'),
    ]

    # destination directory where static files are copied and from which they are served
    STATIC_ROOT = os.path.join(BASE_DIR, 'instance', 'assets')

At the moment there are no built asset files, so to check that things work as expected, add some
placeholders:

.. code-block:: bash

    (django-1.10) $ echo "h1 {color:blue;text-transform:uppercase}" > client/dist/app.css
    (django-1.10) $ echo "document.write('<h1>bluebird demo</h1>')" > client/dist/app.js


Whitenoise
----------

`Whitenoise`_ is a wsgi middleware component that allows a web application to act as its own asset
origin server without requiring an additional storage layer such as S3. It automatically adds a
content-based hash to the static asset file name and produces a gzip-ped version of that file
whenever there is any value in doing so.

After installing `whitenoise`_, update INSTALLED_APPS in **settings.py** to ensure that the custom
runserver app comes before the staticfiles app:

.. code-block:: bash

    INSTALLED_APPS = [
        ...
        'whitenoise.runserver_nostatic',
        'django.contrib.staticfiles',
        ...
    ]
    
Then add the middleware class before any other middleware except SecurityMiddleware:

.. code-block:: bash

    MIDDLEWARE = [
      'django.middleware.security.SecurityMiddleware',
      'whitenoise.middleware.WhiteNoiseMiddleware',
      ...
    ]

Enable gzip (or brotli) compression:

.. code-block:: bash

    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

And if you are using a CDN:

.. code-block:: bash

    STATIC_HOST = '<your cdn url>' if not DEBUG else ''
    STATIC_URL = STATIC_HOST + '/assets/'

Create a template and view
--------------------------

To check that things are working as expected, create a basic template (**bluebird/templates/index.html**):

.. code-block:: html

    <!DOCTYPE html>
    <html>
        <head>
            <title>Bluebird</title>
            <link rel="stylesheet" href="{% static 'app.css' %}" />
            <script src="{% static 'app.js' %}"></script>
        </head>
        <body>
        </body>
    </html>

and an associated view (**bluebird.views.index**):

.. code-block:: python

    from django.shortcuts import render

    def index(request):
        return render(request, 'index.html')

and url pattern (**instance.urls**):

.. code-block:: python

    from django.conf.urls import url

    import bluebird.views

    urlpatterns = [
        url(r'^$', bluebird.views.index, name='home'),
    ]

Now, when you run ``python manage.py runserver``, you should see a blue uppercase 'BLUEBIRD DEMO' at the
website root.

And if you mimic production by setting DEBUG to False:

.. code-block:: python

    DEBUG = False
    ALLOWED_HOSTS = ['*']

and run ``collectstatic``:

.. code-block:: python

    (django-1.10) $ python manage.py collectstatic

Then the website root should again display the blue uppercase title as before.


.. _whitenoise: http://whitenoise.evans.io/

