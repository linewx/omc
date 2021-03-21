import argparse
import functools
import logging
import os
import inspect
import traceback

from omc.common.formatter import Formatter

from omc.utils.file_utils import make_directory
from collections.abc import Callable

logger = logging.getLogger(__name__)

class CompletionContent:
    def __init__(self, content='', valid=None):
        if isinstance(content, bytes):
            self.content = content.decode('UTF-8').splitlines()
        elif isinstance(content, str):
            self.content = content.splitlines()
        elif isinstance(content, list):
            self.content = content
        elif isinstance(content, CompletionContent):
            self.content = content.get_content()

        self.valid = True
        if valid is not None:
            self.valid = valid
        else:
            if isinstance(content, CompletionContent):
                # clone from content
                self.valid = content.is_valid()

    def get_raw_content(self):
        return '\n'.join(self.content)

    def get_content(self):
        return self.content

    def add_content(self, content):
        if isinstance(content, CompletionContent):
            self.content.extend(content.get_content())
            self.valid = content.is_valid() and self.valid
        else:
            self.add_content(CompletionContent(content))

    def get_output(self, force=True):
        if force:
            return self.get_raw_content()

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
            if callable(duration):
                if _is_class_method(duration):
                    cache_duration = duration(args[0])
                else:
                    cache_duration = duration()
            else:
                cache_duration = duration

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
                if cache_duration is None or cache_duration == -1:
                    cache_is_valid = True
                else:
                    # duration and file all exists
                    os.path.getctime(cache_file)
                    the_duration = datetime.now().timestamp() - os.path.getctime(cache_file)
                    if the_duration > cache_duration:
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

                    if not result.is_valid():
                        # don't cache
                        return result

                    with open(cache_file, 'w') as f:
                        f.write(result.get_raw_content())

                    duration_file_name = os.path.join(os.path.dirname(cache_file), 'duration')
                    with open(duration_file_name, 'w') as f:
                        f.write("-1" if cache_duration is None else str(cache_duration))

                    return result
                except Exception as e:
                    logger.error(e, exc_info=True)
                    return CompletionContent('', valid=False)

        return wrapper

    return completion_cache_decorator


def action_arguments(arguments=[]):
    def simple_completion_decorator(func):
        func.completion = True

        @functools.wraps(func)
        def wrapper(self, *func_args, **func_kwargs):
            completions = []
            parser = argparse.ArgumentParser()
            for one in arguments:
                args, kwargs = one
                parser.add_argument(*args, **kwargs)
                for one_args in args:
                    description = kwargs.get('help') if kwargs is not None else one_args
                    completions.append((one_args, description))

            if 'completion' in self._get_action_params():
                completion_result = CompletionContent(Formatter.format_completions(completions))
                print(completion_result.get_raw_content())
                return
            else:
                return func(self, parser, *func_args, **func_kwargs)

        return wrapper

    return simple_completion_decorator
