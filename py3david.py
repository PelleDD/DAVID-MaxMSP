#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on WE 8/02/2022

Master thesis - 2 MA Biomedical Science: Neuroscience
University of Antwerp - Center for Music in the Brain / Aarhus University
Pelle De Deckere

based on pyDavid.py by leehooni (github.com/neuro-team-femto/david)

@author: leehooni
"""

import threading
import time

# Using the new pythonosc library compatible with python3 instead of the old pyosc which is no longer supported for python3
from pythonosc import udp_client
from pythonosc import dispatcher
from pythonosc import osc_server


'''
------ READ ME FIRST PLEASE :) -------

# IF YOU WANT TO USE THE BUNDELED MESSAGES OR BUNDLES SUPPORTED BY THE OSC STANDARD YOU CAN DO IT WITH THE CREATE BUNDLE FUNCTION,
WE FOUND THEM NOT TO WORK PROPERLY IN OUR CASE SO WE STICKED WITH A GROUP OF SEQUENTIAL MESSAGES BUT YOUR MILEAGE MIGHT VARY

DAVID WORKED WITH BUNDLES BUT NOT WHEN THE MESSAGE SENT WAS AN ARRAY, CHECK pythonosc LIBRARY
https://pypi.org/project/python-osc/

DAVID MAXMSP DOES NOT HAVE THESE ADDRESSES ANYMORE /RECSYNC /PITCH /RECSYNC-STORE 

HOW TO USE (also possible in a pyhton code component in the PsychoPy Builder 2021.2.3)
- Start David in MaxMsp
- Import py3david
- Connect with David example:
  david_bridge = py3david.py3david()
  david_bridge.connect()
  david_bridge.MicRecord(...)
'''


# py3DAVID
class py3david():

    # Constructor function, it takes the default localhost for the server, and the standard DAVID port 5678
    def __init__(self, serveradd = "127.0.0.1",  port = 5678):
        self.serveradd = serveradd
        self.port = port        

    def connect(self):
        self.client = udp_client.SimpleUDPClient(self.serveradd, self.port)
        print('Testing OSC connection...')
        time.sleep(2)
        oscmsg = 'py3DAVID is connected, look if the same message shows up in the david console'
        self.client.send_message("/print", oscmsg)
        print(oscmsg)

    def start_server(self):
        
        dispatcher = dispatcher.Dispatcher()
        dispatcher.map("/print", print)
        self.server = osc_server.ThreadingOSCUDPServer((self.serveradd, self.port), dispatcher)
        self.servert = threading.Thread(target=self.server.serve_forever)
        servert = self.servert
        servert.daemon = True
        servert.start()
        
    def disconnect(self):
        self.server.shutdown()

    # test the connection by sending a message, the message should appear on DAVID console
    def ping(self):
        oscmsg = 'ping'
        self.client.send_message("/ping", oscmsg)

# MICROPHONE

    def MicOnOff(self,value):
        if value is 0 or value is 1:
            self.client.send_message("/miconoff", value)
        else:
            raise TypeError("MicOnOff : 0 (off) or 1 (on) expected")

    def MicPreset(self,value):
        self.client.send_message("/miconoff", 1)
        self.client.send_message("/preset", value)

    def MicRamp(self,preset=1, hold_time=0, ramp_time=0):
        self.client.send_message("/miconoff", 1)
        self.client.send_message("/preset", preset)
        self.client.send_message("/automation", [1,hold_time,ramp_time])

    def MicPitchShift(self, sfrecname, pitchshift=0, hold_time=0, ramp_time=0, marker_name = [], sfolderrecname = [] ):
        if marker_name != []:
            self.client.send_message("/recsync", marker_name)
        self.client.send_message("/miconoff", 1)       
        self.client.send_message("/pitch", pitchshift)       
        self.client.send_message("/micrecname", sfrecname)  
        self.client.send_message("/automation", [1,hold_time,ramp_time])
        if sfolderrecname != []:   
            self.client.send_message("/sfolderrecname", sfolderrecname)       
        self.client.send_message("/sfrec", 1)
       
    def StoreMarkers(self, marker_filename = []):
        self.client.send_message("/recsync-store", marker_filename)

    def MicRecord(self, sfrecname, preset=1, hold_time=0, ramp_time=0, sfolderrecname = [] ):
       
        self.client.send_message("/miconoff", 1)  
        self.client.send_message("/preset", preset)  
        self.client.send_message("/micrecname", sfrecname)  
        self.client.send_message("/automation", [1,hold_time,ramp_time])  
        if sfolderrecname != []:
            self.client.send_message("/sfolderrecname",sfolderrecname )

        self.client.send_message("/sfrec",1 )
    
    def StopMicRecord(self):

        self.client.send_message("/miconoff",0 )
        self.client.send_message("/preset",1 )
        self.client.send_message("/automation",[0,0,0] )
        self.client.send_message("/stoprecord", [0] )

# SOUND FILE

    def SfPlay(self,sfplayname = [] ):
        
        self.client.send_message("/miconoff",0 )
        self.client.send_message("/sfplayname",sfplayname )
        self.client.send_message("/sfplay",1 )

    def SfPreset(self,sfplayname,value):

        self.client.send_message("/miconoff",0 )
        self.client.send_message("/preset",value )
        self.client.send_message("/sfplayname",sfplayname )
        self.client.send_message("/sfplay",1 )

    def SfRamp(self,sfplayname,preset=1, hold_time=0, ramp_time=0):

        self.client.send_message("/miconoff",0 )
        self.client.send_message("/preset",preset )
        self.client.send_message("/automation",[1,hold_time,ramp_time] )
        self.client.send_message("/sfplayname",sfplayname )
        self.client.send_message("/sfplay",1 )

    def SfRecord(self,sfplayname, preset=1, hold_time=0, ramp_time=0, sfolderrecname = [] ):
        
        self.client.send_message("/miconoff",0 )
        self.client.send_message("/sfrec",0 )
        self.client.send_message("/sfplayname",sfplayname )
        self.client.send_message("/preset",preset )
        self.client.send_message("/automation",[1,hold_time,ramp_time] )
        #self.client.send_message("/record", 1 )
        if sfolderrecname != []:
            self.client.send_message("/sfolderrecname",sfolderrecname )
            self.client.send_message("/sfrec",1 )
        else:
            self.client.send_message("/sfrec",1 )

    def SfPitchShiftRecord(self,sfplayname,pitchshift=0, hold_time=0, ramp_time=0, marker_name = [], sfolderrecname = [] ):

        if marker_name != []:
            self.client.send_message("/recsync",marker_name )

        self.client.send_message("/miconoff",0 )
        self.client.send_message("/sfrec",0 )
        self.client.send_message("/pitch",pitchshift )
        self.client.send_message("/automation",[1,hold_time,ramp_time] )
        self.client.send_message("/sfplayname",sfplayname )
        #self.client.send_message("/record",1 )
        if sfolderrecname != []:
           self.client.send_message("/sfolderrecname",sfolderrecname )
           self.client.send_message("/sfrec",1 )
        else:
           self.client.send_message("/sfrec",1 )

    def SfRecIter(self,sffoldername, sfolderrecname, preset=1, hold_time=0, ramp_time=0):
        
        self.client.send_message("/miconoff",0 )
        self.client.send_message("/sffoldername",sffoldername )
        self.client.send_message("/automation",[1,hold_time,ramp_time] )
        self.client.send_message("/preset",preset )
        self.client.send_message("/sfolderrecname",sfolderrecname )
        self.client.send_message("/sfrec",1 )

        

