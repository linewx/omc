# -*- coding: utf-8 -*-

import os
from omt.core import Resource


class Doc(Resource):
    def _description(self):
        'description for doc'
        return 'view documents'


    def _run(self):
        self.view()

    def view(self):
        ''''''
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
