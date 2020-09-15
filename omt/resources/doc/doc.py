# -*- coding: utf-8 -*-

import os
from omt.core import Resource


class Doc(Resource):
    """
NAME
    doc - doc command

SYNOPSIS
    project [RESOURCE] action [OPTION]

ACTION LIST
    env - environment command
    edit - edit the doc
    """

    def _run(self):
        self.view()

    def view(self):
        '''
        this is the test doc
        :return:
        '''
        if 'doc' in self.context:
            resource_name = self.context['doc']
            fname = os.path.join(zz.home, 'notes', resource_name + '.txt')
            with open(fname, 'r', encoding="utf8") as fin:
                print(fin.read())

    def edit(self):
        if 'doc' in self.context:
            resource_name = self.context['doc']

            fname = os.path.join(zz.home, 'notes', resource_name + '.txt')
            if os.name == 'posix':
                os.system("open " + fname)
            else:
                os.system("start " + fname)
