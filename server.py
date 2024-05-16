#!/usr/bin/python

#--------------------------------------------------------------

import socket
from datetime import datetime 
import json 
from time import sleep
import sys 
import os

#--------------------------------------------------------------

HOST = ''
PORT = 0

#--------------------------------------------------------------

def create_data_file(fname):
    fname = os.path.join(os.path.expanduser("~/"), fname)
    with open(fname, 'w') as file:
        file.write(json.dumps({"reports":[]}, indent=4))
    return fname


def get_now():
    now = datetime.now()
    date = now.strftime("%m-%d-%y")
    time = now.strftime("%H:%M:%S")
    return date, time 

def create_report(temp):
    date, time = get_now()
    report = {
        "date":date,
        "time":time,
        "temp":temp
    }
    return report

def log(report):
    print("Date: " + report['date'])
    print("Time: " + report['time'])
    temp_c = float(report['temp'])
    temp_f = temp_c * (9/5) +32
    print('temperature (ºC):', "{:.2f}".format(temp_c))
    print('temperature (ºF):', "{:.2f}".format(temp_f))


    print("")
    print()

    with open(data_file, 'r') as df:
        data = json.load(df) 
    data['reports'].append(report)
    with open(data_file, 'w') as df:
        df.write(json.dumps(data, indent=4))

#--------------------------------------------------------------

fname = input("[!] Data file name: ")
data_file = create_data_file(fname)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((HOST, PORT))
print("Listening...")
while True:
    data, address = sock.recvfrom(1024)
    temp_c = data.decode()
    new_report = create_report(temp_c)
    log(new_report)

