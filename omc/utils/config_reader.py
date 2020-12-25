import configparser
import logging


class ConfigReader:
    def __init__(self, cfg_file):
        self.cfg_file = cfg_file
        self.config_parser = configparser.RawConfigParser()
        self.config_parser.read(self.cfg_file)
        self.logger = logging.getLogger(__name__)


    def get_parser(self):
        return self.config_parser

    def get_sections(self):
        return self.config_parser.sections()

    def get_one_section(self, name):
        return self.config_parser[name]

    def get_with_section(self, section, key):
        print(self.config_parser[section][key])
        return self.config_parser[section][key]

    def get(self, key):
        if key is None:
            raise ValueError('key can\'t be empty')
        else:
            config_parser = configparser.ConfigParser()
            config_parser.read(self.cfg_file)
            try:
                if '.' in key:
                    key_list = key.split('.')
                    return config_parser[key_list[0]][key_list[1]]
                else:
                    return config_parser['default'][key]
            except Exception:
                self.logger.error('key %s not found' % key)

    def add(self, section, items):
        config_parser = configparser.RawConfigParser()
        config_parser.read(self.cfg_file)

        if section in config_parser.sections():
            raise ValueError('section %s already exist' % section)
        else:
            config_parser.add_section(section)
            for key, value in items.items():
                config_parser.set(section, key, value)

            with open(self.cfg_file, 'w') as configfile:
                config_parser.write(configfile)

    def update(self, section, items):
        config_parser = configparser.RawConfigParser()
        config_parser.read(self.cfg_file)

        if section not in config_parser.sections():
            raise ValueError('section %s not found' % section)
        else:
            config_parser.add_section(section)
            for key, value in items.items():
                config_parser.set(section, key, value)


            with open(self.cfg_file, 'w') as configfile:
                config_parser.write(configfile)