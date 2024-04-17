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
        # cursor.execute('''
        #     CREATE TABLE IF NOT EXISTS sensor_data
        #     (
        #         id INTEGER NOT NULL AUTOINCREMENT,
        #         process_id TEXT,
        #         humidity REAL,
        #         temperature REAL,
        #         ec REAL,
        #         ph REAL,
        #         nitrogen REAL,
        #         phophorus REAL,
        #         potassium REAL,
        #         timestamp DATETIME,
        #         PRIMARY KEY (id)
        #     );
        #     '''
        # )
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

        # cursor.execute('''
        #     CREATE TABLE IF NOT EXISTS process_data
        #     (
        #         process_id TEXT AUTOINCREMENT,
        #         start_time DATETIME,
        #         end_time DATETIME,
        #         current_phase TEXT,
        #         mature_percentage REAL,
        #         mature_result TEXT,
        #         PRIMARY KEY (process_id)
        #     );
        #     '''
        # )
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

    def GetSensorData(self, process_id:str):
        sensorDataList:List[SensorData] = []

        cursor = self.connection.cursor()
        cursor.execute("SELECT process_id, humidity, temperature, ec, ph, nitrogen, phosphorus, potassium, timestamp FROM sensor_data WHERE process_id = ?", (process_id,))

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
                        convert_datetime_to_string(processData.end_time),
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
                start_time = row[1],
                end_time = row[2],
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

if __name__ == '__main__':
    databaseHelper:DatabaseHelper = DatabaseHelper()
