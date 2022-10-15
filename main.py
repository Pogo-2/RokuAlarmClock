import warnings
import RokuController as rc
import pandas as pd
import json
import sys
import time
from datetime import datetime
from random import randint

# import variables from config and create ect vars
with open("./config.json", "r") as f:
    cfg = json.loads(f.read())
dl = None

# search logic
if cfg["ask_to_search"]:
    device_list = rc.locate_roku_devices()
    if len(device_list) <= 0:
        sys.exit("could not locate devices")

    pd_list = []
    for row in device_list:
        pd_list.append(row.pd_row)
    dl = pd.DataFrame(pd_list)
    if cfg["save_device_list"]:
        dl.to_csv("device_list.csv")

if dl is None:
    try:
        dl = pd.read_csv("./device_list.csv")
    except Exception as e:
        sys.exit(f"could not locate device list {e}")

print("bp")

# select the used device
if cfg["ask_to_select"] or cfg["selected_host"] == "":
    print(dl)
    print("Select witch device you want(on index)")
    selected = ""
    while selected == "":
        num_selected = input()

        if num_selected.isdigit():
            num_selected = int(num_selected)
        else:
            print("enter a valid index is integer:")
            continue

        if num_selected > len(dl)-1 or num_selected < 0:
            print("enter a valid index in range:")
            continue

        selected = dl.loc[dl['Unnamed: 0'] == num_selected, ["hostname"]].values[0][0]
        selected_ip = dl.loc[dl['hostname'] == selected, ["ip"]].values[0][0]
        selected_mac = dl.loc[dl['hostname'] == selected, ["mac"]].values[0][0]

        # set selected in cfg file
        cfg["selected_host"] = selected
        cfg["selected_ip"] = selected_ip
        cfg["selected_mac"] = selected_mac
        with open("./config.json", "w")as my_cfg:
            json.dump(cfg, my_cfg, indent=2)

# Test connection to device
my_device = rc.Device(cfg["selected_ip"], cfg["selected_mac"], None, True)
try:
    my_device.device_data()
except Exception as e:
    warnings.warn(f"could not connect to device: {e}")

# import all clock timings
a_h = int(cfg["alarm_time"].split(":")[0])
a_m = int(cfg["alarm_time"].split(":")[1])
yt_list = cfg["youtube_ids"]
while True:
    if a_h == datetime.now().hour and a_m == datetime.now().minute:
        # generate the string to play at set time
        selected_video = yt_list[randint(0, len(yt_list) - 1)]
        my_device.launch_home()
        time.sleep(5)
        my_device.launch_youtube(selected_video)

    time.sleep(60)




