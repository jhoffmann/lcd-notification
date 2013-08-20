#!/usr/bin/python

from Adafruit_CharLCD import Adafruit_CharLCD
from time import sleep
import socket
from NotificationCenter import NotificationCenter

NC_METHODS = [
    'startup',
    'fun1',
    'status_date',
    'status_weather',
    'status_torrents'
    ]

nc = NotificationCenter()
lcd = Adafruit_CharLCD()
lcd.begin(16,1)

""" Try to keep the weather request from tying things up """
socket.setdefaulttimeout(2)

while 1:
    for NC_METHOD in NC_METHODS:
        res = getattr(nc, NC_METHOD)()
        if len(res):
            lcd.clear()
            lcd.message("\n".join(res))
            sleep(15)
