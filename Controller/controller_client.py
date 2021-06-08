import os
from colorama import Fore, Style
from twisted.internet import protocol
from twisted.internet.protocol import ReconnectingClientFactory as ClFactory
from computation import try_num
import struct


def verify_ans(chosen_task, ans, _difficulty_level):
    f = open(os.path.join("problems", "problem" + str(chosen_task) + ".txt"), "rb")
    problem_context = f.read()
    f.close()
    return try_num(problem_context, ans, _difficulty_level)


class ControllerClient(protocol.Protocol):
    def __init__(self, chosen_task, task_id, _difficulty_level):
        self.is_info_known = False
        self.file_content = ""
        self.chosen_task = chosen_task
        self.task_id = task_id
        self._difficulty_level = _difficulty_level
        self.start_download_time = None
        self.start_job_time = None
        self.task_done_time = None

    def send_message(self, mes, is_binary=False):
        if is_binary:
            self.transport.write(mes)
        else:
            self.transport.write(mes.encode("utf-8"))

    def connectionMade(self):
        f = open(os.path.join("problems", "problem" + str(self.chosen_task) + ".txt"), "rb")
        self.file_content = f.read()
        f.close()
        info = "{}/{}/{}".format(self.task_id, len(self.file_content), self._difficulty_level)
        self.send_message(info)

    def dataReceived(self, data):
        if self.is_info_known is False:
            self.send_message(self.file_content, is_binary=True)
            self.is_info_known = True
        else:

            (self.start_download_time, self.start_job_time, self.task_done_time, data) = struct.unpack('fffi', data)
            print("ans: {} is received from fog server".format(data))
            if verify_ans(self.chosen_task, data, self._difficulty_level):
                print(Fore.GREEN +
                      "ans is verified taken Time {:.2f}+{:.2f}={:.2f}".format(
                          self.start_job_time - self.start_download_time,
                          self.task_done_time - self.start_job_time,
                          self.task_done_time - self.start_download_time)
                      + Style.RESET_ALL)

            else:
                print(Fore.RED + "ans is not verified" + Style.RESET_ALL)
            self.transport.loseConnection()


class ControllerClientFactory(ClFactory):

    def __init__(self, chosen_task, task_id, _difficulty_level):
        self.chosen_task = chosen_task
        self.task_id = task_id
        self._difficulty_level = _difficulty_level

    def clientConnectionLost(self, connector, unused_reason):
        self.retry(connector)

    def clientConnectionFailed(self, connector, reason):
        print(reason)
        self.retry(connector)

    def buildProtocol(self, addr):
        return ControllerClient(self.chosen_task, self.task_id, self._difficulty_level)
