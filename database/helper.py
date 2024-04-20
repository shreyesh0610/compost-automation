import sys
import os
from os.path import dirname
sys.path.append(os.path.abspath(os.path.join(dirname(__file__), os.pardir)))

from utils import *

class DatabaseHelper:
    def __init__(self):
        print(f'Creating DB at {DATABASE_PATH}')
        self.connection = sqlite3.connect(DATABASE_PATH, check_same_thread=False)

        self.CreateTablesIfNotExists()

    def CreateTablesIfNotExists(self):
        cursor = self.connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sensor_data
            (
                id INTEGER PRIMARY KEY,
                process_id TEXT,
                humidity REAL,
                temperature REAL,
                ec REAL,
                ph REAL,
                nitrogen REAL,
                phosphorus REAL,
                potassium REAL,
                timestamp DATETIME
            );
            '''
        )

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS process_data
            (
                process_id TEXT PRIMARY KEY,
                start_time DATETIME,
                end_time DATETIME,
                current_phase TEXT,
                mature_percentage REAL,
                mature_result TEXT
            );
            '''
        )

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS collect_process_data
            (
                process_id TEXT PRIMARY KEY,
                collect_time DATETIME
            );
            '''
        )

        self.connection.commit()
        cursor.close()

    def InsertSensorData(self, sensorData:SensorData):
        cursor = self.connection.cursor()
        cursor.execute('''
                       INSERT INTO sensor_data (process_id, timestamp, humidity, temperature, ec, ph, nitrogen, phosphorus, potassium)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
                       ''',
                       (
                           sensorData.process_id,
                           convert_datetime_to_string(sensorData.timestamp),
                           sensorData.humidity,
                           sensorData.temperature,
                           sensorData.ec,
                           sensorData.ph,
                           sensorData.nitrogen,
                           sensorData.phosphorus,
                           sensorData.potassium
                       )
        )
        self.connection.commit()
        cursor.close()

    def GetSensorData(self, process_id:str, only_one:bool=True):
        sensorDataList:List[SensorData] = []

        cursor = self.connection.cursor()
        if only_one: cursor.execute("SELECT process_id, humidity, temperature, ec, ph, nitrogen, phosphorus, potassium, timestamp FROM sensor_data WHERE process_id = ? ORDER BY timestamp DESC LIMIT 1", (process_id,))
        else: cursor.execute("SELECT process_id, humidity, temperature, ec, ph, nitrogen, phosphorus, potassium, timestamp FROM sensor_data WHERE process_id = ?", (process_id,))

        rows = cursor.fetchall()
        for row in rows:
            sensorDataList.append(SensorData(
                process_id = row[0],
                humidity = row[1],
                temperature = row[2],
                ec = row[3],
                ph = row[4],
                nitrogen = row[5],
                phosphorus = row[6],
                potassium = row[7],
                timestamp = convert_string_to_datetime(row[8])
            ))
        cursor.close()
        return sensorDataList

    def InsertProcessData(self, processData:ProcessData):
        cursor = self.connection.cursor()
        cursor.execute('''
                       INSERT INTO process_data (process_id, start_time, end_time, current_phase, mature_percentage, mature_result)
                       VALUES (?, ?, ?, ?, ?, ?);
                       ''',
                       (
                           processData.process_id,
                           convert_datetime_to_string(processData.start_time),
                           convert_datetime_to_string(processData.end_time) if processData.end_time else None,
                           processData.current_phase,
                           processData.mature_percentage,
                           processData.mature_result,
                       )
        )
        self.connection.commit()
        cursor.close()

    def UpdateProcessData(self, processData: ProcessData):
        cursor = self.connection.cursor()
        cursor.execute('''
                    UPDATE process_data
                    SET end_time = ?,
                        current_phase = ?,
                        mature_percentage = ?,
                        mature_result = ?
                    WHERE process_id = ?;
                    ''',
                    (
                        convert_datetime_to_string(processData.end_time) if processData.end_time else None,
                        processData.current_phase,
                        processData.mature_percentage,
                        processData.mature_result,
                        processData.process_id
                    )
        )
        self.connection.commit()
        cursor.close()

    def GetProcessData(self, process_id:str):
        processData:ProcessData = None

        cursor = self.connection.cursor()
        cursor.execute("SELECT process_id, start_time, end_time, current_phase, mature_percentage, mature_result FROM process_data WHERE process_id = ?", (process_id,))

        rows = cursor.fetchall()
        for row in rows:
            processData:ProcessData = ProcessData(
                process_id = row[0],
                start_time = convert_string_to_datetime(row[1]) if row[1] else None,
                end_time = convert_string_to_datetime(row[2]) if row[2] else None,
                current_phase = row[3],
                mature_percentage = row[4],
                mature_result = row[5]
            )
            break #- only 1
        cursor.close()
        return processData

    def GetCurrentProcess(self):
        processData:ProcessData = None

        cursor = self.connection.cursor()
        cursor.execute("SELECT process_id, start_time, end_time, current_phase, mature_percentage, mature_result FROM process_data WHERE end_time IS NULL ORDER BY start_time DESC")

        rows = cursor.fetchall()
        for row in rows:
            processData:ProcessData = ProcessData(
                process_id = row[0],
                start_time = row[1],
                end_time = row[2],
                current_phase = row[3],
                mature_percentage = row[4],
                mature_result = row[5]
            )
            break #- only 1
        cursor.close()
        return processData

    def InsertCollectProcess(self, process_id:str, collect_time:datetime = datetime.now()):
        cursor = self.connection.cursor()
        cursor.execute('''
                       INSERT INTO collect_process_data (process_id, collect_time)
                       VALUES (?, ?);
                       ''',
                       (
                           process_id,
                           convert_datetime_to_string(collect_time),
                       )
        )
        self.connection.commit()
        cursor.close()
        return process_id

    def GetCollectProcessIDs(self):
        process_id_list:List[str] = []

        cursor = self.connection.cursor()
        cursor.execute("SELECT process_id FROM collect_process_data ORDER BY collect_time DESC;")

        rows = cursor.fetchall()
        for row in rows:
            process_id_list.append(row[0])
        cursor.close()
        return process_id_list

if __name__ == '__main__':
    databaseHelper:DatabaseHelper = DatabaseHelper()
