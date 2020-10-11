import os
from omt.common import CmdTaskMixin
from omt.config import settings
from omt.core.resource import Resource


class Ssh(Resource, CmdTaskMixin):
    template = "ssh -nNT -L %(local_port)s:%(host)s:%(port)s %(bridge)s &"

    def _description(self):
        return 'SSH(Secure Shell) Smart Tool Set'

    def _completion(self, short_mode=True):
        super()._completion(True)
        if not self._have_resource_value():
            if not os.path.exists(settings.SSH_CONFIG_FILE):
                return

            ssh_hosts = []
            with open(settings.SSH_CONFIG_FILE) as f:
                for one_line in f.readlines():
                    try:
                        one_line = one_line.strip()
                        if one_line.startswith("Host "):
                            hostname = one_line.replace("Host", "").strip()
                            if hostname:
                                ssh_hosts.append(hostname)
                    except:
                        pass

            self._print_completion(ssh_hosts)

    def cache(self):
        ssh_host = self._get_one_resource_value()
        cmd = "ssh-copy-id %s" % ssh_host
        self.run_cmd(cmd)

    def _run(self):
        ssh_host = self._get_one_resource_value()
        cmd = 'ssh %s' % ssh_host
        self.run_cmd(cmd)

