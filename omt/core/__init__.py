import functools

from omt.core.resource import Resource

__all__ = ['Resource']


def simple_completion(prompts=None):
    def simple_completion_decorator(func):
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            if 'completion' in self._get_action_params():
                self._print_completion(prompts, True)
                return
            else:
                return func(self, *args, **kwargs)

        return wrapper

    return simple_completion_decorator
