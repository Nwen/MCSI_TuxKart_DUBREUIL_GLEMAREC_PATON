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

import pygame as pg
import pygame.midi

from playsound import playsound

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


#l'enfer commence ici
def print_device_info():
    pygame.midi.init()
    _print_device_info()
    pygame.midi.quit()

def _print_device_info():
    for i in range(pygame.midi.get_count()):
        r = pygame.midi.get_device_info(i)
        (interf, name, input, output, opened) = r

        in_out = ""
        if input:
            in_out = "(input)"
        if output:
            in_out = "(output)"

        print(
            "%2i: interface :%s:, name :%s:, opened :%s:  %s"
            % (i, interf, name, opened, in_out)
        )

def input_main(device_id=None):
    pg.init()
    pg.fastevent.init()
    event_get = pg.fastevent.get
    event_post = pg.fastevent.post

    pygame.midi.init()

    _print_device_info()

    if device_id is None:
        input_id = pygame.midi.get_default_input_id()
    else:
        input_id = device_id

    print("using input_id :%s:" % input_id)
    i = pygame.midi.Input(input_id)

    pg.display.set_mode((1, 1))

    going = True
    while going:
        events = event_get()
        for e in events:
            if e.type in [pg.QUIT]:
                going = False
                print("DED")
                exit()
            if e.type in [pygame.midi.MIDIIN]:
                print(e)
                if(e.status == 144 and e.data1 == 55): #Press Channel C mode C1 single pied   
                    data = b'P_FIRE'
                    client_socket.sendto(data, address)
                    playsound('sound/clap.wav', False)
                elif(e.status == 128 and e.data1 == 55): #Release 
                    data = b'R_FIRE'
                    client_socket.sendto(data, address)
                elif(e.status == 144 and e.data1 == 36): #Press Channel A mode C1 double pied 1
                    data = b'P_LEFT'
                    client_socket.sendto(data, address)
                    sleep(0.3)
                    data = b'R_LEFT'
                    client_socket.sendto(data, address)
                # elif(e.status == 128 and e.data1 == 36): #Release Channel A mode C1 double pied 1
                #     data = b'R_LEFT'
                #     client_socket.sendto(data, address)
                elif(e.status == 144 and e.data1 == 43): #Press Channel A mode C1 double pied 2   
                    data = b'P_RIGHT'
                    client_socket.sendto(data, address)
                    sleep(0.3)
                    data = b'R_RIGHT'
                    client_socket.sendto(data, address)
                # elif(e.status == 128 and e.data1 == 43): #Release Channel A mode C1 double pied 2   
                #     data = b'R_RIGHT'
                #     client_socket.sendto(data, address)
                elif(e.status == 144 and e.data1 == 38): #Press Channel B mode C1 double pied 1
                    data = b'P_NITRO'
                    client_socket.sendto(data, address)
                    playsound('sound/snare.wav', False)
                elif(e.status == 128 and e.data1 == 38): #Relesae Channel B mode C1 double pied 1
                    data = b'R_NITRO'
                    client_socket.sendto(data, address)
                elif(e.status == 128 and e.data1 == 45): #rELEASE Channel B mode C1 double pied 2
                    data = b'R_SKIDDING'
                    client_socket.sendto(data, address)
                elif(e.status == 144 and e.data1 == 45): #Press Channel B mode C1 double pied 2
                    data = b'P_SKIDDING'
                    client_socket.sendto(data, address)
                    playsound('sound/kick.wav', False)
                elif(e.status == 144 and e.data1 == 53): #Press Channel B mode C1 double pied 2
                    data = b'P_RESCUE'
                    client_socket.sendto(data, address)
                    playsound('sound/error.mp3', False)
                    data = b'R_RESCUE'
                    client_socket.sendto(data, address)

                
        if i.poll():
            midi_events = i.read(10)
            # convert them into pygame events.
            midi_evs = pygame.midi.midis2events(midi_events, i.device_id)

            for m_e in midi_evs:
                event_post(m_e)

    del i
    pygame.midi.quit()

osc = OSCThreadServer(default_handler=dump)  # See sources for all the arguments

# You can also use an \*nix socket path here
# sock = osc.listen(address='0.0.0.0', port=8000, default=True)

input_main(2)

sleep(1000)
osc.stop()  # Stop the default socket