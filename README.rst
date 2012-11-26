Kucheninitiative
================

Die Initiative für mehr Kuchen an der HSR ist eine solidarisch-gemeinschafliche
Vereinigung zur Steigerung des allgemeinen Wohlbefindens durch erhöhten und
regelmässigen Kuchengenuss an der HSR.

Diese Webapp hat das Ziel, die Regeln für die Kucheninitiative zu kommunizieren,
den Zeitplan zu organisieren sowie Erinnerungen zu verschicken.


Setup (Dev)
-----------

Prerequisites
~~~~~~~~~~~~~

Requirements:

- Python 2.x and pip
- virtualenv and virtualenvwrapper

The easiest way to set up virtualenvwrapper is::

    $ sudo pip install virtualenv virtualenvwrapper
    $ echo -e "\nsource /usr/local/bin/virtualenvwrapper.sh" >> ~/.bashrc

First time setup
~~~~~~~~~~~~~~~~

The first time setup creates a virtual environment separated from your
systemwide `PYTHONPATH` and sets up some environment variables to be used
every time you activate the virtualenv.

The instructions below assume your postgres database is called ``kuchen``; if
not, just change the ``DATABASE_URL`` env variable.

::

    $ mkvirtualenv kuchen
    $ pip install -r requirements.txt
    $ POSTACTIVATE=$VIRTUAL_ENV/$VIRTUALENVWRAPPER_ENV_BIN_DIR/postactivate
    $ echo "export DATABASE_URL='postgres://localhost/kuchen'" >> $POSTACTIVATE
    $ echo "export PORT=8000" >> $POSTACTIVATE
    $ echo "export DEBUG=True" >> $POSTACTIVATE
    $ ./manage.py syncdb
    $ ./manage.py migrate

Development
~~~~~~~~~~~

Each time you want to work on the project, first enable the virtualenv::

    $ workon kuchen

To start the webserver::

    $ ./manage.py runserver

If database errors occur because the schema has changed after a ``git pull``::

    $ ./manage.py migrate

If some script complains that a python module / dependency is missing::

    $ pip install -U -r requirements.txt


Setup (Heroku)
--------------

::

    $ heroku apps:create --stack cedar [appname]
    $ heroku addons:add heroku-postgresql:dev
    $ heroku config:set DEBUG=False
    $ heroku config:set COMPRESS_OFFLINE=True
    $ git push heroku master
    $ heroku run python manage.py migrate