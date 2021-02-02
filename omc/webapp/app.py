from flask import Flask

app = Flask(__name__)
import omc
import sys
import logging
from omc import utils
import omc
import traceback
import json
from flask import jsonify


@app.route("/zz/<path:path>")
def cmd(path):
    FORMAT = "[%(filename)s:%(lineno)s - %(funcName)s ] %(message)s"
    logging.basicConfig(format=FORMAT)
    logger = logging.getLogger(__name__)
    argv = path.split('/')
    resource_type = argv[0]
    print('################## resource type:' + resource_type + '##################')
    try:
        mod = __import__(".".join(['omc', 'resources', resource_type, resource_type]),
                         fromlist=[resource_type.capitalize()])
        clazz = getattr(mod, resource_type.capitalize())
        context = {
            'all': ['web', *argv],
            'index': 1
        }
        data = clazz(context)._exec()

        response = app.response_class(
            response=json.dumps(data),
            mimetype='application/json'
        )
        return response

    except Exception as inst:
        traceback.print_exc()
        logger.error(inst)
