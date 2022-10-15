import socket
import warnings
import requests
import xml.etree.ElementTree as et


class Device:
    def __init__(self, ip=None, mac=None, raw_data=None, selected=False):
        self.ip = ip
        self.mac = mac
        self.raw_data = raw_data
        self.hostname = self.get_host_name()
        self.selected_device = selected
        self.pd_row = {"ip": self.ip, "hostname": self.hostname, "mac": self.mac}

        # defined variables
        self.device_data = None

    def get_host_name(self):
        if self.ip is not None:
            return socket.gethostbyaddr(self.ip)[0]
        else:
            raise warnings.warn("Can not gather host name ip address not provided")
            return None

    def get_device_info(self):
        query = f"http://{self.ip}:8060/query/device-info"
        response = requests.get(query)
        raw = response.text
        raw = raw.replace('\n', "")
        raw = raw.replace('\t', '')
        xml_parser = et.fromstring(raw)
        device_data = {}
        for child in xml_parser:
            device_data[child.tag] = child.text
        self.device_data = device_data
        return device_data

    def launch_home(self):
        query = f"http://{self.ip}:8060/keypress/home"
        requests.post(query)

    def launch_youtube(self, content_id):
        query = f"http://{self.ip}:8060/launch/837?contentId={content_id}&mediaType=live"
        requests.post(query)


