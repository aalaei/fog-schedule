import random


def schedule_task_sjq(fogs):
    client_id = min(fogs, key=lambda x: fogs[x].status.q_len)
    return client_id


def schedule_task_random(fogs):
    client_id = random.sample(fogs.keys(), 1)[0]
    return client_id
