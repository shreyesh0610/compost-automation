import os
import sys


from utils import *
from database import *
from embedded import *

databaseHelper:DatabaseHelper = DatabaseHelper()

arduinoGenerator = ReadFromArduino(ARDUINO_SENSOR_PORT)
last_sync_time = datetime.now(pytz.utc)

def GetCurrentProcessID():
    processData:ProcessData = databaseHelper.GetCurrentProcess()
    return processData.process_id if processData else ''

def StartNewProcess():
    print('Starting New Process')
    current_process_id = create_process_id()

    print(f'{current_process_id} >> Inserting New Process Data')
    databaseHelper.InsertProcessData(
        processData = ProcessData(
            process_id = current_process_id,
            start_time = datetime.now(pytz.utc),
            end_time = None,
            current_phase = 'Phase 1',
            mature_percentage = 0,
            mature_result = 'Immature'
        )
    )
    StartCompostProcessor()
    return current_process_id

def StopProcess(process_id:str):
    print(f'{process_id} >> Stopping Process')

    processData:ProcessData = databaseHelper.GetProcessData(process_id = process_id)
    if processData:
        processData.end_time = datetime.now(pytz.utc)
        print(f'{process_id} >> Updating Process Data')
        databaseHelper.UpdateProcessData(processData=processData)

    StopCompostProcessor()
    return process_id

def BackgroundProcess():
    while True:

        #* get current process id
        current_process_id:str = GetCurrentProcessID()
        if not current_process_id:
            print('There is no process in progress currently. Sleeping for 60 seconds')
            time.sleep(60)
            continue

        StartCompostProcessor()

        #* Read sensor data from Arduino
        #region Sensor Data
        sensor_data_string = next(arduinoGenerator, None)
        if not sensor_data_string.strip(): continue

        # soil humidity: 30.70, soil temperature: 25.90, soil conductivity: 1053, soil ph: 5.10, nitrogen: 181, phosphorus: 465, potassium: 460
        sensor_data_string = sensor_data_string.lower().strip()
        if not all([
            'soil humidity' in sensor_data_string,
            'soil temperature' in sensor_data_string,
            'soil conductivity' in sensor_data_string,
            'soil ph' in sensor_data_string,
            'soil nitrogen' in sensor_data_string,
            'soil phosphorus' in sensor_data_string,
            'soil potassium' in sensor_data_string,
        ]):
            print(f'{current_process_id} >> Invalid reading string = {sensor_data_string}')
            continue

        split_data = sensor_data_string.split(',')

        try: split_numbers = [float(sd.split(':')[-1].strip()) for sd in split_data]
        except: split_numbers = []

        if len(split_numbers) != 7:
            print(f'{current_process_id} >> Sensor values are not equal to 7 = {sensor_data_string}')
            continue

        sensorData:SensorData = SensorData(
            process_id = current_process_id,
            humidity = split_numbers[0],
            temperature = split_numbers[1],
            ec = split_numbers[2],
            ph = split_numbers[3],
            nitrogen = split_numbers[4],
            phosphorus = split_numbers[5],
            potassium = split_numbers[6],
            timestamp = datetime.now(pytz.utc)
        )
        print(f'{current_process_id} >> Inserting sensor data')
        databaseHelper.InsertSensorData(sensorData=sensorData)
        #endregion

        #* ML Model
        #region ML Model
        #TODO - Call ML Model every 1 hour to get phase, maturity and maturity percentage
        #TODO - update process data in DB
        #endregion