import pkg_resources
from urllib.parse import urlparse


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
