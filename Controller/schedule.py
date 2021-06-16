import random


def schedule_task_sjq(fogs, request):
    client_id = min(fogs, key=lambda x: fogs[x].status.q_len)
    return client_id


def schedule_task_random(fogs, request):
    client_id = random.sample(fogs.keys(), 1)[0]
    return client_id


def schedule_task_tmlns(fogs, request):
    # t_ser_vector = []
    # for fog in fogs:
    #     t_ser = ((request['cmp_dmnd']/fog.status.cmp_cpcty)
    #         +(request['cmntn_dmnd']/fog.status.cmntn_rate)+(fog.status.q_len/fog.status.cmp_cpcty))
    #     t_ser_vector.append(t_ser)
    
    client_id = min(fogs, key=lambda x: ((request['cmp_dmnd']/fogs[x].status.cmp_cpcty)
            +(request['cmntn_dmnd']/fogs[x].status.cmntn_rate)+(fogs[x].status.q_len/fogs[x].status.cmp_cpcty))
            )

    return client_id