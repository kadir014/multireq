#      multireq - Multiple requests
#          Kadir Aksoy - 2020
# https://github.com/kadir014/multireq


import threading
import requests
import time


class Request(threading.Thread):
    def __init__(self, url, method="GET", headers=None, data=None):
        super().__init__()
        self.url = url
        self.method = method
        self.headers = headers
        self.data = data

        self.pool = None
        self.running = False
        self.done = False

    def __repr__(self):
        return f"<Request({self.method}, {self.url})>"

    def run(self):
        try:
            r = requests.request(self.method, self.url, timeout=self.pool.timeout_limit)
        except requests.exceptions.ReadTimeout as e:
            self.pool.tasks[self] = Response(None, fail=True)
            self.running = False
            self.done = True
            return

        self.pool.tasks[self] = Response(r)
        self.running = False
        self.done = True


class Response:
    def __init__(self, request_response, fail=False):
        if fail:
            self.successful = False

            self.code    = -1
            self.reason  = ""
            self.content = b""
            self.text    = ""

            self.headers = None
            self.cookies = None

        else:
            self.successful = True

            self.code    = request_response.status_code
            self.reason  = request_response.reason
            self.content = request_response.content
            self.text    = request_response.text

            self.headers = request_response.headers
            self.cookies = request_response.cookies

    def __repr__(self):
        if self.successful:
            return f"<Response(Successful, code={self.code})>"

        else:
            return "<Response(Failed)>"


class ElapsedTime:
    def __init__(self, dt):
        self.micros = int(dt * 1000000)
        self.microsf = dt * 1000000
        self.millis = int(dt * 1000)
        self.millisf = dt * 1000
        self.secs   = dt
        self.mins   = dt / 60
        self.hours  = self.mins / 60
        self.days   = self.hours / 24

    def __repr__(self):
        return f"<ElapsedTime({self.micros} microseconds, {self.millis} milliseconds, {self.secs} seconds, {self.mins} minutes)>"


class ResponseList:
    def __init__(self, task_dict, elapsed):
        self.__task_dict = task_dict
        self.elapsed = elapsed

    def __repr__(self):
        return f"<ResponseList({len(self.__task_dict)} responses)>"

    def __len__(self):
        return len(self.__task_dict)

    def __getitem__(self, index):
        return self.__task_dict[index]

    def get_successful(self, first=False):
        found = list()
        for r in self.__task_dict:
            if self.__task_dict[r].successful:
                if first:
                    return self.__task_dict[r]
                else:
                    found.append(self.__task_dict[r])

        return found

    def get_failed(self, first=False):
        found = list()
        for r in self.__task_dict:
            if not self.__task_dict[r].successful:
                if first:
                    return self.__task_dict[r]
                else:
                    found.append(self.__task_dict[r])

        return found

    def get_by_code(self, code, first=False):
        found = list()
        for r in self.__task_dict:
            if self.__task_dict[r].code == code:
                if first:
                    return self.__task_dict[r]
                else:
                    found.append(self.__task_dict[r])

        return found

    def get_by_url(self, url, first=False):
        found = list()
        for r in self.__task_dict:
            if r.url == url:
                if first:
                    return self.__task_dict[r]
                else:
                    found.append(self.__task_dict[r])

        return found


class RequestPool:
    def __init__(self, request_list, group_limit=10, timeout_limit=5):
        super().__init__()
        self.running = False
        self.request_list = request_list
        self.tasks = {r:None for r in request_list}
        for task in self.tasks: task.pool = self

        self.group_limit = 10
        self.timeout_limit = 5

    def start_and_wait(self):
        self.running = True
        start = time.time()
        self.run_and_wait()
        end = time.time() - start
        self.running = False
        return ResponseList(self.tasks, ElapsedTime(end))

    def is_done(self, group):
        for req in group:
            if not req.done: return False
        return True

    def run_and_wait(self):
        if len(self.request_list) > self.group_limit:
            groups = int(len(self.request_list)/self.group_limit) + (len(self.request_list) % self.group_limit)
        else:
            groups = 1

        for g in range(groups):
            current_group = list()
            for req in self.request_list:
                if not req.running and not req.done:
                    req.running = True
                    current_group.append(req)
                    req.start()

            while not self.is_done(current_group): pass

        self.request_list.clear()
