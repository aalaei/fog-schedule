from twisted.internet import reactor, protocol
from twisted.internet.protocol import ServerFactory as SrFactory, connectionDone
import numpy as np
from time import time


class FogServer(protocol.Protocol):
    def __init__(self, clients: dict, my_id, problem_prefix, enqueue_task):
        self.my_id = my_id
        self.clients = clients
        self.remainingBytes = -np.inf
        self.task_id = None
        self.file = None
        self.difficulty_level = 0
        self.problem_prefix = problem_prefix
        self.enqueue_task = enqueue_task
        self.start_download_time = None
        self.start_job_time = None
        self.task_done_time = None

    def connectionMade(self):
        print("FOG server: new connection from id={}".format(self.my_id))
        self.clients[self.my_id] = self

    def send_message(self, mes, is_binary=False):
        if is_binary:
            self.transport.write(mes)
        else:
            self.transport.write(mes.encode("utf-8"))

    def dataReceived(self, data):
        if self.remainingBytes < 0:
            self.start_download_time = time()
            self.task_id, self.remainingBytes, self.difficulty_level = [eval(x) for x in
                                                                        data.decode("utf-8").split("/")]
            self.file = open(self.problem_prefix + str(self.task_id) + ".txt", "wb")
            self.send_message(str("1"))
            print("network: task {} with difficultyLevel={} is downloading".format(self.task_id, self.difficulty_level))
            return
        elif self.remainingBytes > 0 and self.file is not None:
            self.file.write(data)
            self.remainingBytes -= len(data)
            print("network: progress on task {}, {} byte is remaining".format(self.task_id, self.remainingBytes))

        if self.remainingBytes <= 0 and self.file is not None:
            self.file.close()
            print("network: task {} is downloaded completely".format(self.task_id))
            self.enqueue_task(str(self.task_id))

    def connectionLost(self, reason=connectionDone):
        self.disconnect()

    def disconnect(self):
        del self.clients[self.my_id]


class FogServerFactory(SrFactory):
    def __init__(self, problem_prefix, manage_tasks, enqueue_task):
        self.clients = {}
        self.last_id = 0
        self.problem_prefix = problem_prefix
        self.enqueue_task = enqueue_task
        reactor.callInThread(manage_tasks, self)

    def buildProtocol(self, addr):
        self.last_id += 1
        return FogServer(self.clients, self.last_id, self.problem_prefix, self.enqueue_task)
