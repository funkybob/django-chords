from collections import OrderedDict
from importlib import import_module
from pathlib import Path

from django import apps
from django.urls import path, include

# TODO
# - some mechanism for ordering...
#   - project level ordering overrides / additions?


def discover():
    '''
    Attempt to discover other modules in the chords.plugins namespace.

    Returns a list of import strings, suitable for settings.INSTALLED_APPS
    '''
    from chords import plugins

    found = OrderedDict()

    for path in plugins.__paths__:
        root = Path(path)
        for child in root.iterdir():
            if not child.is_dir():
                continue
            name = str(child).replace('/', '.')
            try:
                chord = import_module(name, package='chords.plugins')
            except ImportError:
                continue
            else:
                found[name] = (
                    set(getattr(chord, 'include_before', ())),
                    set(getattr(chord, 'include_after', ())),
                )

    # Turn 'before' clauses into 'after' clauses
    for name, (before, after) in found.items():
        for dep in before.intersection(found):
            found[dep][1].add(name)

    result = []
    while found:
        for name, (before, after) in found.items():
            if after.difference(found).issubset(result):
                result.append(name)
                found.pop(name)

    return ['chords.plugins.' + name for name in result]


def auto_urls():
    '''
    Build a URL patterns tree from any App with url_prefix set on its AppConfig
    '''
    urlpatterns = []

    for app in apps.get_app_configs():
        try:
            urlpatterns.append(
                path(
                    app.url_prefix,
                    include('{}.urls'.format(app.label))
                )
            )
        except AttributeError:
            pass
    return urlpatterns
