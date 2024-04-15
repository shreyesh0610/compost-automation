import sys
import os
from os.path import dirname
sys.path.append(os.path.abspath(os.path.join(dirname(__file__), os.pardir)))

import serial
import sys
import RPi.GPIO as GPIO

from utils import *

GPIO.setmode(GPIO.BCM)
GPIO.setup(PROCESSOR_RUN_PIN_NO, GPIO.OUT)
GPIO.setup(PROCESSOR_PHASE_PIN_NO_1, GPIO.OUT)
GPIO.setup(PROCESSOR_PHASE_PIN_NO_2, GPIO.OUT)


def RPReadFromArduino(serial_port:str):
    ser = serial.Serial(port = serial_port, baudrate = 9600)

    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()
            yield line

def RPStartCompostProcessor():
    print('Starting Compost Processor')
    GPIO.output(PROCESSOR_RUN_PIN_NO, GPIO.HIGH)

def RPStopCompostProcessor():
    print('Stopping Compost Processor')
    GPIO.output(PROCESSOR_RUN_PIN_NO, GPIO.LOW)

def RPSetProcessorPhase(phase_no:int):
    print('Setting Compost Processor Phase: Phase {phase_no}')

    if phase_no == 1: #- 00
        GPIO.output(PROCESSOR_PHASE_PIN_NO_1, GPIO.LOW)
        GPIO.output(PROCESSOR_PHASE_PIN_NO_1, GPIO.LOW)
    elif phase_no == 2: #- 01
        GPIO.output(PROCESSOR_PHASE_PIN_NO_1, GPIO.LOW)
        GPIO.output(PROCESSOR_PHASE_PIN_NO_1, GPIO.HIGH)
    elif phase_no == 3: #- 10
        GPIO.output(PROCESSOR_PHASE_PIN_NO_1, GPIO.HIGH)
        GPIO.output(PROCESSOR_PHASE_PIN_NO_1, GPIO.LOW)
    elif phase_no == 4: #- 11
        GPIO.output(PROCESSOR_PHASE_PIN_NO_1, GPIO.HIGH)
        GPIO.output(PROCESSOR_PHASE_PIN_NO_1, GPIO.HIGH)
    else: #- default 00
        GPIO.output(PROCESSOR_PHASE_PIN_NO_1, GPIO.LOW)
        GPIO.output(PROCESSOR_PHASE_PIN_NO_1, GPIO.LOW)