import functools
import os
import inspect
import traceback

from omc.utils.file_utils import make_directory
from collections.abc import Callable

class CompletionContent:
    def __init__(self, content, valid=None):
        if isinstance(content, bytes):
            self.content = content.decode('UTF-8').splitlines()
        elif isinstance(content, str):
            self.content = content.splitlines()
        elif isinstance(content, list):
            self.content = content
        elif isinstance(content, CompletionContent):
            self.content = content.get_content()

        if valid is not None:
            self.valid = valid
        else:
            if isinstance(content, CompletionContent):
                # clone from content
                self.valid = self.content.is_valid()

    def get_raw_content(self):
        return '\n'.join(self.content)

    def get_content(self):
        return self.content

    def add_content(self, content):
        if isinstance(content, CompletionContent):
            self.content.extend(content.get_content())
        else:
            self.add_content(CompletionContent(content))

    def get_output(self):
        if not self.valid:
            return 'no content'
        else:
            return self.get_raw_content()


    def is_valid(self):
        return self.valid

def completion_cache(duration=None, file: (str, Callable) = '/tmp/cache.txt'):
    def _is_class_method(func):
        spec = inspect.signature(func)
        if len(spec.parameters) > 0:
            if list(spec.parameters.keys())[0] == 'self':
                return True
        return False

    def completion_cache_decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            from datetime import datetime
            if callable(file):
                if _is_class_method(file):
                    cache_file = file(args[0])
                else:
                    cache_file = file()
            else:
                cache_file = file

            cache_is_valid = False

            if not os.path.exists(cache_file):
                cache_is_valid = False
            else:
                if duration is None or duration == -1:
                    cache_is_valid = True
                else:
                    # duration and file all exists
                    os.path.getctime(cache_file)
                    the_duration = datetime.now().timestamp() - os.path.getctime(cache_file)
                    if the_duration > duration:
                        cache_is_valid = False
                    else:
                        cache_is_valid = True

            if cache_is_valid:
                with open(cache_file, 'r') as f:
                    return CompletionContent(f.read())

            else:
                # refresh cache
                if os.path.exists(cache_file):
                    os.remove(cache_file)

                make_directory(os.path.dirname(cache_file))
                try:
                    result = func(*args, **kwargs)
                    if not isinstance(result, CompletionContent):
                        return CompletionContent('', valid=False)

                    with open(cache_file, 'w') as f:
                        f.write(result.get_raw_content())

                    duration_file_name = os.path.join(os.path.dirname(cache_file), 'duration')
                    with open(duration_file_name, 'w') as f:
                        f.write("-1" if duration is None else str(duration))

                    return result
                except Exception as r:
                    return CompletionContent('', valid=False)

        return wrapper

    return completion_cache_decorator
