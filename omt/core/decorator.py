import functools
import os

from omt.utils.file_utils import make_directory


def filecache(duration=None, file='/tmp/cache.txt'):
    def completion_cache_decorator(func):
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            from datetime import datetime
            cache_file = file
            if hasattr(self, '_get_cache_file_name'):
                cache_file = self._get_cache_file_name()

            cache_is_valid = False

            if not os.path.exists(cache_file):
                cache_is_valid = False
            else:
                if duration is None:
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
                    return f.read()

            else:
                # refresh cache
                if os.path.exists(cache_file):
                    os.remove(cache_file)

                make_directory(os.path.dirname(cache_file))
                result = func(self, *args, **kwargs)
                with open(cache_file, 'w') as f:
                    f.write(result)

                duration_file_name = os.path.join(os.path.dirname(cache_file), 'duration')
                with open(duration_file_name, 'w') as f:
                    f.write("-1" if duration is None else str(duration))

                return result

        return wrapper

    return completion_cache_decorator
