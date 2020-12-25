import re

import pkg_resources
from omc.core.decorator import filecache

from omc.common import CmdTaskMixin
from omc.core import Resource
from omc.utils import JmxTermUtils


class Bean(Resource, CmdTaskMixin):
    def _run(self):
        pass

    @filecache(duration=60 * 60, file=Resource._get_cache_file_name)
    def _completion(self, short_mode=False):
        results = []

        results.append(super()._completion(True))

        if not self._have_resource_value():
            jmx = self.context['jmx'][0] if self.context['jmx'] else ''
            cmd = JmxTermUtils.build_command('open %s && beans' % jmx)
            result = self.run_cmd(cmd, capture_output=True)
            output = result.stdout.decode("utf-8").splitlines()
            output = list(map(lambda x: x.replace(":", "\:"), output))
            results.extend(self._get_completion(output, True))

        return '\n'.join(results)

    def info(self):
        jmxterm = pkg_resources.resource_filename(__name__, '../../../lib/jmxterm-1.0.2-uber.jar')
        jmx = self._get_one_resource_value('jmx')
        bean = self._get_one_resource_value()
        bean = bean.replace(" ", "\\ ")
        cmd = 'echo "open %s && bean %s && info"  | java -jar %s -n' % (jmx, bean, jmxterm)
        self.run_cmd(cmd)

    def exec(self):
        if 'completion' in self._get_params():
            jmx = self._get_one_resource_value('jmx')
            bean = self._get_one_resource_value()
            bean = bean.replace(" ", "\\ ")
            short_cmd = "open %s && bean %s && info" % (jmx, bean)
            result = self.run_cmd(JmxTermUtils.build_command(short_cmd), capture_output=True, verbose=False)
            output = result.stdout.decode('utf-8').splitlines()
            for one_attr in (self._list_operation_resources(self._parse_info(output))):
                print(one_attr['method'] + ":" + one_attr['raw_data'])
        else:
            attr_name = ' '.join(self._get_params())
            jmx = self._get_one_resource_value('jmx')
            bean = self._get_one_resource_value()
            bean = bean.replace(" ", "\\ ")
            cmd = "open %s && bean %s && run %s" % (jmx, bean, attr_name)
            # cmd = 'echo "open %s && bean %s && set %s"  | java -jar %s -n' % (jmx, bean, attr_name, jmxterm)
            self.run_cmd(JmxTermUtils.build_command(cmd))

    def get(self):
        if 'completion' in self._get_params():
            jmx = self.context['jmx']
            bean = self._get_resource_values()[0]
            bean = bean.replace(" ", "\\ ")
            short_cmd = "open %s && bean %s && info" % (jmx, bean)
            result = self.run_cmd(JmxTermUtils.build_command(short_cmd), capture_output=True, verbose=False)

            output = result.stdout.decode('utf-8').splitlines()
            for one_attr in (self._list_readable_resources(self._parse_info(output))):
                print(one_attr['attribute'] + ":" + one_attr['raw_data'])
        else:
            attr_name = ' '.join(self._get_params())
            jmxterm = pkg_resources.resource_filename(__name__, '../../../lib/jmxterm-1.0.2-uber.jar')
            jmx = self._get_one_resource_value('jmx')
            bean = self._get_one_resource_value()
            bean = bean.replace(" ", "\\ ")
            cmd = 'echo "open %s && bean %s && get %s"  | java -jar %s -n' % (jmx, bean, attr_name, jmxterm)
            self.run_cmd(cmd)

    def set(self):
        if 'completion' in self._get_params():
            jmx = self._get_one_resource_value('jmx')
            bean = self._get_one_resource_value()
            bean = bean.replace(" ", "\\ ")
            short_cmd = "open %s && bean %s && info" % (jmx, bean)
            result = self.run_cmd(JmxTermUtils.build_command(short_cmd), capture_output=True, verbose=False)
            output = result.stdout.decode('utf-8').splitlines()
            for one_attr in (self._list_writable_resources(self._parse_info(output))):
                print(one_attr['attribute'] + ":" + one_attr['raw_data'])
        else:
            attr_name = ' '.join(self._get_params())
            jmx = self._get_one_resource_value('jmx')
            bean = self._get_one_resource_value()
            bean = bean.replace(" ", "\\ ")
            cmd = "open %s && bean %s && set %s" % (jmx, bean, attr_name)
            self.run_cmd(JmxTermUtils.build_command(cmd))

    def _parse_info(self, result):
        # notification parser is not support right now, should find a example

        '''
        # attributes
        %0   - className (java.lang.String, r)
        %1   - configBaseName (java.lang.String, r)
        %2   - contextClass (java.lang.String, rw)
        %3   - copyXML (boolean, rw)
        %4   - deployXML (boolean, rw)
        %5   - modelerType (java.lang.String, r)
        %6   - unpackWARs (boolean, rw)
        # operations
        %0   - void addServiced(java.lang.String name)
        %1   - void check(java.lang.String name)
        %2   - void checkUndeploy()
        %3   - long getDeploymentTime(java.lang.String name)
        %4   - boolean isDeployed(java.lang.String name)
        %5   - boolean isServiced(java.lang.String name)
        %6   - void manageApp(org.apache.catalina.Context context)
        %7   - void removeServiced(java.lang.String name)
        %8   - void unmanageApp(java.lang.String contextPath)
        '''

        # there's no notifications
        attr_lines = []
        ops_lines = []
        notification_lines = []

        current_section = None
        for line in result:
            if line is None or not line.strip():
                continue

            if '# attributes' in line:
                current_section = 'attributes'
                continue
            if '# operations' in line:
                current_section = 'operations'
                continue

            if '# notifications' in line:
                current_section = 'notifications'
                continue

            if '#there' in line:
                # no content found, e.g. '#there's no notification'
                current_section = None

            if line.startswith('#'):
                # end of section, unknown section
                break

            if current_section == 'attributes':
                attr_lines.append(line)

            if current_section == 'operations':
                ops_lines.append(line)

            if current_section == 'notifications':
                notification_lines.append(line)

            if not current_section:
                continue

        return {
            'attrs': attr_lines,
            'ops': ops_lines,
            'notifications': notification_lines
        }

    def _list_readable_resources(self, parsed_info):
        results = []
        for one_attr_line in parsed_info['attrs']:
            one_result = self._parse_one_attr_line(one_attr_line)
            if one_result['readable']:
                results.append(one_result)
        return results

    def _list_writable_resources(self, parsed_info):
        results = []
        for one_attr_line in parsed_info['attrs']:
            one_result = self._parse_one_attr_line(one_attr_line)
            if one_result['writable']:
                results.append(one_result)
        return results

    def _list_operation_resources(self, parsed_info):
        results = []
        for one_ops_line in parsed_info['ops']:
            one_result = self._parse_one_opeartion_line(one_ops_line)
            results.append(one_result)
        return results

    def _parse_one_attr_line(self, attr):
        # example: '%0   - className (java.lang.String, r)'

        try:
            parsed_result = re.match('.*-(.*)\((.*), (\w+)\)', attr).groups()

            permission = parsed_result[2].strip()

            result = {
                'attribute': parsed_result[0].strip(),
                'param_type': parsed_result[1].strip(),
                'readable': 'r' in permission,
                'writable': 'w' in permission,
                'raw_data': attr
            }

            return result
        except Exception as inst:
            raise Exception("attr: " + str(attr), inst)

    def _parse_one_opeartion_line(self, ops):
        # %0   - void addServiced(java.lang.String name)
        try:
            parsed_result = re.match(".*- ([\w\.]+)(.*)\((.*)\)", ops).groups()

            result = {
                'return': parsed_result[0].strip(),
                'method': parsed_result[1].strip(),
                'param': parsed_result[2].strip(),
                'raw_data': ops
            }
            return result
        except Exception as inst:
            raise Exception("ops: " + str(ops), inst)
            # raise AttributeError(ops)


if __name__ == '__main__':
    result = '''
        # attributes
        %0   - className (java.lang.String, r)
        %1   - configBaseName (java.lang.String, r)
        %2   - contextClass (java.lang.String, rw)
        %3   - copyXML (boolean, rw)
        %4   - deployXML (boolean, rw)
        %5   - modelerType (java.lang.String, r)
        %6   - unpackWARs (boolean, rw)
        # operations
        %0   - void addServiced(java.lang.String name)
        %1   - void check(java.lang.String name)
        %2   - void checkUndeploy()
        %3   - long getDeploymentTime(java.lang.String name)
        %4   - boolean isDeployed(java.lang.String name)
        %5   - boolean isServiced(java.lang.String name)
        %6   - void manageApp(org.apache.catalina.Context context)
        %7   - void removeServiced(java.lang.String name)
        %8   - void unmanageApp(java.lang.String contextPath)
        '''
    #
    # result = (Bean()._parse_info(result.splitlines()))
    # for one_attr in result['attrs']:
    #     print(Bean()._parse_attr(one_attr))
    #
    # for one_op in result['ops']:
    #     print(Bean()._parse_opeartion(one_op))
