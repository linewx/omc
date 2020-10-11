import os

import argparse
from omt.common import CmdTaskMixin
from omt.config import settings
from omt.core.resource import Resource


class Ssh(Resource, CmdTaskMixin):

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

    def exec(self):
        ssh_host = self._get_one_resource_value()
        cmd = "ssh %s -C '%s'" % (ssh_host, " ".join(self._get_action_params()))
        self.run_cmd(cmd)

    def upload(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('-r', '--recursive', action='store_true')
        parser.add_argument('--local', nargs='?', help='local files')
        parser.add_argument('--remote', nargs='?', help='remote files')

        ssh_host = self._get_one_resource_value()

        args = parser.parse_args(self._get_action_params())
        cmd = "scp %s %s %s:%s" % ('-r' if args.recursive else '', args.local, ssh_host, args.remote)
        self.run_cmd(cmd)

    def download(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('-r', '--recursive', action='store_true')
        parser.add_argument('--local', nargs='?', help='local files')
        parser.add_argument('--remote', nargs='?', help='remote files')

        ssh_host = self._get_one_resource_value()

        args = parser.parse_args(self._get_action_params())
        cmd = "scp %s %s:%s %s" % ('-r' if args.recursive else '', ssh_host, args.remote, args.local)
        self.run_cmd(cmd)

    def tunnel(self):
        tunnel_template = "ssh -nNT -L %(local_port)s:%(remote_host)s:%(remote_port)s %(bridge)s"
        bridge = self._get_one_resource_value()

        parser = argparse.ArgumentParser()
        parser.add_argument('--local-port', nargs='?', help='local port')
        parser.add_argument('--remote-port', nargs='?', help='remote port')
        parser.add_argument('--remote-host', nargs='?', help='remote host')

        args = parser.parse_args(self._get_action_params())
        cmd = tunnel_template % {
            'bridge': bridge,
            'local_port': args.local_port,
            'remote_port': args.remote_port,
            'remote_host': args.remote_host,
        }

        self.run_cmd(cmd)
