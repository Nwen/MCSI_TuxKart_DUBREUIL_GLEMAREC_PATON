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
from playsound import playsound
from threading import Thread

import os

import pygame as pg
import pygame.midi

stopped = False

dejavu = ['C5', 'D5', 'Eb5', 'Eb5', 'Eb5', 'D5', 'C5', 'Bb4', 'Bb4', 'C5', 'C5', 'G5', 'F5', 'Eb5', 'D5', 'Eb5', 'Eb5', 'Eb5', 'F5', 'Eb5', 'F5', 'F5', 'G5', 'F5', 'C5', 'D5', 'Eb5', 'Eb5', 'Eb5', 'D5', 'C5', 'Bb4', 'Bb4', 'C5', 'C5', 'G5', 'F5', 'Eb5', 'D5', 'Eb5', 'Eb5', 'Eb5', 'F5', 'Eb5', 'F5', 'F5', 'G5', 'G5', 'F5', 'G5']
miichannel = ['Gb5', 'A5', 'Db6', 'A5', 'Gb5', 'D5', 'D5', 'D5', 'Db5', 'D5', 'Gb5', 'A5', 'Db6', 'A5', 'Gb5', 'Ab5', 'G5', 'Gb5', 'Ab5', 'Db6', 'Gb5', 'Db6', 'Ab5', 'Db6', 'G5', 'Gb5', 'E5', 'C5', 'C5', 'C5', 'C5', 'C5', 'C5', 'Ab4', 'G4', 'Gb4', 'A5', 'Db6', 'A5', 'Gb5', 'E5', 'E5', 'E5', 'E6', 'E6', 'E6', 'B3', 'Gb5', 'A5', 'Db6', 'A5', 'Gb5', 'Db6', 'B5', 'B5', 'G5', 'D5', 'Db5', 'B5', 'G5', 'Db5', 'A5', 'Gb5', 'C5', 'B4', 'F5', 'D5', 'B4', 'Db5', 'Db5', 'Db5', 'Bb5', 'B5', 'Db6', 'D6', 'Gb6', 'A6']
coconut = ['D5', 'Eb5', 'E5', 'D5', 'D5', 'E5', 'F5', 'C6', 'D6', 'C6', 'D6', 'C6', 'Bb5', 'A5', 'G5', 'F5', 'D5', 'Eb5', 'E5', 'D5', 'D5', 'E5', 'F5', 'F5', 'A5', 'F5', 'A5', 'F5', 'D5', 'E5', 'F5', 'D5', 'Eb5', 'E5', 'D5', 'D5', 'E5', 'F5', 'C6', 'D6', 'C6', 'D6', 'C6', 'Bb5', 'A5', 'G5', 'F5', 'C6', 'F6', 'D6', 'C6', 'B5', 'Bb5', 'A5', 'C6', 'Db6', 'D6', 'F6', 'A6', 'F6', 'A6', 'F6', 'D6', 'E6', 'F6', 'Eb5', 'E5', 'F5', 'Eb5', 'Eb5', 'F5', 'Gb5', 'Db6', 'Eb6', 'Db6', 'Eb6', 'Db6', 'B5', 'Bb5', 'Ab5', 'Gb5', 'Eb5', 'E5', 'F5', 'Eb5', 'Eb5', 'F5', 'Gb5', 'Gb5', 'Bb5', 'Gb5', 'Bb5', 'Gb5', 'Eb5', 'F5', 'Gb5']
melody = ['Ab6', 'E6', 'Ab6', 'E6', 'Ab6', 'E6', 'A6', 'Ab6', 'Gb6', 'Ab6', 'E6', 'Ab6', 'E6', 'Ab6', 'E6', 'A6', 'Ab6', 'Gb6', 'E6', 'Db6', 'E6', 'Db6', 'E6', 'Db6', 'E6', 'Eb6', 'E6', 'Gb6', 'A6', 'Gb6', 'A6', 'Gb6', 'A6', 'Gb6', 'B6', 'A6', 'Ab6', 'A6', 'Gb6', 'A6', 'Gb6', 'A6', 'Gb6', 'B6', 'A6', 'Ab6', 'A6', 'Gb6', 'A6', 'Gb6', 'A6', 'Gb6', 'A6', 'Ab6', 'A6', 'B6', 'Ab6', 'E6', 'Ab6', 'E6', 'Ab6', 'E6', 'A6', 'Ab6', 'Gb6', 'Ab6', 'E6', 'Ab6', 'E6', 'Ab6', 'E6', 'A6', 'Ab6', 'Gb6', 'E6', 'Db6', 'E6', 'Db6', 'E6', 'Db6', 'E6', 'Eb6', 'E6', 'Gb6', 'A6', 'Gb6', 'A6', 'Gb6', 'A6', 'Gb6', 'B6', 'A6', 'Ab6', 'A6', 'Gb6', 'A6', 'Gb6', 'A6', 'Gb6', 'B6', 'A6', 'Ab6', 'A6', 'Gb6', 'A6', 'Gb6', 'A6', 'Gb6', 'A6', 'Ab6', 'A6', 'B6', 'B6', 'G6', 'B6', 'G6', 'B6', 'G6', 'C7', 'B6', 'A6', 'B6', 'G6', 'B6', 'G6', 'B6', 'G6', 'C7', 'B6', 'A6', 'G6', 'E6', 'D6', 'G6', 'E6', 'G6', 'E6', 'G6', 'Gb6', 'G6', 'A6', 'C7', 'A6', 'C7', 'A6', 'C7', 'A6', 'D7', 'C7', 'B6', 'C7', 'A6', 'C7', 'A6', 'C7', 'A6', 'D7', 'C7', 'B6', 'C7', 'B6', 'A6', 'C7', 'A6', 'C7', 'A6', 'C7', 'B6', 'C7', 'D7', 'Bb6', 'Eb7', 'D7', 'C7', 'D7', 'Eb7', 'Bb6', 'G6', 'Ab6', 'Bb6', 'Ab6', 'G6', 'F6', 'Eb6', 'G6', 'F6', 'Bb6', 'G7', 'Ab7', 'G7', 'F7', 'Eb7', 'F7', 'G7', 'F7', 'D7', 'F7', 'Eb7', 'C7', 'D7', 'Eb7', 'Ab6', 'G6', 'Eb6', 'F6', 'G6', 'Ab6', 'G6', 'Bb6', 'Ab6', 'G6', 'F6', 'F6', 'Db6', 'F6', 'Db6', 'F6', 'Db6', 'Gb6', 'F6', 'Eb6', 'F6', 'Db6', 'Eb6', 'F6', 'Db6', 'F6', 'Db6', 'Gb6', 'F6', 'Eb6', 'Db6', 'Bb5', 'Db6', 'Bb5', 'Db6', 'Bb5', 'Db6', 'C6', 'Db6', 'Eb6', 'Gb6', 'Eb6', 'Gb6', 'Eb6', 'Gb6', 'Eb6', 'Ab6', 'Gb6', 'F6', 'Gb6', 'Eb6', 'Gb6', 'Eb6', 'Gb6', 'Eb6', 'Ab6', 'Gb6', 'F6', 'Gb6', 'Eb6', 'Gb6', 'Eb6', 'Gb6', 'Eb6', 'Gb6', 'F6', 'Gb6', 'Ab6', 'Ab6', 'E6', 'Ab6', 'E6', 'Ab6', 'E6', 'A6', 'Ab6', 'Gb6', 'Ab6', 'E6', 'Ab6', 'E6', 'Ab6', 'E6', 'A6', 'Ab6', 'Gb6', 'E6', 'Db6', 'E6', 'Db6', 'E6', 'Db6', 'E6', 'Eb6', 'E6', 'Gb6', 'A6', 'Gb6', 'A6', 'Gb6', 'A6', 'Gb6', 'B6', 'A6', 'Ab6', 'A6', 'Gb6', 'A6', 'Gb6', 'A6', 'Gb6', 'B6', 'A6', 'Ab6', 'A6', 'Gb6', 'A6', 'Gb6', 'A6', 'Gb6', 'A6', 'Ab6', 'A6', 'B6', 'B6', 'G6', 'B6', 'G6', 'B6', 'G6', 'C7', 'B6', 'A6', 'B6', 'G6', 'B6', 'G6', 'B6', 'G6', 'C7', 'B6', 'A6', 'G6', 'E6', 'G6', 'E6', 'G6', 'E6', 'G6', 'Gb6', 'G6', 'A6', 'C7', 'A6', 'C7', 'A6', 'C7', 'A6', 'D7', 'C7', 'B6', 'C7', 'A6', 'C7', 'A6', 'C7', 'A6', 'D7', 'C7', 'B6', 'C7', 'A6', 'C7', 'A6', 'C7', 'A6', 'C7', 'B6', 'C7', 'D7', 'Bb6', 'Eb7', 'D7', 'C7', 'D7', 'Eb7', 'Bb6', 'G6', 'Ab6', 'Bb6', 'Ab6', 'G6', 'F6', 'Eb6', 'G6', 'F6', 'Bb6', 'G7', 'Ab7', 'G7', 'F7', 'Eb7', 'F7', 'G7', 'F7', 'D7', 'F7', 'Eb7', 'C7', 'D7', 'Eb7', 'Ab6', 'G6', 'Eb6', 'F6', 'G6', 'Ab6', 'G6', 'Bb6', 'Ab6', 'G6', 'F6']


melodyindex = 0

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

def play_next_note():
    global melodyindex
    print(f"Playing Note {melody[melodyindex]}, index {melodyindex}")
    path = "keys/" + melody[melodyindex] + ".mp3"
    playsound(str(path), False)
    print(len(melody))
    if melodyindex < len(melody)-1:
        melodyindex = melodyindex +1
    else:
        melodyindex = 0

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
    global stopped
    going = True
    performance = False
    while going:
        events = event_get()
        for e in events:
            if e.type in [pg.QUIT]:
                going = False
                print("DED")
                exit()
            if e.type in [pygame.midi.MIDIIN]:
                print(e)
                if(performance == False):
                    if(e.data1 == 49 and e.status == 153): #Press PAD 8 
                        performance = True
                        playsound("sound/faster.mp3", False)
                        print("\nPERFORMANCE MODE ACTIVATED\n")
                    elif(e.data1 == 1 and e.data2 == 0): #MOD bas
                        data = b'P_BRAKE'
                        client_socket.sendto(data, address)
                    elif(e.data1 == 1 and (e.data2 != 0 and e.data2 != 127)): #MOD milieu
                        data = b'R_BRAKE'
                        client_socket.sendto(data, address)
                        data = b'R_ACCELERATE'
                        client_socket.sendto(data, address)
                    elif(e.data1 == 1 and e.data2 == 127): #MOD haut
                        data = b'P_ACCELERATE'
                        client_socket.sendto(data, address)
                    elif(e.data1 >= 48 and e.data1 <= 72 and e.status == 144): #Press piano key
                        play_next_note()
                        stopped = False
                        t = Thread(target=turnIntensity,args=(e.data1,e.status,))
                        t.start()
                    elif(e.data1 >= 48 and e.data1 <= 72 and e.status == 128): #Press piano key
                        stopped = True
                elif(performance):
                    if(e.data1 == 49 and e.status == 153): #Press PAD 8
                        performance = False
                        playsound("sound/deja-vu.mp3", False)
                        print("\nFUN MODE ACTIVATED\n")
                    elif(e.data1 == 0 and e.data2 < 64): #PITCH bas
                        data = b'P_LOOKBACK'
                        client_socket.sendto(data, address)
                        data = b'R_SKIDDING'
                        client_socket.sendto(data, address)
                    elif(e.data1 == 0 and e.data2 > 64): #PITCH milieu
                        data = b'R_LOOKBACK'
                        client_socket.sendto(data, address)
                        data = b'P_SKIDDING'
                        client_socket.sendto(data, address)
                    elif(e.data1 == 0 and e.data2 == 64): #PITCH milieu
                        data = b'R_LOOKBACK'
                        client_socket.sendto(data, address)
                        data = b'R_SKIDDING'
                        client_socket.sendto(data, address)
                    elif(e.data1 >= 60 and e.data1 <= 72 and e.status == 144): #Press piano right
                        data = b'P_RIGHT'
                        client_socket.sendto(data, address)
                    elif(e.data1 >= 60 and e.data1 <= 72 and e.status == 128): #Release piano right
                        data = b'R_RIGHT'
                        client_socket.sendto(data, address)
                    elif(e.data1 >= 48 and e.data1 <= 59 and e.status == 144): #Press piano left
                        data = b'P_LEFT'
                        client_socket.sendto(data, address)
                    elif(e.data1 >= 48 and e.data1 <= 59 and e.status == 128): #Release piano left
                        data = b'R_LEFT'
                        client_socket.sendto(data, address)
                    elif(e.data1 >= 48 and e.data1 <= 71 and e.status == 128): #Press piano right
                        stopped = True
                    elif(e.data1 == 1 and e.data2 == 0): #MOD bas
                        data = b'P_BRAKE'
                        client_socket.sendto(data, address)
                    elif(e.data1 == 1 and (e.data2 != 0 and e.data2 != 127)): #MOD milieu
                        data = b'R_BRAKE'
                        client_socket.sendto(data, address)
                        data = b'R_ACCELERATE'
                        client_socket.sendto(data, address)
                    elif(e.data1 == 1 and e.data2 == 127): #MOD haut
                        data = b'P_ACCELERATE'
                        client_socket.sendto(data, address)
                    elif(e.data1 == 36 and e.status == 153): #Press PAD 1 
                        data = b'P_FIRE'
                        client_socket.sendto(data, address)
                    elif(e.data1 == 36 and e.status == 137): #Release PAD 1
                        data = b'R_FIRE'
                        client_socket.sendto(data, address)
                    elif(e.data1 == 50 and e.status == 153): #Press PAD 5
                        data = b'P_RESCUE'
                        client_socket.sendto(data, address)
                    elif(e.data1 == 50 and e.status == 137): #Release PAD 5
                        data = b'R_RESCUE'
                        client_socket.sendto(data, address)
                    elif(e.data1 == 38 and e.status == 153): #Press PAD 2
                        data = b'P_NITRO'
                        client_socket.sendto(data, address)
                    elif(e.data1 == 38 and e.status == 137): #Release PAD 2
                        data = b'R_NITRO'
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

def turnIntensity(touche,pushed):
    pas = 0.2
    #GAUCHE
    if touche <= 59:
        print(f"ToucheG = {touche-47}")
        while(pushed == 144):
            data = b'P_LEFT'
            client_socket.sendto(data, address)
            sleep((touche-47)/13*pas)
            data = b'R_LEFT'
            client_socket.sendto(data, address)
            print((touche-47)/13*pas)
            if stopped:
                break
    elif touche <= 72:
        print(f"ToucheD = {-1*touche+73}")
        while(pushed == 144):
            data = b'P_RIGHT'
            client_socket.sendto(data, address)
            sleep((-1*touche+73)/12*pas)
            data = b'R_RIGHT'
            client_socket.sendto(data, address)
            print((-1*touche+73)/12*pas)
            if stopped:
                break
    return

input_main(1)

sleep(1000)
osc.stop()  # Stop the default socket