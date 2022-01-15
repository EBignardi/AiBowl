
import serial
import serial.tools.list_ports
import numpy as np
import urllib.request
import base64
from datetime import datetime
import geocoder
import time
from requests import post, get
class Bridge():
    def setupSerial(self):
        
        self.ser = None
        print("list of available ports: ")

        ports = serial.tools.list_ports.comports()
        self.portname=None
        for port in ports:
            print (port.device)
            print (port.description)
            if 'Arduino Uno (COM3)' in port.description:
                print(port.device)
                self.portname = port.device
        print ("connecting to " + self.portname)

        try:
            if self.portname is not None:
                self.ser = serial.Serial(self.portname, 9600, timeout=0)
        except:
            self.ser = None

        # self.ser.open()

        # internal input buffer from serial
        self.inbuffer = []

    def setup(self):
        self.setupSerial()

    def loop(self):
        while (True):
            if not self.ser is None:
                if self.ser.in_waiting>0:
                    # data available from the serial port
                    lastchar=self.ser.read(1)
                    if lastchar==b'\xfe': #EOL
                        self.useData()
                        self.inbuffer =[]
                    else:
                        # append
                        self.inbuffer.append (lastchar)

    def useData(self):
        # I have received a line from the serial port. I can use it
        if len(self.inbuffer)<2:   # at least header, size, footer
            return False
        # split parts
        if self.inbuffer[0] != b'\xff':
            return False
        dim=self.inbuffer[1]
        if dim==b'\x13':
            i=3
            lat1=''
            while(i<6):
                val=self.inbuffer[i]
                val=int.from_bytes(val, byteorder='big')
                lat1=lat1+str(val)
                i=i+1
            #lat1=lat1.decode("utf-8")
            lat2=''
            i=6
            while(i<12):
                val=self.inbuffer[i]
                val=int.from_bytes(val, byteorder='big')
                lat2=lat2+str(val)
                i=i+1
            lat=lat1+'.'+lat2
            i=12
            lng1=''
            while(i<15):
                val=self.inbuffer[i]
                val=int.from_bytes(val, byteorder='big')
                lng1=lng1+str(val)
                i=i+1
            i=15
            #lng1=lng1.decode('utf-8')
            lng2=''
            while(i<21):
                val=self.inbuffer[i]
                val=int.from_bytes(val, byteorder='big')
                lng2=lng2+str(val)
                i=i+1
            lng=lng1+'.'+lng2
            lat=float(lat)
            lng=float(lng)
            print( lat)
            print(lng)
            r=post('http://127.0.0.1:5000/api/v1/animale/1377a80b-d0d4-4871-818d-005526c5df01', json={'tipo':'dog', 'long':lng, 'lat':lat})



if __name__ == '__main__':
    br=Bridge()
    br.setup()
    br.loop()