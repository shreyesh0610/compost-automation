import os
import sys
import time

from utils import *
from database import *
from embedded import *
from ml import *

databaseHelper:DatabaseHelper = DatabaseHelper()
mlHelper:MLHelper = MLHelper()

LAST_SYNC_TIME = datetime.now().replace(tzinfo=None)- timedelta(hours=1) #- already settinb one hour behind so it runs for the first time at the start of the code

def ShouldProcessML():
    #- function to monitor if its been 1 hour since last ML run
    global LAST_SYNC_TIME

    # if LAST_SYNC_TIME < datetime.now().replace(tzinfo=None) - timedelta(hours=1):   #- will only run once per hour
    if LAST_SYNC_TIME < datetime.now().replace(tzinfo=None) - timedelta(minutes=1): #- will only run once per min
        return True
    return False

def CollectProcess(process_id):
    return databaseHelper.InsertCollectProcess(process_id)

def GetCurrentProcessID():
    processData:ProcessData = databaseHelper.GetCurrentProcess()
    return processData.process_id if processData else ''

def StartNewProcess(is_mature_process:bool=False):
    print('Starting New Process')

    #- If a process is already going on, do not create another process.
    #- return the ongoing process ID

    any_old_process_id:str = GetCurrentProcessID()

    if any_old_process_id:
        current_process_id = any_old_process_id
    else:
        current_process_id = create_process_id()

        print(f'{current_process_id} >> Inserting New Process Data')
        databaseHelper.InsertProcessData(
            processData = ProcessData(
                process_id = current_process_id,
                start_time = datetime.now(),
                end_time = None,
                current_phase = 'Phase 1',
                mature_percentage = 0,
                mature_result = 'Immature',
                is_mature_process = is_mature_process
            )
        )
    RPStartCompostProcessor()
    RPSetProcessorPhase(0)
    return current_process_id

def StopProcess(process_id:str):
    print(f'{process_id} >> Stopping Process')

    processData:ProcessData = databaseHelper.GetProcessData(process_id = process_id)
    if processData:
        processData.end_time = datetime.now()
        print(f'{process_id} >> Updating Process Data')
        databaseHelper.UpdateStopProcessData(process_id=processData.process_id)

    RPStopCompostProcessor()
    RPSetProcessorPhase(0)
    return process_id

def BackgroundProcess():
    arduinoGenerator = RPReadFromArduino(ARDUINO_SENSOR_PORT)
    while True:
        try:
            #* Get current process id
            current_process_id:str = GetCurrentProcessID()
            if not current_process_id:
                print('There is no process in progress currently. Sleeping')
                time.sleep(1)
                continue
            processData:ProcessData = databaseHelper.GetProcessData(process_id = current_process_id)

            RPStartCompostProcessor()

            print(f'{current_process_id} >> {"MATURE" if processData.is_mature_process else "STANDARD"} >> Processing')

            if not processData.is_mature_process: #- if its STANDARD process

                #* Read sensor data from Arduino
                #region Sensor Data
                print(f'{current_process_id} >> {"MATURE" if processData.is_mature_process else "STANDARD"} >> Reading Sensor')
                sensor_data_string = next(arduinoGenerator, None)
                if not sensor_data_string:
                    print(f'{current_process_id} >> {"MATURE" if processData.is_mature_process else "STANDARD"} >> No sensor data found to read.')
                    time.sleep(1)
                    try: current_phase_no = int(processData.current_phase.split('Phase')[1].strip())
                    except: current_phase_no = 0
                    RPSetProcessorPhase(current_phase_no)
                    continue

                # soil humidity: 30.70, soil temperature: 25.90, soil conductivity: 1053, soil ph: 5.10, nitrogen: 181, phosphorus: 465, potassium: 460
                sensor_data_string = sensor_data_string.lower().strip()
                if not all([
                    'soil humidity:' in sensor_data_string,
                    'soil temperature:' in sensor_data_string,
                    'soil conductivity:' in sensor_data_string,
                    'soil ph:' in sensor_data_string,
                    'soil nitrogen:' in sensor_data_string,
                    'soil phosphorus:' in sensor_data_string,
                    'soil potassium:' in sensor_data_string,
                ]):
                    print(f'{current_process_id} >> {"MATURE" if processData.is_mature_process else "STANDARD"} >> Invalid reading string = {sensor_data_string}')
                    time.sleep(1)
                    continue

                split_data = sensor_data_string.split(',')

                try: split_numbers = [float(sd.split(':')[-1].strip()) for sd in split_data]
                except: split_numbers = []

                if len(split_numbers) != 7:
                    print(f'{current_process_id} >> {"MATURE" if processData.is_mature_process else "STANDARD"} >> Sensor values are not equal to 7 = {sensor_data_string}')
                    time.sleep(1)
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
                    timestamp = datetime.now()
                )
                print(f'{current_process_id} >> {"MATURE" if processData.is_mature_process else "STANDARD"} >> Inserting sensor data')
                databaseHelper.InsertSensorData(sensorData=sensorData)
                #endregion

                #* ML Model
                #region ML Model
                predicted_phase = mlHelper.PredictPhase(
                    temperature = sensorData.temperature,
                    humidity = sensorData.humidity,
                    ec = sensorData.ec,
                    ph = sensorData.ph
                )

                predicted_maturity = mlHelper.PredictMaturity(
                    temperature = sensorData.temperature,
                    humidity = sensorData.humidity,
                    ec = sensorData.ec,
                    ph = sensorData.ph
                )
                #endregion

                # - logic to not let phase go backward
                try: old_phase = int(processData.current_phase.split('Phase')[1].strip())
                except: old_phase = 0
                predicted_phase = predicted_phase if predicted_phase >= old_phase else old_phase
                # ----------

                #- Logic to hardcode maturity for Phase 1-3
                if predicted_phase <= 3:
                    predicted_maturity = "Immature"

            else: #- if process is MATURE process
                predicted_phase = 4             #- default phase of MATURE process
                predicted_maturity = 'Mature'   #- default maturity of MATURE process

            processData.current_phase = f'Phase {predicted_phase}'
            processData.mature_result = predicted_maturity if processData.mature_result != 'Mature' else processData.mature_result

            print(f'{current_process_id} >> {"MATURE" if processData.is_mature_process else "STANDARD"} >> Predicted Phase: {predicted_phase}, Maturity: {predicted_maturity}')
            databaseHelper.UpdateProcessData(processData)

            RPSetProcessorPhase(predicted_phase)
            time.sleep(1)

        except Exception as ex:
            print(ex)
            traceback.print_exc()


if __name__ == '__main__':
    BackgroundProcess()