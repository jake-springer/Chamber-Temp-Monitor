# Chamber-Temp-Monitor
Network monitor that reports the temperature of my 3D printer enclosure via WLAN.

## Requirements:
- Raspberry Pi Pico W (MicroPython v1.20.0)
- DS18B20 Temperature Sensor
  - [I use this one](https://www.amazon.com/gp/product/B09NVWNGLQ/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&psc=1)

## Overview 
CTM uses the Python sockets module to create a UDP connection on the local network. Afterwards, the Pico W sends the reported temperature over the network to the server, which stores the data in a json file with the time the data was recieved. This project was made to help me troubleshoot why my ABS prints are warping so badly, but it's nifty to have around anyways. 

## Setup
Nothing too crazy, just install the `client.py` script onto the Pico, update the WLAN credentials, and run the `server.py` script on whatever system is meant to log the temperature. 
On start, the `server.py` script asks for a name for the project. This is to quickly reference whatever it was you were monitoring at the time. It'll be written as a `.json` file in the local directory.
