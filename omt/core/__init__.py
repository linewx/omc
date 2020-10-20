import functools
import os

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


def filecache(duration=None, file='/tmp/cache.txt'):
    def completion_cache_decorator(func):
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            from datetime import datetime
            cache_file = file
            if hasattr(self, '_get_cache_file_name'):
                cache_file = self._get_cache_file_name()

            if os.path.exists(cache_file):
                cache_is_valid = True  # permanent by default
                if duration is not None:
                    # cache is not permanent
                    os.path.getctime(cache_file)
                    the_duration = datetime.now().timestamp() - os.path.getctime(cache_file)
                    if the_duration > duration:
                        # cache is invalid:
                        cache_is_valid = False
                        os.remove(cache_file)

                        result = func(self, *args, **kwargs)
                        with open(cache_file, 'w') as f:
                            f.write(result)

                        return result

                if cache_is_valid:
                    with open(cache_file, 'r') as f:
                        return f.read()


        return wrapper

    return completion_cache_decorator
