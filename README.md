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

If your chord must be installed before or after a particular plugin, you can
list these in the module's __init__.py as `include_before` and `include_after`.
When generating the discovered list, chords will resolve the dependencies for
you.


Auto-URLs
---------

Another function included is support for ``AppConfig.url_prefix``, allowing
your plugins [or any other app!] to specify a default URL prefix for including
its urls.

    urlpatterns = [
        ...
    ] + chords.auto_urls()

It generates a list of URL ``include`` patterns for each of the apps with a
`url_prefix` attribute.
