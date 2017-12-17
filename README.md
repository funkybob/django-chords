# django-chords
A simple Plugins system for Django

Installing
----------

In your settings.py :

    import chords

    INSTALLED_APPS = [ ....] + chords.discover()


Creating Plugins
----------------

Chords relies on the functionality of PEP 420, added in Python 3.3.

It will try to discover packages inside the chords.plugins package.

Make your plugin have the following directory structure:

    chords/
        plugins/
            myapp/
                __init__.py
                models.py
                ...

Note the absence of __init__.py files in the top level directories. These will
be treated as "namespace packages".
