from importlib import import_module
from pathlib import Path


# TODO
# - some mechanism for ordering...
#   - before / after lists ?


def discover():
    '''
    Attempt to discover other modules in the chords.plugins namespace.

    Returns a list of import strings, suitable for settings.INSTALLED_APPS
    '''
    from chords import plugins

    FOUND = []

    for path in plugins.__paths__:
        root = Path(path)
        for child in root.iterdir():
            if not child.is_dir():
                continue
            name = str(child).replace('/', '.')
            try:
                import_module(name, package='chords.plugins')
            except ImportError:
                continue
            else:
                FOUND.append('chords.plugins.' + name)

    return FOUND
