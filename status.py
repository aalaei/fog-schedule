import json


class Status:
    def __init__(self, obj):
        if obj is not None:
            self.id = obj['id']
            self.rssi = obj['rssi']
            self.q_len = obj['q_len']
        else:
            self.id = -1
            self.rssi = 0
            self.q_len = 0

    def __str__(self):
        return "id: {}, rssi: {:.2f}, q_len: {}".format(self.id, self.rssi, self.q_len)

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__)
