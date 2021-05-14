import resource_object
import threading
import pandas

class CapacityManager:

    mem_limit_threshold = 90
    mem_request_threshold = 90
    cpu_limit_threshold = 90
    cpu_request_threshold = 90

    def __init__(self,
                 scanner,
                 notifiers,
                 interval=30,
                 mem_limit_threshold=90,
                 mem_request_threshold=90,
                 cpu_limit_threshold=90,
                 cpu_request_threshold=90,
                 max_hit=100,
                 report_type='all'):
        self.scanner = scanner
        self.notifiers = notifiers
        self.interval = interval
        self.mem_limit_threshold = mem_limit_threshold
        self.mem_request_threshold = mem_request_threshold
        self.cpu_limit_threshold = cpu_limit_threshold
        self.cpu_request_threshold = cpu_request_threshold
        self.max_hit = max_hit
        self.report_type = report_type
        self.running = False
        self.__initialization()

    def __initialization(self):
        self.node_list = {}
        self.pod_list = {}
        self.mem_limit_query = f"mem_limit > {self.mem_limit_threshold}"
        self.mem_request_query = f"mem_requests > {self.mem_request_threshold}"
        self.cpu_limit_query = f"cpu_limit > {self.cpu_limit_threshold}"
        self.cpu_request_query = f"cpu_requests > {self.cpu_request_threshold}"

    def report(self):
        nodes, pods = self.scanner.scan()
        return nodes.to_json(), pods.to_json()

    def test(self):
        nodes, pods = self.scanner.scan()
        return nodes, pods

    def start(self):
        if ~self.running:
            self.running = True
            self.scan_resources()
            return 'Service is started!'
        else:
            return 'Service is already started!'

    def stop(self):
        if self.running:
            self.running = False
            return 'Service is stopped!'
        else:
            return 'No service is running!'

    def status(self):
        return self.running

    def scan_resources(self):
        print(self.running)
        if self.running:
            threading.Timer(self.interval, self.scan_resources).start()
        self.update()

    def __generate_report(self):
        report = ''
        for key in self.node_list:
            message = self.node_list[key].get_notification(self.report_type)
            if message != '':
                report += f"{message}\n"
        for key in self.pod_list:
            message = self.pod_list[key].get_notification(self.report_type)
            if message != '':
                report += f"{message}\n"
        return report

    def __notify(self):
        for notifier in self.notifiers:
            notifier.notify(self.__generate_report())

    def update(self):
        self.__update_data()
        self.__notify()

    def __update_data(self):
        nodes, pods = self.scanner.scan()
        self.__update_nodes(nodes)
        self.__update_pods(pods)

    def __update_nodes(self, nodes):
        node_keys = list(self.node_list.keys())
        critical_nodes = pandas.concat([
            nodes.query(self.mem_limit_query),
            nodes.query(self.mem_request_query),
            nodes.query(self.cpu_limit_query),
            nodes.query(self.cpu_request_query)
        ], ignore_index=True).drop_duplicates()
        for index, node in critical_nodes.iterrows():
            key = node['node_name']
            if key not in node_keys:
                self.node_list[key] = self.__create_object('node', key)
            else:
                node_keys.remove(key)
            self.node_list[key].update_memory(node['mem_requests'], node['mem_limit'])
            self.node_list[key].update_cpu(node['cpu_requests'], node['cpu_limit'])
        self.__cleanup_nodes(node_keys)

    def __update_pods(self, pods):
        pod_keys = list(self.pod_list.keys())
        critical_pods = pandas.concat([
            pods.query(self.mem_limit_query),
            pods.query(self.mem_request_query),
            pods.query(self.cpu_limit_query),
            pods.query(self.cpu_request_query)
        ], ignore_index=True).drop_duplicates()
        for index, pod in critical_pods.iterrows():
            key = f"{pod['node_name']}_{pod['pod_name']}"
            if key not in pod_keys:
                self.pod_list[key] = self.__create_object('pod', key)
            else:
                pod_keys.remove(key)
            self.pod_list[key].update_memory(pod['mem_requests'], pod['mem_limit'])
            self.pod_list[key].update_cpu(pod['cpu_requests'], pod['cpu_limit'])
        self.__cleanup_nodes(pod_keys)

    def __cleanup_nodes(self, keys):
        for key in keys:
            self.node_list.pop(key)

    def __cleanup_pods(self, keys):
        for key in keys:
            self.pod_list.pop(key)

    def __create_object(self, object_type, key):
        return resource_object.ResourceObject(
            object_type,
            key,
            self.mem_limit_threshold,
            self.mem_request_threshold,
            self.cpu_limit_threshold,
            self.cpu_request_threshold,
            self.max_hit)
