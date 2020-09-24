#!/usr/bin/env python

#   The contents of this file are subject to the Mozilla Public License
#   Version 1.1 (the "License"); you may not use this file except in
#   compliance with the License. You may obtain a copy of the License at
#   https://www.mozilla.org/MPL/
#
#   Software distributed under the License is distributed on an "AS IS"
#   basis, WITHOUT WARRANTY OF ANY KIND, either express or implied. See the
#   License for the specific language governing rights and limitations
#   under the License.
#
#   The Original Code is RabbitMQ Management Plugin.
#
#   The Initial Developer of the Original Code is GoPivotal, Inc.
#   Copyright (c) 2007-2020 Pivotal Software, Inc.  All rights reserved.

from __future__ import print_function

import base64
import json
import os
import socket
import ssl
import traceback

import http.client as httplib
import urllib.parse as urlparse
from urllib.parse import quote_plus
from optparse import OptionParser, TitledHelpFormatter

try:
    from signal import signal, SIGPIPE, SIG_DFL

    signal(SIGPIPE, SIG_DFL)
except ImportError:
    pass

import sys


def b64(s):
    return base64.b64encode(s.encode('utf-8')).decode('utf-8')


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


if sys.version_info[0] < 2 or (sys.version_info[0] == 2 and sys.version_info[1] < 6):
    eprint("Sorry, rabbitmqadmin requires at least Python 2.6 (2.7.9 when HTTPS is enabled).")
    sys.exit(1)


    def b64(s):
        return base64.b64encode(s.encode('utf-8')).decode('utf-8')

if sys.version_info[0] == 2:
    class ConnectionError(OSError):
        pass


    class ConnectionRefusedError(ConnectionError):
        pass

VERSION = '3.8.3'

LISTABLE = {'connections': {'vhost': False, 'cols': ['name', 'user', 'channels']},
            'channels': {'vhost': False, 'cols': ['name', 'user']},
            'consumers': {'vhost': True},
            'exchanges': {'vhost': True, 'cols': ['name', 'type']},
            'queues': {'vhost': True, 'cols': ['name', 'messages']},
            'bindings': {'vhost': True, 'cols': ['source', 'destination',
                                                 'routing_key']},
            'users': {'vhost': False},
            'vhosts': {'vhost': False, 'cols': ['name', 'messages']},
            'permissions': {'vhost': False},
            'nodes': {'vhost': False, 'cols': ['name', 'type', 'mem_used']},
            'parameters': {'vhost': False, 'json': ['value']},
            'policies': {'vhost': False, 'json': ['definition']},
            'operator_policies': {'vhost': False, 'json': ['definition']},
            'vhost_limits': {'vhost': False, 'json': ['value']}}

SHOWABLE = {'overview': {'vhost': False, 'cols': ['rabbitmq_version',
                                                  'cluster_name',
                                                  'queue_totals.messages',
                                                  'object_totals.queues']}}

PROMOTE_COLUMNS = ['vhost', 'name', 'type',
                   'source', 'destination', 'destination_type', 'routing_key']

URIS = {
    'exchange': '/exchanges/{vhost}/{name}',
    'queue': '/queues/{vhost}/{name}',
    'binding': '/bindings/{vhost}/e/{source}/{destination_char}/{destination}',
    'binding_del': '/bindings/{vhost}/e/{source}/{destination_char}/{destination}/{properties_key}',
    'vhost': '/vhosts/{name}',
    'user': '/users/{name}',
    'permission': '/permissions/{vhost}/{user}',
    'parameter': '/parameters/{component}/{vhost}/{name}',
    'policy': '/policies/{vhost}/{name}',
    'operator_policy': '/operator-policies/{vhost}/{name}',
    'vhost_limit': '/vhost-limits/{vhost}/{name}'
}


def queue_upload_fixup(upload):
    # rabbitmq/rabbitmq-management#761
    #
    # In general, the fixup_upload argument can be used to fixup/change the
    # upload dict after all argument parsing is complete.
    #
    # This simplifies setting the queue type for a new queue by allowing the
    # user to use a queue_type=quorum argument rather than the somewhat confusing
    # arguments='{"x-queue-type":"quorum"}' parameter
    #
    if 'queue_type' in upload:
        queue_type = upload.get('queue_type')
        arguments = upload.get('arguments', {})
        arguments['x-queue-type'] = queue_type
        upload['arguments'] = arguments


DECLARABLE = {
    'exchange': {'mandatory': ['name', 'type'],
                 'json': ['arguments'],
                 'optional': {'auto_delete': 'false', 'durable': 'true',
                              'internal': 'false', 'arguments': {}}},
    'queue': {'mandatory': ['name'],
              'json': ['arguments'],
              'optional': {'auto_delete': 'false', 'durable': 'true',
                           'arguments': {}, 'node': None, 'queue_type': None},
              'fixup_upload': queue_upload_fixup},
    'binding': {'mandatory': ['source', 'destination'],
                'json': ['arguments'],
                'optional': {'destination_type': 'queue',
                             'routing_key': '', 'arguments': {}}},
    'vhost': {'mandatory': ['name'],
              'optional': {'tracing': None}},
    'user': {'mandatory': ['name', ['password', 'password_hash'], 'tags'],
             'optional': {'hashing_algorithm': None}},
    'permission': {'mandatory': ['vhost', 'user', 'configure', 'write', 'read'],
                   'optional': {}},
    'parameter': {'mandatory': ['component', 'name', 'value'],
                  'json': ['value'],
                  'optional': {}},
    # priority has to be converted to an integer
    'policy': {'mandatory': ['name', 'pattern', 'definition'],
               'json': ['definition', 'priority'],
               'optional': {'priority': 0, 'apply-to': None}},
    'operator_policy': {'mandatory': ['name', 'pattern', 'definition'],
                        'json': ['definition', 'priority'],
                        'optional': {'priority': 0, 'apply-to': None}},
    'vhost_limit': {'mandatory': ['vhost', 'name', 'value'],
                    'json': ['value'],
                    'optional': {}},
}

DELETABLE = {
    'exchange': {'mandatory': ['name']},
    'queue': {'mandatory': ['name']},
    'binding': {'mandatory': ['source', 'destination_type', 'destination'],
                'optional': {'properties_key': '~'}},
    'vhost': {'mandatory': ['name']},
    'user': {'mandatory': ['name']},
    'permission': {'mandatory': ['vhost', 'user']},
    'parameter': {'mandatory': ['component', 'name']},
    'policy': {'mandatory': ['name']},
    'operator_policy': {'mandatory': ['name']},
    'vhost_limit': {'mandatory': ['vhost', 'name']}
}

CLOSABLE = {
    'connection': {'mandatory': ['name'],
                   'optional': {},
                   'uri': '/connections/{name}'}
}

PURGABLE = {
    'queue': {'mandatory': ['name'],
              'optional': {},
              'uri': '/queues/{vhost}/{name}/contents'}
}

EXTRA_VERBS = {
    'publish': {'mandatory': ['routing_key'],
                'optional': {'payload': None,
                             'properties': {},
                             'exchange': 'amq.default',
                             'payload_encoding': 'string'},
                'json': ['properties'],
                'uri': '/exchanges/{vhost}/{exchange}/publish'},
    'get': {'mandatory': ['queue'],
            'optional': {'count': '1', 'ackmode': 'ack_requeue_true',
                         'payload_file': None, 'encoding': 'auto'},
            'uri': '/queues/{vhost}/{queue}/get'}
}

for k in DECLARABLE:
    DECLARABLE[k]['uri'] = URIS[k]

for k in DELETABLE:
    DELETABLE[k]['uri'] = URIS[k]
    DELETABLE[k]['optional'] = DELETABLE[k].get('optional', {})
DELETABLE['binding']['uri'] = URIS['binding_del']


def short_usage():
    return "rabbitmqadmin [options] subcommand"


def title(name):
    return "\n%s\n%s\n\n" % (name, '=' * len(name))


def subcommands_usage():
    usage = """Usage
=====
  """ + short_usage() + """

  where subcommand is one of:
""" + title("Display")

    for l in LISTABLE:
        usage += "  list {0} [<column>...]\n".format(l)
    for s in SHOWABLE:
        usage += "  show {0} [<column>...]\n".format(s)
    usage += title("Object Manipulation")
    usage += fmt_usage_stanza(DECLARABLE, 'declare')
    usage += fmt_usage_stanza(DELETABLE, 'delete')
    usage += fmt_usage_stanza(CLOSABLE, 'close')
    usage += fmt_usage_stanza(PURGABLE, 'purge')
    usage += title("Broker Definitions")
    usage += """  export <file>
  import <file>
"""
    usage += title("Publishing and Consuming")
    usage += fmt_usage_stanza(EXTRA_VERBS, '')
    usage += """
  * If payload is not specified on publish, standard input is used

  * If payload_file is not specified on get, the payload will be shown on
    standard output along with the message metadata

  * If payload_file is specified on get, count must not be set
"""
    return usage


def config_usage():
    usage = "Usage\n=====\n" + short_usage()
    usage += "\n" + title("Configuration File")
    usage += """  It is possible to specify a configuration file from the command line.
  Hosts can be configured easily in a configuration file and called
  from the command line.
"""
    usage += title("Example")
    usage += """  # rabbitmqadmin.conf.example START

  [host_normal]
  hostname = localhost
  port = 15672
  username = guest
  password = guest
  declare_vhost = / # Used as default for declare / delete only
  vhost = /         # Used as default for declare / delete / list

  [host_ssl]
  hostname = otherhost
  port = 15672
  username = guest
  password = guest
  ssl = True
  ssl_key_file = /path/to/key.pem
  ssl_cert_file = /path/to/cert.pem

  # rabbitmqadmin.conf.example END
"""
    usage += title("Use")
    usage += """  rabbitmqadmin -c rabbitmqadmin.conf.example -N host_normal ..."""
    return usage


def more_help():
    return """
More Help
=========

For more help use the help subcommand:

  rabbitmqadmin help subcommands  # For a list of available subcommands
  rabbitmqadmin help config       # For help with the configuration file
"""


def fmt_required_flag(val):
    # when one of the options is required, e.g.
    # password vs. password_hash
    if type(val) is list:
        # flag1=... OR flag2=... OR flag3=...
        return "=... OR ".join(val)
    else:
        return val


def fmt_optional_flag(val):
    return val


def fmt_usage_stanza(root, verb):
    def fmt_args(args):
        res = " ".join(["{0}=...".format(fmt_required_flag(a)) for a in args['mandatory']])
        opts = " ".join("{0}=...".format(fmt_optional_flag(o)) for o in args['optional'].keys())
        if opts != "":
            res += " [{0}]".format(opts)
        return res

    text = ""
    if verb != "":
        verb = " " + verb
    for k in root.keys():
        text += " {0} {1} {2}\n".format(verb, k, fmt_args(root[k]))
    return text


def default_config():
    home = os.getenv('USERPROFILE') or os.getenv('HOME')
    if home is not None:
        config_file = home + os.sep + ".rabbitmqadmin.conf"
        if os.path.isfile(config_file):
            return config_file
    return None


def print_version():
    print("rabbitmqadmin {0}".format(VERSION))
    sys.exit(0)


def exit(s):
    eprint("*** {0}\n".format(s))
    sys.exit(1)


class RabbitmqManagement:

    def __init__(self, options):
        default_options = {"hostname": "localhost",
                           "port": "15672",
                           "path_prefix": "",
                           "declare_vhost": "/",
                           "username": "guest",
                           "password": "guest",
                           "ssl": False,
                           "request_timeout": 120,
                           "verbose": True,
                           "format": "table",
                           "depth": 1,
                           "bash_completion": False}

        self.options = default_options
        if options is not None:
            self.options.update(options)

    def get(self, path):
        return self.http("GET", "%s/api%s" % (self.options.get('path_prefix'), path), "")

    def put(self, path, body):
        return self.http("PUT", "%s/api%s" % (self.options.get('path_prefix'), path), body)

    def post(self, path, body):
        return self.http("POST", "%s/api%s" % (self.options.get('path_prefix'), path), body)

    def delete(self, path):
        return self.http("DELETE", "%s/api%s" % (self.options.get('path_prefix'), path), "")

    def __initialize_connection(self, hostname, port):
        if self.options.get('ssl'):
            return self.__initialize_https_connection(hostname, port)
        else:
            return httplib.HTTPConnection(hostname, port, timeout=self.options.get('request_timeout'))

    def __initialize_https_connection(self, hostname, port):
        # Python 2.7.9+
        if hasattr(ssl, 'create_default_context'):
            return httplib.HTTPSConnection(hostname, port, context=self.__initialize_tls_context())
        # Python < 2.7.8, note: those versions still have SSLv3 enabled
        #                       and other limitations. See rabbitmq/rabbitmq-management#225
        else:
            eprint("WARNING: rabbitmqadmin requires Python 2.7.9+ when HTTPS is used.")
            return httplib.HTTPSConnection(hostname, port,
                                           cert_file=self.options.get('ssl_cert_file'),
                                           key_file=self.options.get('ssl_key_file'))

    def __initialize_tls_context(self):
        # Python 2.7.9+ only
        ssl_ctx = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        ssl_ctx.options &= ~ssl.OP_NO_SSLv3

        ssl_insecure = self.options.get('ssl_insecure')
        ssl_disable_hostname_verification = ssl_insecure or self.options.get('ssl_disable_hostname_verification')
        # Note: you must set check_hostname prior to verify_mode
        if ssl_disable_hostname_verification:
            ssl_ctx.check_hostname = False
        if ssl_insecure:
            ssl_ctx.verify_mode = ssl.CERT_NONE

        if self.options.get('ssl_key_file'):
            ssl_ctx.load_cert_chain(self.options.get('ssl_cert_file'),
                                    self.options.get('ssl_key_file'))
        if self.options.get('ssl_ca_cert_file'):
            ssl_ctx.load_verify_locations(self.options.get('ssl_ca_cert_file'))
        return ssl_ctx

    def http(self, method, path, body):
        conn = self.__initialize_connection(self.options.get('hostname'), self.options.get('port'))
        auth = (self.options.get('username') + ":" + self.options.get('password'))

        headers = {"Authorization": "Basic " + b64(auth)}
        if body != "":
            headers["Content-Type"] = "application/json"
        try:
            conn.request(method, path, body, headers)
        except ConnectionRefusedError as e:
            exit("Could not connect: {0}".format(e))
        except socket.error as e:
            traceback.print_exc()
            exit("Could not connect: {0}".format(e))
        try:
            resp = conn.getresponse()
        except socket.timeout:
            exit("Timed out getting HTTP response (request timeout: {0} seconds)".format(
                self.options.get('request_timeout')))
        except (KeyboardInterrupt, SystemExit):
            raise
        except (Exception):
            e_fmt = traceback.format_exc()
            exit("Error getting HTTP response:\n\n{0}".format(e_fmt))
        if resp.status == 400:
            exit(json.loads(resp.read())['reason'])
        if resp.status == 401:
            exit("Access refused: {0}".format(path))
        if resp.status == 404:
            exit("Not found: {0}".format(path))
        if resp.status == 301:
            url = urlparse.urlparse(resp.getheader('location'))
            [host, port] = url.netloc.split(':')
            self.options.hostname = host
            self.options.port = int(port)
            return self.http(method, url.path + '?' + url.query, body)
        if resp.status > 400:
            raise Exception("Received response %d %s for path %s\n%s"
                            % (resp.status, resp.reason, path, resp.read()))
        return resp.read().decode('utf-8')

    def verbose(self, string):
        if self.options.get('verbose'):
            print(string)

    def export_def(self, path):
        uri = "/definitions"
        if self.options.get('vhost'):
            uri += "/%s" % quote_plus(self.options.get('vhost'))
        definitions = self.get(uri)
        f = open(path, 'w')
        f.write(definitions)
        f.close()

    def import_def(self, path):
        f = open(path, 'r')
        definitions = f.read()
        f.close()
        uri = "/definitions"
        if self.options.get('vhost'):
            uri += "/%s" % quote_plus(self.options.get('vhost'))
        self.post(uri, definitions)

    def get_queues(self):
        uri = "/queues"
        if self.options.get('vhost'):
            uri += "/%s" % quote_plus(self.options.get('vhost'))
        queues = self.get(uri)
        return json.loads(queues)

    def get_exchanges(self):
        uri = "/exchanges"
        if self.options.get('vhost'):
            uri += "/%s" % quote_plus(self.options.get('vhost'))
        exchanges = self.get(uri)
        return json.loads(exchanges)

    def get_bindings(self):
        uri = "/bindings"
        if self.options.get('vhost'):
            uri += "/%s" % quote_plus(self.options.get('vhost'))
        bindings = self.get(uri)
        return json.loads(bindings)


if __name__ == "__main__":
    rmq = RabbitmqManagement({
        'username': 'guest',
        'password': 'guest'
    })

    # rmq.export_def("/tmp/rmq.json")
    # print(rmq.get_queues())
    # print(rmq.get_exchanges())
    print(rmq.get_bindings())
