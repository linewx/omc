# -*- coding: utf-8 -*-

import os

import pkg_resources

import omt
import logging
import copy
import textwrap


class Resource:
    """
        NAME
            project - project command

        SYNOPSIS
            project [RESOURCE] action [OPTION]

        ACTION LIST
            env - environment command
            edit - edit the doc
    """

    def __init__(self, context={}, type='web'):
        self.context = context
        # set default resoure context
        self.context[self._get_resource_name()] = []
        self.logger = logging.getLogger('.'.join([self.__module__, self.__class__.__name__]))
        self.has_params = None
        self.type = type

    def _get_resource_name(self):
        return (self.__class__.__name__).lower()

    def _get_resource_value(self):
        return self.context[self._get_resource_name()]

    def _get_params(self):
        raw_command = self.context['all']
        index = self.context['index']
        params = raw_command[index + 1:]
        return params

    def _run(self):
        raise Exception('no run action defined')

    def _before_sub_resource(self):
        pass

    def _after_sub_resource(self):
        pass

    def _format(self, result):
        if self.type == 'cmd':
            print(result)
        elif self.type == 'web':
            return result
        else:
            raise Exception("unsupported type")

    def _exec(self):
        return self._format(self._execute())

    def _execute(self):
        resource_name = self._get_resource_name()
        raw_command = self.context['all']
        index = self.context['index']
        params = raw_command[index + 1:]
        self.context[resource_name] = []  # init reosurce params

        while True:
            if not params:
                # has no params, stop parsing then start to run default action
                self._run()
                break

            else:
                # has params
                next_value = params[0]
                if next_value.startswith('-'):
                    # next value is resource params
                    self.context[resource_name].append(params[0])
                    self.context['index'] = self.context['index'] + 1  # increase index
                    index = self.context['index']
                    params = raw_command[index + 1:]
                elif next_value in self._get_submodules():
                    # chain to other resource

                    try:
                        # detect if it's a resource type
                        mod_path = (str(self.__class__.__module__)).split('.')[:-1]
                        mod_path.extend([next_value, next_value])
                        mod = __import__('.'.join(mod_path), fromlist=[next_value.capitalize()])
                        self._before_sub_resource()
                        context = copy.copy(self.context)
                        context['index'] = self.context['index'] + 1
                        context[resource_name] = self.context[resource_name]
                        if hasattr(mod, next_value.capitalize()):
                            clazz = getattr(mod, next_value.capitalize())
                            instance = clazz(context)
                            result = instance._execute()
                            self._after_sub_resource()
                            return result
                        else:
                            self.logger.error("module %s deteched, but not exists in fact", next_value)
                            return
                    except ModuleNotFoundError as inst:
                        self.logger.info(inst)


                elif hasattr(self, next_value):
                    # next_value is resource action
                    action = getattr(self, next_value)
                    self.context['index'] += 1
                    return action()
                else:
                    #
                    # if self.has_params is None:
                    #     self.has_params = True
                    self.context['index'] = self.context['index'] + 1
                    index = self.context['index']
                    self.context[resource_name].append(next_value)
                    params = raw_command[index + 1:]

    def description(self):
        """this is the description for resources"""
        return self._get_resource_name()

    def completion(self):
        # list candidates for completions in zsh style (a:"description for a" b:"description for b")
        try:
            if not self._get_resource_value():
                self._list_resources()
            else:
                # public methods
                public_methods = self._get_public_methods()
                description = [(one, getattr(self, one).__doc__) for one in public_methods]
                for one_desc in description:
                    print(one_desc[0] + ':' + one_desc[0] if one_desc[1] is None else one_desc[1])

                # available modules
                # pkg_resources.resource_listdir('omt')
                # self._get_submodules()
                for one_module in self._get_submodules():
                    print(one_module + ":" + 'submodule-' + one_module)
                return description
        except Exception as inst:
            # keep silent in completion mode
            return

    def _get_public_methods(self):
        return list(filter(lambda x: callable(getattr(self, x)) and not x.startswith('_'), dir(self)))

    def _get_submodules(self):
        # for example, module name is 'omt.resources.jmx.jmx', submodules should be other folder within omt.resources.jmx folder
        module_path = self.__module__.split('.')
        module_path.pop()
        current_module = module_path.pop()
        all_resources = (pkg_resources.resource_listdir('.'.join(module_path), current_module))
        filterd_modules = [one for one in all_resources if
                           pkg_resources.resource_isdir('.'.join(module_path) + '.' + current_module,
                                                        one) is True and one not in ['__pycache__']]

        return filterd_modules

    def _list_resources(self):
        pass

    def help(self):
        raw_command = self.context['all']
        index = self.context['index']
        params = raw_command[index + 1:]
        if len(params) == 0:
            return textwrap.dedent(self.__doc__)
        try:
            first_param = params[0]
            # detect if it's a resource type
            mod_path = (str(self.__class__.__module__)).split('.')[:-1]
            mod_path.extend([first_param, first_param])
            mod = __import__('.'.join(mod_path), fromlist=[first_param.capitalize()])
            clazz = getattr(mod, first_param.capitalize())
            return clazz.textwrap.dedent(__doc__)
        except (ModuleNotFoundError, AttributeError) as inst:
            try:
                action = getattr(self, params[0])
                print(textwrap.dedent(action.__doc__))
            except Exception as inst:
                print(inst)
