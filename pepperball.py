#!/usr/bin/python

from __future__ import absolute_import, print_function

from optparse import OptionParser, make_option
import os
import sys
import uuid
import time
import bluetooth
from bluetooth import *

#
#create a bluetooth device to emulate a HID keyboard, 
# advertize a SDP record using our bluez profile class
#
class BTKbDevice():
    #change these constants 
    MY_ADDRESS="B8:27:EB:29:90:12"
    MY_DEV_NAME="PepperBall"


    def __init__(self):

        print("Setting up BT device")

        self.init_bt_device()
        # self.init_bluez_profile()

    #configure the bluetooth hardware device
    def init_bt_device(self):


        print("Configuring for name "+BTKbDevice.MY_DEV_NAME)

        #set the device class to a keybord and set the name
        os.system("hciconfig hcio class 0x002540")
        os.system("hciconfig hcio name " + BTKbDevice.MY_DEV_NAME)

        #make the device discoverable
        os.system("hciconfig hcio piscan")


    #set up a bluez profile to advertise device capabilities from a loaded service record
    # def init_bluez_profile(self):

    #     print("Configuring Bluez Profile")

    #     #setup profile options
    #     service_record=self.read_sdp_service_record()

    #     opts = {
    #         "ServiceRecord":service_record,
    #         "Role":"server",
    #         "RequireAuthentication":False,
    #         "RequireAuthorization":False
    #     }


    #listen for incoming client connections
    #ideally this would be handled by the Bluez 5 profile 
    #but that didn't seem to work
    def listen(self):

        print("Waiting for connections")
        self.scontrol=BluetoothSocket(L2CAP)
        self.sinterrupt=BluetoothSocket(L2CAP)

        #bind these sockets to a port - port zero to select next available    
        self.scontrol.bind(self.MY_ADDRESS)
        self.sinterrupt.bind(self.MY_ADDRESS)

        #Start listening on the server sockets 
        self.scontrol.listen(1) # Limit of 1 connection
        self.sinterrupt.listen(1)

        self.ccontrol,cinfo = self.scontrol.accept()
        print ("Got a connection on the control channel from " + cinfo[0])

        self.cinterrupt, cinfo = self.sinterrupt.accept()
        print ("Got a connection on the interrupt channel from " + cinfo[0])


    #send a string to the bluetooth host machine
    def send_string(self,message):

     #    print("Sending "+message)
         self.cinterrupt.send(message)



#define a dbus service that emulates a bluetooth keyboard
#this will enable different clients to connect to and use 
#the service
# class  BTKbService(dbus.service.Object):

#     def __init__(self):

#         print("Setting up service")

#         #create and setup our device
#         self.device= BTKbDevice();

#         #start listening for connections
#         self.device.listen();

#     def send_keys(self,modifier_byte,keys):

#         cmd_str=""
#         cmd_str+=chr(0xA1)
#         cmd_str+=chr(0x01)
#         cmd_str+=chr(modifier_byte)
#         cmd_str+=chr(0x00)

#         count=0
#         for key_code in keys:
#             if(count<6):
#                 cmd_str+=chr(key_code)
#             count+=1

#         self.device.send_string(cmd_str);   


#main routine
if __name__ == "__main__":
    if not os.geteuid() == 0:
       sys.exit("Only root can run this script")

    device = BTKbDevice()
    device.listen()
    