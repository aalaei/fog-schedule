import random
import numpy as np
from colorama import Fore, Style


def schedule_task_sjq(fogs, request):
    client_id = min(fogs, key=lambda x: fogs[x].status.q_len)
    return client_id


def schedule_task_random(fogs, request):
    client_id = random.sample(fogs.keys(), 1)[0]
    return client_id


def schedule_task_service_time(fogs: dict, request):
    # t_ser_vector = []
    # for fog in fogs:
    #     t_ser = ((request['cmp_dmnd']/fog.status.cmp_cpcty)
    #         +(request['cmntn_dmnd']/fog.status.cmntn_rate)+(fog.status.q_len/fog.status.cmp_cpcty))
    #     t_ser_vector.append(t_ser)
    client_ids = []
    service_times = []

    for fog in fogs.keys():
        client_ids.append(fog)
        t = ((request['cmp_dmnd'] / fogs[fog].status.cmp_cpcty)
             + (request['cmntn_dmnd'] / fogs[fog].status.cmntn_rate) + (
                     fogs[fog].status.q_len / fogs[fog].status.cmp_cpcty))
        service_times.append(t)
        print(Fore.YELLOW + "client {}: ServiceTime={:.4f}".format(fog, t) + Style.RESET_ALL)

    service_times = np.array(service_times)
    client_ids = np.array(client_ids)
    client_id = client_ids[service_times.argmin()]
    # client_id2 = min(fogs, key=lambda x: ((request['cmp_dmnd'] / fogs[x].status.cmp_cpcty)
    #                                       + (request['cmntn_dmnd'] / fogs[x].status.cmntn_rate) + (
    #                                               fogs[x].status.q_len / fogs[x].status.cmp_cpcty))
    #                  )
    # assert client_id2 == client_id

    return client_id


def schedule_task_tmlns(fogs: dict, request):
    V = 1000
    client_ids = []
    service_times = []

    for fog in fogs.keys():
        client_ids.append(fog)
        t = ((request['cmp_dmnd'] / fogs[fog].status.cmp_cpcty)
             + (request['cmntn_dmnd'] / fogs[fog].status.cmntn_rate) + (
                     fogs[fog].status.q_len / fogs[fog].status.cmp_cpcty))
        service_times.append(t*V + fogs[fog].status.q_len)
        print(Fore.YELLOW + "client {}: ServiceTime={:.4f}".format(fog, t) + Style.RESET_ALL)

    service_times = np.array(service_times)
    client_ids = np.array(client_ids)
    client_id = client_ids[service_times.argmin()]
    # client_id2 = min(fogs, key=lambda x: ((request['cmp_dmnd'] / fogs[x].status.cmp_cpcty)
    #                                       + (request['cmntn_dmnd'] / fogs[x].status.cmntn_rate) + (
    #                                               fogs[x].status.q_len / fogs[x].status.cmp_cpcty))
    #                  )
    # assert client_id2 == client_id

    return client_id
