import random
import json
from sys import stderr
from time import time, sleep
from twisted.internet import reactor, protocol
from twisted.internet.protocol import ReconnectingClientFactory as ClFactory
from status import Status

last_job_id = 1


class FogClient(protocol.Protocol):
    def __init__(self, all_clients: list, status, fog_server_port):
        self.status = status
        self.all_clients = all_clients
        self.FOG_SERVER_PORT = fog_server_port
        print("Created")
        reactor.callInThread(self.message_input)
        reactor.callInThread(self.update_status)

    @staticmethod
    def __encode_json(**kwargs):
        return json.dumps(kwargs)

    def send_message(self, **kwargs):
        self.transport.write(self.__encode_json(**kwargs).encode("utf-8"))

    def set_status(self, status):
        self.status = status

    def update_status(self):
        while True:
            sleep(1)
            self.status.rssi = random.random()

    def message_input(self):
        while True:
            self.send_message(value=input("value:"), type=input("type:"))

    def connectionMade(self):
        self.send_message(type="id_req", value=1)

    def parse_single_command(self, data):
        try:
            data = json.loads(data)
        except UnicodeDecodeError or json.JSONDecodeError:
            print("Something went wrong :(", file=stderr)
            return

        if data['type'] == 'error':
            print(data.get('value', "Unknown error"), file=stderr)
        if data['type'] == 'id_res':
            self.status.id = data['value']['self']
            self.all_clients = data['value']['all']
            print("my id is {}".format(self.status.id))
        elif data['type'] == 'ping':
            self.send_message(type="cl_status", value=self.status.to_json())
        elif data['type'] == 'comp_req':
            global last_job_id
            self.send_message(type="comp_res", value="{}/{}".format(self.FOG_SERVER_PORT, last_job_id))
            last_job_id += 1
        else:
            print(data.get('value', "No value in the message"))

    def dataReceived(self, data):
        data = data.decode("utf-8")
        data = data[1:-1].split("}{")
        for dt in data:
            self.parse_single_command("{" + dt + "}")


class FogClientFactory(ClFactory):

    def __init__(self, fog_server_port):
        self.fog_server_port=fog_server_port
        self.all_clients = []
        self.status = Status(None)

    def clientConnectionLost(self, connector, unused_reason):
        self.retry(connector)

    def clientConnectionFailed(self, connector, reason):
        print(reason)
        self.retry(connector)

    def buildProtocol(self, addr):
        return FogClient(all_clients=self.all_clients, status=self.status, fog_server_port=self.fog_server_port)