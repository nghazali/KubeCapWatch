import subprocess
import json
from builtins import list
import pandas

class Scanner:
    def __init__(self, scope, namespace):
        self.scope = scope
        self.namespace = namespace
    __node_columns = [
        'node_name',
        'cpu_requests',
        'mem_requests',
        'cpu_limit',
        'mem_limit'
    ]
    __pod_columns = [
        'node_name',
        'pod_name',
        'namespace',
        'cpu_requests',
        'mem_requests',
        'cpu_limit',
        'mem_limit'
    ]

    def scan(self):
        nodes = self.__get_nodes()
        pods = []
        if self.scope == 'all' or self.scope == 'pod':
            pods = self.__get_pods()
        pandas.DataFrame()

        return nodes, pods

    def __get_nodes(self):
        data = self.__scan_node_status()
        nodes = []
        [nodes.append([node['name'],
                       int(node['cpu']['requestsPercent'].strip('%')),
                       int(node['memory']['requestsPercent'].strip('%')),
                       int(node['cpu']['limitsPercent'].strip('%')),
                       int(node['memory']['limitsPercent'].strip('%'))])
            for node in data['nodes']]
        return pandas.DataFrame(data=nodes, columns=self.__node_columns)

    def __get_pods(self):
        data = self.__scan_pod_status()
        pods = []
        for node in data['nodes']:
            [pods.append([node['name'],
                          pod['name'],
                          pod['namespace'],
                          int(pod['cpu']['requestsPercent'].strip('%')),
                          int(pod['memory']['requestsPercent'].strip('%')),
                          int(pod['cpu']['limitsPercent'].strip('%')),
                          int(pod['memory']['limitsPercent'].strip('%'))])
                  for pod in node['pods']]
        iterator = filter(self.namespace_iterator, pods)
        pods = list(iterator)
        return pandas.DataFrame(data=pods, columns=self.__pod_columns)

    def __scan_node_status(self):
        process = subprocess.Popen(['kube-capacity', '-o', 'json'],
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        jdata = json.loads(stdout.decode('utf8').replace("'", '"'))

        return jdata

    def __scan_pod_status(self):
        process = subprocess.Popen(['kube-capacity', '--pods', '-o', 'json'],
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        jdata = json.loads(stdout.decode('utf8').replace("'", '"'))
        return jdata

    def namespace_iterator(self, item):
        if self.namespace == '':
            return True
        return item[2] in self.namespace
