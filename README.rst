Shop e-Comerce
====
.. image:: https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter
     :target: https://github.com/pydanny/cookiecutter-django/
     :alt: Built with Cookiecutter Django
.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
     :target: https://github.com/ambv/black
     :alt: Black code style


.. image:: https://github.com/bsperezb/Django-Ecomerce/blob/main/gif_portada.gif


:License: MIT
====



**Hi, welcome to my eComerce website Project.**

This project was developed with Python 3.9, Django 3.1.13, Postgresql 12.6, Wompi and CookieCutter.

In this project you can add items to the store as administrator, manage user accounts, make and edit orders of different quantities of products, make online payments with Wompi and manage refunds



Running project local with docker (option 1)
--------------
This project can be used immediately with docker and docker compose.


Prerequisites
^^^^^^^^^^^^^^^^^^^^^

* Docker; if you don’t have it yet, follow the installation instructions_.
.. _instructions: https://docs.docker.com/get-docker/;

* Docker Compose; refer to the official documentation_ for the installation guide.
.. _documentation: https://docs.docker.com/get-docker/;

* Pre-commit (optional); refer to the official documentation for the installation guide_.
.. _guide: https://pre-commit.com/



Build the stack
^^^^^^^^^^^^^^^^^^^^^

This can take a while, especially the first time you run this particular command on your development system:
::

    $ docker-compose -f local.yml build

Run the stack
^^^^^^^^^^^^^^^^^^^^^

This brings up both Django and PostgreSQL. The first time it is run it might take a while to get started, but subsequent runs will occur quickly.

Open a terminal at the project root and run the following for local development:
::

    $ docker-compose -f local.yml up

Execute Management Commands
^^^^^^^^^^^^^^^^^^^^^

As with any shell command that we wish to run in our container, this is done using the ``docker-compose -f local.yml run --rm command`` :
::

    $ docker-compose -f local.yml run --rm django python manage.py migrate

    $ docker-compose -f local.yml run --rm django python manage.py createsuperuser


Running locally (option 2)
--------------

Prerequisites
^^^^^^^^^^^^^^^^^^^^^

* Python 3.9

* Postgresql 12.6

installs and activates dependencies
^^^^^^^^^^^^^^^^^^^^^

Create a virtual enviroment:
::
    $ python3.9 -m venv <virtual env path>

Activate the virtual enviroment:
::
    $ source <virtual env path>/bin/activate

Install development requirements:
::
    $ cd <what you have entered as the project_slug at setup stage>

    $ pip install -r requirements/local.txt

    $ pip install -r requirements/base.txt

    $ pip install -r requirements/production.txt


Database configuration
^^^^^^^^^^^^^^^^^^^^^

Create a new PostgreSQL database using createdb, where **shop** is the database name and **<password>** is the password of your postgres account:
::
    $ createdb shop -U postgres --password <password>

Apply migrations and create super user:
::
    $ python manage.py migrate
    $ python manage.py createsuperuser

Run:
::
    $ python manage.py runserver


Use the App
--------------

To create a **normal user account**, just go to Sign Up and fill out the form. Once you submit it, you'll see a "Verify Your E-mail Address" page. Go to your console to see a simulated email verification message. Copy the link into your browser. Now the user's email should be verified and ready to go.

For convenience, you can keep your normal user logged in on Chrome and your superuser logged in on Firefox (or similar), so that you can see how the site behaves for both kinds of users.

you can add, delete and update store items. The sing in admin page is at the following link: https://localhost/admin/

Wompi is the payment method chosen for the project, it was configured in sandbox mode. To make payments choose any method offered by the documentation page_.

.. _page: https://docs.wompi.co/docs/en/datos-de-prueba-en-sandbox;


Settings
--------
The file with enviroment files was saved by default, if you need to config a enviroment variables go to ``.env/``. For more details : click-me_.


.. _click-me: http://cookiecutter-django.readthedocs.io/en/latest/settings.html


Type checks
^^^^^^^^^^^

Running type checks with mypy:

::

  $ mypy shop

Test coverage
^^^^^^^^^^^^^

To run the tests, check your test coverage, and generate an HTML coverage report::

    $ coverage run -m pytest
    $ coverage html
    $ open htmlcov/index.html

Running tests with py.test
~~~~~~~~~~~~~~~~~~~~~~~~~~

::

  $ pytest

Live reloading and Sass CSS compilation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Moved to `Live reloading and SASS compilation`_.

.. _`Live reloading and SASS compilation`: http://cookiecutter-django.readthedocs.io/en/latest/live-reloading-and-sass-compilation.html

More information to Deploymentment
----------

Docker
^^^^^^

See detailed `cookiecutter-django Docker documentation`_.

.. _`cookiecutter-django Docker documentation`: http://cookiecutter-django.readthedocs.io/en/latest/deployment-with-docker.html
