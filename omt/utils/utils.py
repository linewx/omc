import functools
import os

def rsetattr(obj, attr, val):
    pre, _, post = attr.rpartition('.')
    return setattr(rgetattr(obj, pre) if pre else obj, post, val)


sentinel = object()


def rgetattr(obj, attr, default=sentinel):
    if default is sentinel:
        _getattr = getattr
    else:
        def _getattr(obj, name):
            return getattr(obj, name, default)
    return functools.reduce(_getattr, [obj] + attr.split('.'))


def omt_import(name):
    components = name.split('.')

    for comp in components:
        mod = __import__(components[0])
        mod = getattr(mod, comp)
    return mod



def make_directory(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)
