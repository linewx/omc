# -*- coding: utf-8 -*-

import os
from omt.core.resource import Resource
from omt.utils.config_reader import ConfigReader


class Config(Resource):
    """
NAME
    config - sub resource type of project resource

SYNOPSIS
    project [<>] action [OPTION]

ACTION LIST
    config - view config file

    edit - edit the doc
    """
    def _run(self):
        project = self.context['project']

        cfg_file_path = os.path.join(zz.home, 'projects', project, 'cfg', 'config.ini')
        if 'config' not in self.context:
            self._list_config(cfg_file_path)
        else:
            item = self.context['config']
            configreader = ConfigReader(cfg_file_path)
            print(configreader.get(item))

    def _list_config(self, config_file):
        with open(config_file, 'r', encoding="utf8") as fin:
            print(fin.read())






