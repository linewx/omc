from omt.core.resource import Resource
#from omt import model,engine
from sqlalchemy.orm import sessionmaker
import subprocess

class Ssh(Resource):
    template = "ssh -nNT -L %(local_port)s:%(host)s:%(port)s %(bridge)s &"
    def _description(self):
        return 'SSH(Secure Shell) Smart Tool Set'
    
    def get_session(self):
        Session = sessionmaker()
        Session.configure(bind=engine)
        return Session()

    def start(self):
        service_name = self.__get_resource_value()
        Session = sessionmaker()
        Session.configure(bind=engine)
        session = Session()
        query = session.query(model.ProxyTable).filter(model.ProxyTable.service_name == service_name)
        the_row = query.first()
        service_cmd = Ssh.template % the_row.__dict__
        subprocess.run(service_cmd, shell=True)
    
    def list(self):
        session = self.get_session()
        query = session.query(model.ProxyTable.service_name)
        query_result = query.all()
        result = [one[0] for one in query_result]
        print(result)
    
    




