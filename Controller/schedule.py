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
                     fogs[fog].status.q_v / fogs[fog].status.cmp_cpcty))
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


def schedule_task_AFC(fogs: dict, request):
    v = 1000
    client_ids = []
    service_times = []
    energy = []

    for fog in fogs.keys():
        client_ids.append(fog)
        t = ((request['cmp_dmnd'] / fogs[fog].status.cmp_cpcty)
             + (request['cmntn_dmnd'] / fogs[fog].status.cmntn_rate) + (
                     fogs[fog].status.q_v / fogs[fog].status.cmp_cpcty))
        service_times.append(t * v + fogs[fog].status.q_v)
        e_cpu = (request['cmp_dmnd'] / fogs[fog].status.cmp_cpcty) * fogs[fog].status.cpu_power
        e_network = (request['cmntn_dmnd'] / fogs[fog].status.cmntn_rate) * fogs[fog].status.network_power
        energy.append(e_cpu + e_network)

        print(Fore.YELLOW + "client {}: ServiceTime={:.4f}, Energy: {:.04f}".format(fog, t, e_cpu + e_network)
              + Style.RESET_ALL)

    service_times = np.array(service_times)
    client_ids = np.array(client_ids)
    client_id = client_ids[service_times.argmin()]
    # client_id2 = min(fogs, key=lambda x: ((request['cmp_dmnd'] / fogs[x].status.cmp_cpcty)
    #                                       + (request['cmntn_dmnd'] / fogs[x].status.cmntn_rate) + (
    #                                               fogs[x].status.q_len / fogs[x].status.cmp_cpcty))
    #                  )
    # assert client_id2 == client_id

    return client_id


h_i_t = {}
z_i_t = {}
global g_t
g_t = 0


def schedule_task_tmlns(fogs: dict, request):
    v = 1000
    client_ids = []
    DpP = []
    C_D = 1  # ??
    C_L = 1  # ??

    B_max = max([fog.status.cmp_cpcty for fog in fogs.values()])
    q_v_average = sum([x.status.q_v for x in fogs.values()]) / len(fogs.keys())
    f_t = request['cmp_dmnd'] / request['cmntn_dmnd'] - C_L
    global g_t

    for fog in fogs.keys():
        client_ids.append(fog)
        t = ((request['cmp_dmnd'] / fogs[fog].status.cmp_cpcty)
             + (request['cmntn_dmnd'] / fogs[fog].status.cmntn_rate) + (
                     fogs[fog].status.q_v / fogs[fog].status.cmp_cpcty))
        e_cpu = (request['cmp_dmnd'] / fogs[fog].status.cmp_cpcty) * fogs[fog].status.cpu_power
        e_network = (request['cmntn_dmnd'] / fogs[fog].status.cmntn_rate) * fogs[fog].status.network_power
        total_energy = e_network + e_cpu
        Q_t = fogs[fog].status.q_v + request['cmp_dmnd']

        v_i = fogs[fog].status.cmp_cpcty / B_max
        g_i = fogs[fog].status.q_v / v_i - q_v_average

        y_t = max(0, t - request['deadlineTime']) - C_D

        DpP.append(total_energy * v + Q_t * (h_i_t.get(fog, 0) / v_i + 1) + z_i_t.get(fog, 0) * y_t + g_t * f_t)

        print(Fore.YELLOW + "client {}: ServiceTime={:.4f}, Energy: {:.04f}".format(fog, t, total_energy)
              + Style.RESET_ALL)

        h_i_t[fog] = h_i_t.get(fog, 0) + g_i
        z_i_t[fog] = max(z_i_t.get(fog, 0) + y_t, 0)

    g_t = max(0, g_t + f_t)

    np_DpPs = np.array(DpP)
    client_ids = np.array(client_ids)
    client_id = client_ids[np_DpPs.argmin()]
    return client_id
