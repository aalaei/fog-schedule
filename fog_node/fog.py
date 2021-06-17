import os.path
import random
import shutil
import struct
import sys
from time import time, sleep

from colorama import Fore, Style
from twisted.internet import reactor
from twisted.internet.endpoints import TCP4ClientEndpoint, TCP4ServerEndpoint

sys.path.insert(0, '..')

'''user defined imports'''
from computation import computational_task, diff2dmnd
from fog_client import FogClientFactory
from fog_server import FogServerFactory

CONTROLLER_SERVER_IP = "172.21.48.59"
CONTROLLER_SERVER_PORT = 12345

FOG_SERVER_IP = "172.21.48.63"

# CONTROLLER_SERVER_IP = "127.0.0.1"
# FOG_SERVER_IP = "127.0.0.1"

FOG_SERVER_PORT = random.randint(10000, 65535)

problem_prefix = "pr{}/".format(random.randint(1, 99999999))
tasks_queue = []
global cmntn_rate, cmp_cpcty
cmntn_rate = 1e10
cmp_cpcty = 1e10


def manage_tasks(connections):
    while True:
        sleep(0.001)
        if len(tasks_queue) > 0:
            name = tasks_queue.pop(0)
            print("task {} is chosen".format(name))
            related_connections = [x for x in connections.clients.values() if str(x.task_id) == name]
            assert len(related_connections) == 1
            print("task {} is running".format(name))
            fog_server_obj = related_connections[0]
            fog_server_obj.start_job_time = time()
            file_name = problem_prefix + name + ".txt"
            res = computational_task(file_name, fog_server_obj.difficulty_level)
            fog_server_obj.task_done_time = time()
            ref_time = int(fog_server_obj.start_download_time)
            global cmntn_rate, cmp_cpcty

            cmntn_rate = fog_server_obj.problem_transfer_throughput
            cmp_cpcty = diff2dmnd(fog_server_obj.difficulty_level) / \
                        (fog_server_obj.task_done_time - fog_server_obj.start_job_time)

            fog_server_obj.send_message(struct.pack('dddQQ', fog_server_obj.start_download_time - ref_time,
                                                    fog_server_obj.start_job_time - ref_time,
                                                    fog_server_obj.task_done_time - ref_time,
                                                    int(fog_server_obj.problem_transfer_throughput),
                                                    int(res)), is_binary=True)
            print(Fore.GREEN + "task {} is done completely".format(name) + Style.RESET_ALL)
            # fog_server_obj.transport.loseConnection()


def enqueue_task(name):
    tasks_queue.append(name)


def update_status(conn):
    global cmntn_rate, cmp_cpcty
    while True:
        conn.status.rssi = random.random()
        conn.status.q_len = len(tasks_queue)
        conn.status.cmp_cpcty = cmp_cpcty
        conn.status.cmntn_rate = cmntn_rate
        sleep(0.1)


if __name__ == '__main__':
    if os.path.exists(problem_prefix) and os.path.isdir(problem_prefix):
        shutil.rmtree(problem_prefix)

    os.mkdir(problem_prefix)
    endpoint = TCP4ClientEndpoint(reactor, CONTROLLER_SERVER_IP, CONTROLLER_SERVER_PORT)
    endpoint.connect(FogClientFactory(fog_server_ip=FOG_SERVER_IP, fog_server_port=FOG_SERVER_PORT
                                      , update_status_func=update_status))

    endpoint2 = TCP4ServerEndpoint(reactor, FOG_SERVER_PORT)
    endpoint2.listen(FogServerFactory(problem_prefix, manage_tasks, enqueue_task))
    reactor.run()
