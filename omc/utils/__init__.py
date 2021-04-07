import os
import subprocess

import pkg_resources
from urllib.parse import urlparse

from omc.core import console


class UrlUtils:
    def __init__(self, url):
        self.url = url
        self.parsed_result = urlparse(url)

    def parse(self):
        return self.parsed_result

    def remove_identification(self):
        # 'http://guest:guest@localhost:15672/api'
        if self.parsed_result.username is not None:
            return self.parsed_result.geturl().replace(
                self.parsed_result.username + ":" + self.parsed_result.password + "@", "")
        else:
            return self.parsed_result.geturl()

    def get_username(self):
        return self.parsed_result.username

    def get_password(self):
        return self.parsed_result.password

    def get_hostname(self):
        return self.parsed_result.hostname

    def get_port(self):
        return self.parsed_result.port


def prompt(question, required=False, isBool=False, default=None):
    while True:
        result = input(question)
        if required and result:
            if isBool:
                if result[0].lower() == 'y':
                    return True
                elif result[0].lower() == 'n':
                    return False

            else:
                return result

        elif required:
            # result is None
            if default is not None:
                return default
            else:
                continue
        else:
            # not required
            if isBool:
                if result:
                    if default is not None:
                        return default
                else:
                    if result[0].lower() == 'y':
                        return True
                    elif result[0].lower() == 'n':
                        return False

            else:
                return result


def run_cmd(cmd, cwd=None, env=None, block=True, capture_output=False, verbose=True, *args, **kwargs):
    the_env = {}
    the_env.update(os.environ)
    if env is not None:
        the_env.update(env)

    try:
        cwd = cwd if cwd is None else cwd.replace("\\", "/")

        if verbose:
            console.log("cmd: %s, cwd: %s" % (cmd, cwd))

        if block:
            if capture_output:
                # capture output
                result = subprocess.run(cmd, cwd=cwd, shell=True, check=True, env=the_env, capture_output=True, *args,
                                        **kwargs)
                return result
            else:
                # to output
                result = subprocess.run(cmd, cwd=cwd, shell=True, check=True, env=the_env, capture_output=False, *args,
                                        **kwargs)
                return result
        else:
            result = subprocess.Popen(cmd, cwd=cwd, shell=True, env=the_env, *args, **kwargs)
            return result

    except Exception as e:
        raise e
