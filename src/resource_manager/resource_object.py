
class ResourceObject:
    def __init__(self,
                 resource_type,
                 resource_name,
                 mem_limit_threshold,
                 mem_request_threshold,
                 cpu_limit_threshold,
                 cpu_request_threshold,
                 max_hit):
        self.resource_type = resource_type
        self.resource_name = resource_name
        self.cpu_limit = 0
        self.mem_limit = 0
        self.cpu_request = 0
        self.mem_request = 0
        self.mem_hits = 0
        self.cpu_hits = 0

        self.mem_limit_hits = 0
        self.cpu_limit_hits = 0
        self.mem_req_hits = 0
        self.cpu_req_hits = 0

        self.mem_limit_threshold = mem_limit_threshold
        self.mem_request_threshold = mem_request_threshold
        self.cpu_limit_threshold = cpu_limit_threshold
        self.cpu_request_threshold = cpu_request_threshold
        self.max_hit = max_hit

    def __hit_cpu(self):
        if self.cpu_limit > self.cpu_limit_threshold or self.cpu_request > self.cpu_request_threshold:
            self.cpu_hits += 1
            if self.cpu_limit > self.cpu_limit_threshold:
                self.cpu_limit_hits +=1
                self.cpu_hits = min(self.cpu_hits, self.cpu_limit_hits)
            else:
                self.cpu_limit_hits = 0

            if self.cpu_request > self.cpu_request_threshold:
                self.cpu_limit_hits +=1
                self.cpu_hits = min(self.cpu_hits, self.cpu_req_hits)
            else:
                self.cpu_req_hits = 0

            if self.cpu_hits > self.max_hit:
                self.cpu_hits = 1
        else:
            self.cpu_hits = 0
            self.cpu_req_hits = 0
            self.cpu_limit_hits = 0

    def __hit_mem(self):
        if self.mem_limit > self.mem_limit_threshold or self.mem_request > self.mem_request_threshold:
            self.mem_hits += 1
            if self.mem_limit > self.mem_limit_threshold:
                self.mem_limit_hits +=1
                self.mem_hits = min(self.mem_hits, self.mem_limit_hits)
            else:
                self.mem_limit_hits = 0

            if self.mem_request > self.mem_request_threshold:
                self.mem_limit_hits +=1
                self.mem_hits = min(self.mem_hits, self.mem_req_hits)
            else:
                self.mem_req_hits = 0

            if self.mem_hits > self.max_hit:
                self.mem_hits = 1
        else:
            self.mem_req_hits = 0
            self.mem_limit_hits = 0
            self.mem_hits = 0

    def update_memory(self, limit, request):
        self.mem_limit = limit
        self.mem_request = request
        self.__hit_mem()

    def update_cpu(self, limit, request):
        self.cpu_limit = limit
        self.cpu_request = request
        self.__hit_cpu()

    def get_notification(self, watch_type):
        message = ''
        cpu_message = ''
        mem_message = ''
        if self.cpu_hits > 0:
            cpu_message = f" [cpu request: {self.cpu_request}% , cpu limit: {self.cpu_limit}%]"
        if self.mem_hits > 0:
            mem_message = f" [memory request: {self.mem_request}% , memory limit: {self.mem_limit}%]"

        if watch_type=="all" and (self.cpu_hits==1 or self.mem_hits == 1):
            if self.cpu_hits>0 and self.mem_hits>0:
                message = ' and'
            message = cpu_message+message+mem_message
        elif watch_type == 'cpu' and self.cpu_hits == 1:
            message = cpu_message
        elif watch_type == 'memory' and self.mem_hits == 1:
            message = mem_message

        if message != '':
            message = f"{self.resource_type} {self.resource_name} is under stress:{message}"

        return message

