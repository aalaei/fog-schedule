import json


class Status:
    def __init__(self, obj):
        if obj is not None:
            self.id = obj['id']
            self.rssi = obj['rssi']
            self.q_len = obj['q_len']
            self.cmp_cpcty = obj['cmp_cpcty']
            self.cmntn_rate = obj['cmntn_rate']
        else:
            self.id = -1
            self.rssi = 1e-5
            self.cmp_cpcty = 1e-5
            self.cmntn_rate = 1e-5

            self.q_len = 0

    def __str__(self):
        return "id: {}, rssi: {:.2f}, q_len: {}, cmp_cpcty: {:.4f}, cmntn_rate: {:.2f} MBytes/s".format(
            self.id, self.rssi, self.q_len, self.cmp_cpcty, self.cmntn_rate/1048576)

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__)
