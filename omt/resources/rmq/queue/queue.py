from omt.core import Resource


class Queue(Resource):
    def list(self):
        self.context.get('')