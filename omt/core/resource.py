# -*- coding: utf-8 -*-

import os
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

    def __init__(self, context, type='web'):
        self.context = context
        # set default resoure context
        self.context[self._get_resource_name()] = ''
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
        if len(params) == 0:
            self._run()
        elif params[0].startswith('-'):
            self._run()
        else:
            # chain to other resource
            first_param = params[0]

            try:
                # detect if it's a resource type
                mod_path = (str(self.__class__.__module__)).split('.')[:-1]
                mod_path.extend([first_param, first_param])
                mod = __import__('.'.join(mod_path), fromlist=[first_param.capitalize()])
                context = copy.copy(self.context)
                context['index'] = self.context['index'] + 1
                context[resource_name] = self.context[resource_name]
                if hasattr(mod, first_param.capitalize()):
                    clazz = getattr(mod, first_param.capitalize())
                    instance = clazz(context)
                    return instance._execute()
            except ModuleNotFoundError as inst:
                self.logger.info(inst)

                # if not a resource, detect if it's action
                if hasattr(self, first_param):
                    action = getattr(self, first_param)
                    self.context['index'] += 1
                    return action()
                else:
                    # if not resource or action, treat as param
                    if self.has_params is None:
                        self.has_params = True

                        self.context['index'] = self.context['index'] + 1
                        self.context[resource_name] = first_param
                        return self._execute()
                    else:
                        import traceback
                        traceback.print_exc()
                        self.logger.error('can not parse the command')

    def help(self):
        raw_command = self.context['all']
        index = self.context['index']
        params = raw_command[index + 1:]
        if len(params) == 0:
            return textwrap.dedent(self.__doc__)
            return
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