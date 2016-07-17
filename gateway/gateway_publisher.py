#!/usr/bin/python
#Author : Arun Kumar <@ioarun>

from gattlib import GATTRequester
from datetime import datetime
import time
import csv
from gattlib import DiscoveryService
import csv
import httplib
import urllib
import Tkinter
import time
import paho.mqtt.client as mqtt
import json
import uuid
import base64
import random, string
import math
import pygame
import pygame.image
import pygame.camera
from pygame.locals import *
import base64
import socket
import os

os.system("sudo /etc/init.d/bluetooth restart")
s = socket.socket()
host = socket.gethostname()
port = 12345
s.bind(("192.168.1.103", port)) #

pygame.init()
pygame.camera.init()

macAddress="20474721a2eb"

#Set the variables for connecting to the iot service
broker = ""
topic = "iot-2/evt/status/fmt/json"
username = "use-token-auth"
password = "U1jT1K9EAVL5qhvt3y"
organization = "d8uu23"
deviceType = "healthgateway"

class simpleapp_tk(Tkinter.Tk):
    
    def __init__(self,parent):
        Tkinter.Tk.__init__(self,parent)
        self.parent = parent
        self.initialize()

    def initialize(self):
        self.grid()
	    self.labelVariable1 = Tkinter.StringVar()
        label1 = Tkinter.Label(self,textvariable=self.labelVariable1,
                              anchor="w",fg="white",bg="blue")
        label1.grid(column=0,row=0,columnspan=1,sticky='EW')
        self.labelVariable1.set(u"Enter Name")
        self.entryVariable1 = Tkinter.StringVar()
        self.entry1 = Tkinter.Entry(self,textvariable=self.entryVariable1)
        self.entry1.grid(column=1,row=0,sticky='EW')
        self.entry1.bind("<Return>", self.OnPressEnter)
        self.entryVariable1.set(u"Enter name here.")

        self.labelVariable2 = Tkinter.StringVar()
        label2 = Tkinter.Label(self,textvariable=self.labelVariable2,
                              anchor="w",fg="white",bg="blue")
        label2.grid(column=0,row=1,columnspan=1,sticky='EW')
        self.labelVariable2.set(u"Enter Age")
        self.entryVariable2 = Tkinter.StringVar()
        self.entry2 = Tkinter.Entry(self,textvariable=self.entryVariable2)
        self.entry2.grid(column=1,row=1,sticky='EW')
        self.entry2.bind("<Return>", self.OnPressEnter)
        self.entryVariable2.set(u"Enter age here.")

        self.labelVariable3 = Tkinter.StringVar()
        label3 = Tkinter.Label(self,textvariable=self.labelVariable3,
                              anchor="w",fg="white",bg="blue")
        label3.grid(column=0,row=2,columnspan=1,sticky='EW')
        self.labelVariable3.set(u"Enter Contact")
        self.entryVariable3 = Tkinter.StringVar()
        self.entry3 = Tkinter.Entry(self,textvariable=self.entryVariable3)
        self.entry3.grid(column=1,row=2,sticky='EW')
        self.entry3.bind("<Return>", self.OnPressEnter)
        self.entryVariable3.set(u"Enter Contact here.")

        self.labelVariable4 = Tkinter.StringVar()
        label4 = Tkinter.Label(self,textvariable=self.labelVariable4,
                              anchor="w",fg="white",bg="blue")
        label4.grid(column=0,row=3,columnspan=1,sticky='EW')
        self.labelVariable4.set(u"Enter Location")
        self.entryVariable4 = Tkinter.StringVar()
        self.entry4 = Tkinter.Entry(self,textvariable=self.entryVariable4)
        self.entry4.grid(column=1,row=3,sticky='EW')
        self.entry4.bind("<Return>", self.OnPressEnter)
        self.entryVariable4.set(u"Enter Location here.")

        self.labelVariable5 = Tkinter.StringVar()
        label5 = Tkinter.Label(self,textvariable=self.labelVariable5,
                              anchor="w",fg="white",bg="blue")
        label5.grid(column=0,row=9,columnspan=2,sticky='EW')
	
	    buttonGSR = Tkinter.Button(self,text=u"GSR",
                                command=self.OnGSRButtonClick)
        buttonGSR.grid(column=0,row=5)
	
	    buttonBP = Tkinter.Button(self,text=u"BP/HR",
                                command=self.OnBPButtonClick)
        buttonBP.grid(column=1,row=5)
	    buttonECG = Tkinter.Button(self,text=u"ECG",
                                command=self.OnECGButtonClick)
        buttonECG.grid(column=3,row=5)
	
	
        button = Tkinter.Button(self,text=u"Submit",
                                command=self.OnButtonClick)
        button.grid(column=1,row=8)

        self.grid_columnconfigure(0,weight=1)
        self.resizable(True,False)
        self.update()
        self.geometry(self.geometry())


    def OnBPButtonClick(self):
	
	   f = open("bp.csv", 'wt')
	   writer = csv.writer(f)
	   writer.writerow( ('sys', 'dia','pulse') )
	   req = GATTRequester("98:4F:EE:0F:59:D6")
	   req.write_by_handle(0x000e,str(bytearray([02])))
	   tt = req.read_by_handle(0x0010)[0]
	   pp = []
	   for c in tt:
		  pp.append(ord(c))
	   print pp
	   if(pp[1] == 2):
		
		while(1):
			try:
				tt = req.read_by_handle(0x0010)[0]
				pp = []
				for c in tt:
					pp.append(ord(c))
				if(pp[0] == 3):
					break
			except Exception,e:
				print e
		
		try:
			name = req.read_by_uuid("2A40")[0]
			#steps = (req.read_by_handle(0x0009)[0])
			print type(name)
		
			value = []
			for c in name:
				value.append((c))
			print value
			print "sys :"+value[1]+value[2]+value[3]+"\n"
			print "dia :"+value[6]+value[7]+value[8]+"\n"
			print "sys :"+value[11]+value[12]+value[13]+"\n"
			writer.writerow((value[1]+value[2]+value[3],value[6]+value[7]+value[8],value[11]+value[12]+value[13]))
		
				
		except Exception,e:
			#name = False
			print e
	
	
	self.labelVariable5.set("BP/HR Done!" )
	
    
    def OnGSRButtonClick(self):
	
	    req = GATTRequester("98:4F:EE:0F:59:D6")
	    temp = []
	    f = open("gsr.csv", 'a')
	    writer = csv.writer(f)
	    writer.writerow( ('timestamp', 'gsr') )
	    flagTemp = 0;
	    flagBP = 1;
	    flagGSR = 0;
	    req.write_by_handle(0x000e,str(bytearray([01])))
	    tt = req.read_by_handle(0x0010)[0]
        pp = []
	    for c in tt:
		  pp.append(ord(c))
	    print pp
	    if(pp[0] == 1):
	       counter = 0
		while(counter < 24):
			try:
				name = req.read_by_uuid("2A40")[0]
				#steps = (req.read_by_handle(0x0009)[0])
				#print type(name)
		
				value = []
				for c in name:
					value.append(ord(c))
				temp = value	
				print temp
				print datetime.now()
	
				try:
					print "*********************************************"
					for x in temp:
    						print "writing......"
    						writer.writerow((datetime.now(),(x)))
						print "written......"
        				
				finally:
					print "finally"
				counter += 1
    				#print counter
		
		
				
			except Exception,e:
				#name = False
				print e

		req.disconnect()

	
	self.labelVariable5.set("GSR Done!" )

    def OnECGButtonClick(self):
	
	f = open("ecg.csv", 'a')
	writer = csv.writer(f)
	writer.writerow( ('timestamp', 'value') )
	s.listen(5) # Now wait for client connection.
	c, addr = s.accept()

	# Establish connection with client.
	print 'Got connection from', addr
	c.send("send")
	while True:
		a = c.recv(4)
		print a
		writer.writerow((datetime.now(),(a)))
		if(a == "c"):
			c.close()
			s.close()
			break
			
	
	self.labelVariable5.set("ECG/Temp Done!" )
##########################################################################################3
    def OnButtonClick(self):
        #self.labelVariable1.set( self.entryVariable1.get())
        #self.entry1.focus_set()
        #self.entry1.selection_range(0, Tkinter.END)

        g = []
        e = []
        p = []
        name = self.entryVariable1.get()
        age = self.entryVariable2.get()
        contact = self.entryVariable3.get()
        location = self.entryVariable4.get()

        #cam = pygame.camera.Camera("/dev/video0",(640,480))
        #cam = pygame.camera.Camera(pygame.camera.list_cameras()[0])
        #camlist = pygame.camera.list_camera()
        #if camlist:
        #cam = pygame.camera.Camera(camlist[0],(640,480))
	    print "clicking profile"
	    self.labelVariable5.set("clicking profile" )
	    time.sleep(5)
	
        cam.start()
        img = cam.get_image()
        im = pygame.image.save(img,name+".jpg")
        pygame.camera.quit()
	
        with open(name+".jpg", "rb") as image_file:
            encoded1 = base64.b64encode(image_file.read())
	    print "clicked"
	
	    self.labelVariable5.set("clicked" )
	    time.sleep(2)
	
	    print "Show symptom"
	
	    self.labelVariable5.set("Show symptom" )
	    time.sleep(4)
	    print "clicking symptoms"
	    self.labelVariable5.set("clicking symptoms" )
		pygame.init()
	    pygame.camera.init()
	    cam = pygame.camera.Camera(pygame.camera.list_cameras()[0])
	    cam.start()
        img = cam.get_image()
        im = pygame.image.save(img,name+"1.jpg")
        pygame.camera.quit()
	
	    with open(name+"1.jpg", "rb") as image_file:
            encoded2 = base64.b64encode(image_file.read())
	    print "clicked"
	    self.labelVariable5.set("clicked" )
        
        def convertImageToBase64():
            with open(name+".jpg", "rb") as image_file:
                encoded = base64.b64encode(image_file.read())
            return encoded
        def randomword(length):
            return ''.join(random.choice(string.lowercase) for i in range(length))
        packet_size=3000
        def publishEncodedImage(encoded):

            end = packet_size
            start = 0
            length = len(encoded)
            picId = randomword(8)
            pos = 0
            no_of_packets = math.ceil(length/packet_size)


            while start <= len(encoded):
                data = {"data": encoded[start:end], "pic_id":picId, "pos": pos, "size": no_of_packets}
                msg = json.JSONEncoder().encode(data)
                mqttc.publish(topic, payload=msg, qos=0, retain=False)
                end += packet_size
                start += packet_size
                pos = pos +1
        
        def HttpPost(route,name,imagestring1,imagestring2):
            params1 = urllib.urlencode({
                'name' : name,
                'photo1' : imagestring1
            })
	    params2 = urllib.urlencode({
                'name' : name,
                'photo1' : imagestring2
            })
            headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
            httpServ = httplib.HTTPConnection("iot-vaidya.mybluemix.net", 80)
            httpServ.connect()
            httpServ.request('POST', '/imagepro',params1,headers)

            response = httpServ.getresponse()
            if response.status == httplib.OK:
                print "Output from server request"
                printText (response.read())
	    httpServ.request('POST', '/imagesyma',params2,headers)
            response = httpServ.getresponse()
            if response.status == httplib.OK:
                print "Output from server request"
                printText (response.read())
            httpServ.close()


        def ReadECGfromCSV(ecg):
            count = 0
            with open('ecg.csv', 'rb') as csvfile:
                ecg = []
                reader = csv.reader(csvfile)
		    reader.next()
		    reader.next()
		    reader.next()
            data = list(reader)
            for row in data:
                if(count <= 1000):
                    msg = json.JSONEncoder().encode({ "x" :row[0],"y" : row[1]})
                    ecg.append({"x" : row[0],"y" : row[1]})
                    count += 1;

            return ecg
        def ReadGSRfromCSV(gsr):
            count = 0
            with open('gsr.csv', 'rb') as csvfile:
                gsr = []
                reader = csv.reader(csvfile)
		    reader.next()
		    reader.next()
		    reader.next()
            data = list(reader)
            for row in data:
                if(count <= 90):
                    msg = json.JSONEncoder().encode({ "x" :row[0],"y" : row[1]})
                    gsr.append({"x" : row[0],"y" : row[1]})
                    count += 1;
            return gsr

	    with open('bp.csv', 'rb') as csvfile:
                reader = csv.reader(csvfile)
                data = list(reader)
		for row in data:
			pulse = row[2]
			sys = row[0]
			dia = row[1]
        ecg = []
        gsr = []
	
        bp = [
                {
                    "sys":sys,
                    "dia":dia
                }
            ]
	
        print ReadECGfromCSV(ecg)
        msg = json.JSONEncoder().encode({"name" : name,"age" : age,"contact" : contact,"location" : location,"temperature" : temp,"bp" : bp,"gsr" : ReadGSRfromCSV(gsr),"ecg" : ReadECGfromCSV(ecg),"pulse" : pulse})
        mqttc.publish(topic, payload=msg, qos=0, retain=False)
        #time.sleep(1)
        #encoded_str = convertImageToBase64()
        #publishEncodedImage(encoded_str)
	    print "Mqtt published"
	    self.labelVariable5.set("Mqtt published!")
	    time.sleep(4)
        HttpPost("iot-vaidya.mybluemix.net",name,encoded1,encoded2)
        self.labelVariable5.set("Report Published Successfully!" )
        print "Report Published"


    def OnPressEnter(self,event):
        self.labelVariable1.set( self.entryVariable1.get()+" (You pressed ENTER)" )
        self.entry1.focus_set()
        self.entry1.selection_range(0, Tkinter.END)

#Creating the client connection
#Set clientID and broker
clientID = "d:" + organization + ":" + deviceType + ":" + macAddress
broker = organization + ".messaging.internetofthings.ibmcloud.com"
mqttc = mqtt.Client(clientID)

#Set authentication values, if connecting to registered service
if username is not "":
        mqttc.username_pw_set(username, password=password)

mqttc.connect(host=broker, port=1883, keepalive=60)


#Publishing to IBM Internet of Things Foundation
mqttc.loop_start()


if __name__ == "__main__":
    app = simpleapp_tk(None)
    app.title('IOT VAIDYA')
    app.mainloop()
	
		

