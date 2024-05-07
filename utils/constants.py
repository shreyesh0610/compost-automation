import sys
import os
from os.path import dirname
sys.path.append(os.path.abspath(os.path.join(dirname(__file__), os.pardir)))

from typing import List,Dict

# CURRENT_DIRECTORY = os.getenv("CURRENT_DIRECTORY", f"{os.getcwd()}")
CURRENT_DIRECTORY = os.getenv("CURRENT_DIRECTORY", '/home/admin/Desktop/test-compostifAI/compost-automation')

DEBUGGING = True if os.getenv('DEBUGGING') and str(os.getenv('DEBUGGING')).upper() == 'TRUE' else False
MOCK_API = True if os.getenv('MOCK_API') and str(os.getenv('MOCK_API')).upper() == 'TRUE' else False

# * Database
DATABASE_PATH = os.getenv('DATABASE_PATH', f'{CURRENT_DIRECTORY}/compost.db')

#* Arduino
ARDUINO_SENSOR_PORT = os.getenv('ARDUINO_SENSOR_PORT', '/dev/ttyUSB0')

#* RaspberryPi
PROCESSOR_RUN_PIN_NO = int(os.getenv('PROCESSOR_RUN_PIN_NO', 18))
PROCESSOR_PHASE_PIN_NO_1 = int(os.getenv('PROCESSOR_PHASE_PIN_NO_1', 19))
PROCESSOR_PHASE_PIN_NO_2 = int(os.getenv('PROCESSOR_PHASE_PIN_NO_2', 20))

#* ML
DATASET_EXCEL_PATH = os.getenv('DATASET_EXCEL_PATH', f'{CURRENT_DIRECTORY}/ml/dataset3.xlsx')
LR_SHEET_NAME = os.getenv('LR_SHEET_NAME', 'Linear Regression-')
RF_SHEET_NAME = os.getenv('RF_SHEET_NAME', 'Random Forest')
