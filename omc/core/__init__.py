import argparse
import functools

from omc.core.terminal import console
from omc.core.resource import Resource

__all__ = ['Resource', 'console']

built_in_resources = ['config', 'completion']


def simple_completion(prompts=None):
    def simple_completion_decorator(func):
        func.completion = True

        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            if 'completion' in self._get_action_params():
                self._print_completion(prompts, True)
                return
            else:
                return func(self, *args, **kwargs)

        return wrapper

    return simple_completion_decorator



