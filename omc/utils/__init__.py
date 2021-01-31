import pkg_resources
from urllib.parse import urlparse


class JmxTermUtils:
    @staticmethod
    def build_command(command):
        jmxterm = pkg_resources.resource_filename(__name__, '../lib/jmxterm-1.0.2-uber.jar')
        jmx_cmd = 'echo "%s"  | java -jar %s -n' % (command, jmxterm)
        return jmx_cmd


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