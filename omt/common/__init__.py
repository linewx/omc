from dynaconf import settings
import subprocess


class CmdTaskMixin:
    def run_cmd(self, cmd, cwd=None, env=None, block=True, *args, **kwargs):
        import os
        verbose = kwargs['verbose'] if 'verbose' in kwargs else None
        fout = None
        ferr = None
        the_env = env if not env else os.environ
        try:
            # todo@rain: ugly solution, to use pathlib instead
            cwd = cwd if cwd is None else cwd.replace("\\", "/")
            print("cmd: %s, cwd: %s" % (cmd, cwd))

            if not verbose:
                fout = open(os.path.join(settings.LOG_DIR, 'omw.log'), "w+")
                ferr = open(os.path.join(settings.LOG_DIR, 'omw.err.log'), "w+")

            if block:
                result = subprocess.run(cmd, cwd=cwd, shell=True, check=True, stdout=fout, stderr=ferr,
                                        env=the_env)
                return result
            else:
                result = subprocess.Popen(cmd, cwd=cwd, shell=True, stdout=fout, stderr=ferr, env=the_env)
                return result

        except Exception as e:
            raise e
        finally:
            if fout is not None:
                fout.close()
            if ferr is not None:
                ferr.close()