from omt.core import Resource
from pyrabbit.api import Client


class Queue(Resource):

    def list(self):
        print('list')
