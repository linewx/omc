import os
import subprocess

from omc.core import console


class CmdTaskMixin:

    def run_cmd(self, cmd, cwd=None, env=None, block=True, capture_output=False, verbose=True, *args, **kwargs):
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
                    result = subprocess.run(cmd, cwd=cwd, shell=True, check=True, env=the_env, capture_output=True, *args, **kwargs)
                    return result
                else:
                    # to output
                    result = subprocess.run(cmd, cwd=cwd, shell=True, check=True, env=the_env, capture_output=False, *args, **kwargs)
                    return result
            else:
                result = subprocess.Popen(cmd, cwd=cwd, shell=True, env=the_env, *args, **kwargs)
                return result

        except Exception as e:
            raise e


class CompletionMixin:
    def print_completion(self, descriptions, short_mode=False):
        if type(descriptions) == list:
            for one in descriptions:
                if type(one) == tuple or type(one) == list:
                    if not short_mode:
                        console.log(":".join(one))
                    else:
                        console.log(one[0])
                else:
                    console.log(one)
