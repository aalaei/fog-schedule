import random

from twisted.internet import reactor
from twisted.internet.endpoints import TCP4ServerEndpoint
from time import sleep
import numpy as np

'''user defined imports'''
from controller_server import ControllerServerFactory
import schedule

CHECK_INTERVAL_MS = 1000
SCHEDULE_INTERVAL_MS = 1000
PROBLEM_GENERATION_INTERVAL_MS = 2_000

CONTROLLER_SERVER_PORT = 12345

difficulty_level = 5
all_tasks_queue = []


def problem_feeder():
    while True:
        all_tasks_queue.append(str(random.randint(1, 10)))
        sleep(PROBLEM_GENERATION_INTERVAL_MS / 1000)


schedule_task = schedule.schedule_task_random
# schedule_task = schedule.schedule_task_sjq


def manage_task(con):
    while True:
        if len(all_tasks_queue) > 0 and len(con.clients) > 0:
            client_id = schedule_task(con.clients)
            con.clients[client_id].chosen_task = eval(all_tasks_queue.pop(0))
            con.clients[client_id].send_message(value=1, type="comp_req")
            print("client #{} is chosen".format(client_id))
        sleep(SCHEDULE_INTERVAL_MS / 1000)


if __name__ == '__main__':
    endpoint = TCP4ServerEndpoint(reactor, CONTROLLER_SERVER_PORT)
    endpoint.listen(ControllerServerFactory(check_interval_ms=CHECK_INTERVAL_MS,
                                            difficulty_level=difficulty_level, manage_task=manage_task))
    reactor.callInThread(problem_feeder)
    reactor.run()
