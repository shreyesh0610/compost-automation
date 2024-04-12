import sys
import os
from os.path import dirname
sys.path.append(os.path.abspath(os.path.join(dirname(__file__), os.pardir)))

import serial
import sys
import RPi.GPIO as GPIO

from utils import *

GPIO.setmode(GPIO.BCM)
GPIO.setup(PROCESSOR_PIN_NO, GPIO.OUT)


def ReadFromArduino(serial_port:str):
    ser = serial.Serial(port = serial_port, baudrate = 9600)

    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()
            yield line

def StartCompostProcessor():
    print('Starting Compost Processor')
    GPIO.output(PROCESSOR_PIN_NO, GPIO.HIGH)

def StopCompostProcessor():
    print('Stopping Compost Processor')
    GPIO.output(PROCESSOR_PIN_NO, GPIO.LOW)