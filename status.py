import json


class Status:
    def __init__(self, obj):
        if obj is not None:
            self.id = obj['id']
            self.rssi = obj['rssi']
        else:
            self.id = -1
            self.rssi = 0

    def __str__(self):
        return "id: {}, rssi: {}".format(self.id, self.rssi)

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__)

