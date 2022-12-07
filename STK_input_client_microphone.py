#!/usr/bin/env python3
#Michael ORTEGA - 09 jan 2018

###############################################################################
## Global libs
import socket
import sys
import select
from time import sleep
import time
from oscpy.server import OSCThreadServer

import os

address = ('localhost', 6006)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

t1 = time.time()
t2 = time.time()


def dump(address, *values):
    print(u'{}: {}'.format(
        address.decode('utf8'),
        ', '.join(
            '{}'.format(
                v.decode(options.encoding or 'utf8')
                if isinstance(v, bytes)
                else v
            )
            for v in values if values
        )
    ))

import pyaudio
import wave
import audioop

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "output.wav"

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

#for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):


osc = OSCThreadServer(default_handler=dump)  # See sources for all the arguments

# You can also use an \*nix socket path here
#sock = osc.listen(address='0.0.0.0', port=8000, default=True)
going = False
while True:
    data = stream.read(CHUNK)
    rms = audioop.rms(data, 2)    # here's where you calculate the volume
    
    if(rms > 3000):
        data = b'P_ACCELERATE'
        client_socket.sendto(data, address)
        print("GO!")
        going = True
    elif going == True:
        data = b'R_ACCELERATE'
        client_socket.sendto(data, address)
        going = False
sleep(1000)
osc.stop()  # Stop the default socket