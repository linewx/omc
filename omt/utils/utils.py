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


def get_obj_value2(obj, key):
    return functools.reduce(lambda x, y: getattr(x, y), key.split('.'), obj)


def delete_obj_key(obj, key):
    if not key:
        return None

    first_attr, others = extract_first_attr(key)

    if not others:
        # do set value

        if first_attr:
            if isinstance(obj, dict):
                # obj.pop(key, None)
                del obj[key]
            elif isinstance(obj, list):
                del obj[int(first_attr)]
            else:
                try:
                    delattr(obj, first_attr)
                except:
                    setattr(obj, first_attr, None)

            return
    else:
        # do get value

        if first_attr:
            if isinstance(obj, dict):
                first_value = obj.get(first_attr)
            elif isinstance(obj, list):
                first_value = obj[int(first_attr)]
            else:
                first_value = getattr(obj, first_attr)

            delete_obj_key(first_value, others)


def set_obj_value(obj, key, value):
    # e.g. get pod.data.ips[0]
    if not key:
        return None

    first_attr, others = extract_first_attr(key)

    if not others:
        # do set value

        if first_attr:
            if isinstance(obj, dict):
                obj[first_attr] = value
            elif isinstance(obj, list):
                obj[int(first_attr)] = value
            else:
                setattr(obj, first_attr, value)

            return
    else:
        # do get value

        if first_attr:
            if isinstance(obj, dict):
                first_value = obj.get(first_attr)
            elif isinstance(obj, list):
                first_value = obj[int(first_attr)]
            else:
                first_value = getattr(obj, first_attr)

            set_obj_value(first_value, others, value)


def get_obj_value(obj, key):
    # e.g. get pod.data.ips[0]
    if not key:
        return None

    first_attr, others = extract_first_attr(key)

    if first_attr:
        if isinstance(obj, dict):
            first_value = obj.get(first_attr)
        elif isinstance(obj, list):
            first_value = obj[int(first_attr)]
        else:
            first_value = getattr(obj, first_attr)

        if not others:
            return first_value

        else:
            return get_obj_value(first_value, others)


def extract_first_attr(key):
    key = key.strip('[].')
    for index in range(0, len(key)):
        if key[index] in '[].':
            return key[:index], key[index:].strip('[].')

    return key, None


def get_all_dict_Keys(obj, paths=[]):
    if isinstance(obj, dict):
        for k, v in obj.items():
            paths.append(k)
            subpaths = []
            get_all_dict_Keys(v, subpaths)
            paths.extend([k + one if one.startswith('[') else k + '.' + one for one in subpaths])
    elif isinstance(obj, list):
        paths.append('[0]')
        subpaths = []
        get_all_dict_Keys(obj[0], subpaths)
        paths.extend(['[0].' + one for one in subpaths])


if __name__ == '__main__':
    import json

    obj = json.loads('{"a":"a", "b": [{"e": "sdfsdf"}, "d"]}')
    set_obj_value(obj, 'b[0].e', 'test')
    delete_obj_key(obj, 'b[0].e')
    print(obj)
    print(get_obj_value(obj, 'b[0].e'))

    paths = []
    get_all_dict_Keys(obj, paths)
    print(paths)
    # first,other = (extract_first_attr('a[1].b'))
    # second,other2 = extract_first_attr(other)
    # print(extract_first_attr(other2))
