#---------------------------------------------------------

import machine, onewire, ds18x20, time 
import network
import socket
import sys

#---------------------------------------------------------

ds_pin = machine.Pin(22)
ADDRESS = ('IP', 'PORT')

#---------------------------------------------------------

def write_to_syslog(msg):
    print(msg)
    with open('syslog.txt', 'a') as file:
        file.write("\n" + msg)


class Client:
    def __init__(self):
        write_to_syslog("Initializing client")
        self.ssid = 'SSID HERE!'
        self.password = 'PASSWORD HERE!'
        self.server_ip = ''
        self.wlan_status = None 
        self.wlan = network.WLAN(network.STA_IF)
        self.connect_attempt_pause = 5

    def connect_wlan(self):
        write_to_syslog("Connecting to network: " + self.ssid)
        self.wlan.active(True)
        self.wlan.connect(self.ssid, self.password)
        while not self.wlan.isconnected() and self.wlan.status() >= 0:
            write_to_syslog("Waiting to connect...")
            time.sleep(1)
        write_to_syslog(' '.join(self.wlan.ifconfig()))
        return
        

class TempSensor:
    def __init__(self, ds_pin):
        write_to_syslog("Initializing TempSensor")
        self.ds_pin = ds_pin 
        self.ds_sensor = ds18x20.DS18X20(onewire.OneWire(self.ds_pin))
        self.ds_address = self.ds_sensor.scan()[0]
        self.temp_c = None 
        self.temp_f = None 

    def read_sensor(self):
        self.ds_sensor.convert_temp()
        self.temp_c = round(self.ds_sensor.read_temp(self.ds_address), 1)
        self.temp_f = round(self.temp_c * (9/5) + 32, 1)
    
    def report(self):
        self.read_sensor()
        return self.temp_c, self.temp_f



#---------------------------------------------------------
c = Client()
c.connect_wlan()
temp = TempSensor(ds_pin)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
write_to_syslog("Starting loop...")
while True:
    temp.report()
    payload = str(temp.temp_c)
    write_to_syslog("Sending payload: " + payload)
    sock.sendto(payload.encode(), ADDRESS)
    time.sleep(5)

#---------------------------------------------------------
