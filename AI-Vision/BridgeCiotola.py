import serial
import serial.tools.list_ports
import numpy as np
import urllib.request
import mysql.connector
from datetime import datetime
import time
from requests import post, get
import base64
import struct
import paho.mqtt.client as mqtt
import cv2
import matplotlib
from torch.utils.data import DataLoader
import random
import matplotlib.pyplot as plt
import utils
from PIL import Image
import geocoder





def most_frequent(List):
    return max(set(List), key = List.count)





class Bridge():
    def neuralnw(self):
        categories = {0: 'cane', 1: "cavallo", 2: "gallina", 3: "gatto", 4: "mucca", 5: "pecora", 6: "scoiattolo"}

        # print example
        # utils.read_show_image("/home/erosb/Desktop/raw-img/cane/OIP-0d7hpjwVocPjQXWE67RdKwHaFj.jpeg")

        # prepare data for training
        #print("LOADING DATASET...")
        #x_train, y_train, x_test, y_test, img_size = utils.create_data()

        #print("Train image: " + str(len(x_train)), "Test image:" + str(len(x_test)))

        # check shape of the train and test
        #print(x_train.shape) # (n, H, W, C)
        #print(y_train.shape) # (n)

        # check label for an image
        # print(y_train[10])
        # print(x_train[10])
        # img = x_train[10]
        # cv2.imshow('label: ' + str(categories[y_train[10]]), img)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

        # train Convolution Neural Network
        #print("TRAINING NETWORK...")
        net = utils.CNN_Network()

        # net.summary()

        # open webcam
        i = 0
        cv2.namedWindow("preview")
        vc = cv2.VideoCapture(0)

        if vc.isOpened(): # try to get the first frame
            rval, frame = vc.read()
        else:
            rval = False
        lista=[]
        cont=10
        while cont>0:
            cont=cont-1
            cv2.imshow("preview", frame)
            rval, frame = vc.read()
            key = cv2.waitKey(1)

            print("Save image and predict the class of the image...")
            #print(frame.shape)
            frame = cv2.resize(frame, (100, 100), interpolation=cv2.INTER_AREA)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            #print(gray.shape)
            cv2.imwrite("Frame " + str(i) + ".jpg", gray)
            i += 1
            utils.search_animal(net, gray)
            lista.append(str(utils.search_animal(net, gray)))
            time.sleep(1)
            #print("Classe predetta: " + str(utils.search_animal(net, gray)))
            
        vc.release()
        cv2.destroyWindow("preview")
        classe=most_frequent(lista)
        return str(classe)



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
        # infinite loop for serial managing
        #
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
            """
            codice per attivare il motorino: attualmente in attesa
            r=get('http://127.0.0.1:5000/api/v1/info/1377a80b-d0d4-4871-818d-005526c5df01')
            r=r.json()
            qtcibo=r['quantità_cibo']
            string=b''
            string+=struct.pack('!B',qtcibo)
            head=b''
            head+=struct.pack('!B',255)
            dim=b''
            dim+=struct.pack('!B',1)
            tail=b''
            tail+=struct.pack('!B',254)
            
            self.ser.write(head)
            self.ser.write(dim)
            self.ser.write(string)
            self.ser.write(tail)
            time.sleep(10)
            """
    def useData(self):
        # I have received a line from the serial port. I can use it
        if len(self.inbuffer)<2:   # at least header, size, footer
            return False
        # split parts
        if self.inbuffer[0] != b'\xff':
            return False

        id=self.inbuffer[1]
        if id==b'\x01':
            classe=self.neuralnw()
            print(classe)
            g = geocoder.ip('me')
            long=g.latlng[1]
            lat=g.latlng[0]
            url='http://127.0.0.1:5000/api/v1/posizione/'+str(long)+'/'+str(lat)+'/'+classe
            r=get(url)
            if r.status_code==200:
                r=r.json()
                uuid=r['animale']
                url1='http://127.0.0.1:5000/api/v1/info/'+uuid
                r=get(url1)
                r=r.json()
                qtcibo=int(r['quantità_cibo'])
                print(qtcibo)
                string=b''
                string+=struct.pack('!B',qtcibo)
                head=b''
                head+=struct.pack('!B',255)
                id=b''
                id+=struct.pack('!B',2)
                tail=b''
                tail+=struct.pack('!B',254)
                self.ser.write(head)
                self.ser.write(id)
                self.ser.write(string)
                self.ser.write(tail)
                url='http://127.0.0.1:5000/api/v1/mangiato/'+uuid
                r=post(url, json={'long':long,'lat':lat})
            else:
                string=b''
                string+=struct.pack('!B',0)
                head=b''
                head+=struct.pack('!B',255)
                id=b''
                id+=struct.pack('!B',3)
                tail=b''
                tail+=struct.pack('!B',254)
                self.ser.write(head)
                self.ser.write(id)
                self.ser.write(string)
                self.ser.write(tail)
                
            

    
if __name__ == '__main__':
    br=Bridge()
    br.setup()
    br.loop()

