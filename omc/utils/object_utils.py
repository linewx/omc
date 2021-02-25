import json

from omc.core import console


class ObjectUtils:
    # @staticmethod
    # def get_obj_value2(obj, key):
    #     return functools.reduce(lambda x, y: getattr(x, y), key.split('.'), obj)

    @staticmethod
    def delete_node(obj, path):
        if not path:
            return None

        first_attr, others, delimiter = ObjectUtils._get_parent_path(path)

        if not others:
            # do set value

            if first_attr:
                if isinstance(obj, dict):
                    # obj.pop(key, None)
                    if path in obj:
                        del obj[path]
                elif isinstance(obj, list):
                    index = int(first_attr)
                    if index < len(obj):
                        del obj[index]
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

                ObjectUtils.delete_node(first_value, others)

    @staticmethod
    def set_node(obj, path, value):
        # e.g. get pod.data.ips[0]
        if not path:
            return None

        first_attr, others, delimiter = ObjectUtils._get_parent_path(path)

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

                ObjectUtils.set_node(first_value, others, value)

    @staticmethod
    def get_node(obj, path):
        # e.g. get pod.data.ips[0]
        if not path:
            return None

        first_attr, others, delimiter = ObjectUtils._get_parent_path(path)

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
                return ObjectUtils.get_node(first_value, others)

    @staticmethod
    def _get_parent_path(path):
        path = path.strip('[].')
        for index in range(0, len(path)):
            if path[index] in '[].':
                return path[:index], path[index:].strip('[].'), path[index]

        return path, None, None

    @staticmethod
    def get_nodes(obj, paths=[]):
        if isinstance(obj, dict):
            for k, v in obj.items():
                paths.append(k)
                subpaths = []
                ObjectUtils.get_nodes(v, subpaths)
                paths.extend([k + one if one.startswith('[') else k + '.' + one for one in subpaths])
        elif isinstance(obj, list):
            paths.append('[0]')
            subpaths = []
            ObjectUtils.get_nodes(obj[0], subpaths)
            paths.extend(['[0].' + one for one in subpaths])

    @staticmethod
    def build(path, value, init_object={}):
        # todo: to support array
        first, others, delimiter = ObjectUtils._get_parent_path(path)

        if others is None:
            # build_object('a', 'b')
            if isinstance(init_object, list):
                index = int(first)
                if index < len(init_object):
                    init_object[index] = value
                elif index == len(init_object):
                    init_object.append(value)
            else:
                init_object[path] = value
            return init_object
        elif delimiter == '.':
            # build_object('a.b', 'c')
            return {first: ObjectUtils.build(others, value, {})}
        else:
            if isinstance(init_object, list):
                index = int(first)
                if index < len(init_object):
                    init_object[int(first)] = ObjectUtils.build(others, value, {})
                    return init_object
                elif index == len(init_object):
                    init_object.append(ObjectUtils.build(others, value, {}))
                    return init_object
                else:
                    raise Exception('out of range')
            else:
                # build_object('a[0].b', 'c')
                init_object = {first: ObjectUtils.build(others, value, [])}
                return init_object

    @staticmethod
    def format(obj):
        return json.dumps(obj, indent=2)

if __name__ == '__main__':
    # obj = json.loads('{"a":"a", "b": [{"e": "sdfsdf"}, "d"]}')
    # set_obj_value(obj, 'b[0].e', 'test')
    # delete_obj_key(obj, 'b[0].e')
    # print(obj)
    # print(get_obj_value(obj, 'b[0].e'))
    #
    # paths = []
    # get_all_dict_Keys(obj, paths)
    # print(paths)
    #
    # #result = build_object('a.b.c', 'value')
    # #print(result)
    # first,other = (extract_first_attr('a[1].b'))
    # second,other2 = extract_first_attr(other)
    # print(extract_first_attr(other2))

    # the_object = (build_object('a[0].c.d', 'b'))
    # print(get_obj_value(the_object, 'a[0].c.d'))
    the_object = (ObjectUtils.build('a[0]', {'a': 'b'}))
    console.log(the_object)
    # print(json.loads('b'))
