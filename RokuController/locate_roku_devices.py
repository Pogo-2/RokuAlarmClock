from ssdpy import SSDPClient
from RokuController import Device


def locate_roku_devices():
    device_list = []
    for x in range(5):
        client = SSDPClient()
        client.broadcast_ip = "239.255.255.250"
        client.port = "1900"
        devices = client.m_search(st="roku:ecp", mx=4)
        for device in devices:
            device_list.append(Device(device["location"][7:-1].split(":")[0], device["wakeup"].split(";")[0][4:], device))

        if len(device_list) > 0:
            return device_list
        else:
            continue
    return device_list
