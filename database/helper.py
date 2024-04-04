import sys
import os
from os.path import dirname
sys.path.append(os.path.abspath(os.path.join(dirname(__file__), os.pardir)))

from utils import *

class DatabaseHelper:
    def __init__(self):
        self.connection = sqlite3.connect(DATABASE_PATH)

        self.CreateTableIfNotExists()

    def CreateTableIfNotExists(self):
        cursor = self.connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sensor_data
            (
                id INTEGER NOT NULL AUTOINCREMENT,
                process_id TEXT,
                timestamp TEXT DEFAULT CURRENT_TIMESTAMP, 
                humidity REAL, 
                temperature REAL, 
                ec REAL, 
                ph REAL, 
                nitrogen REAL,
                phophorus REAL, 
                potassium REAL,
                PRIMARY KEY (id)
            );
            '''
        )

    def InsertSensorData(self, process_id:str, sensorData:SensorData):
        cursor = self.connection.cursor()
        cursor.execute('''
                       INSERT INTO sensor_data (process_id, humidity, temperature, ec, ph, nitrogen, phosphorus, potassium) 
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?);
                       ''',
                       (process_id, sensorData.humidity, sensorData.temperature, sensorData.ec, sensorData.ph, sensorData.nitrogen, sensorData.phosphorus, sensorData.potassium)
        )
        self.connection.commit()
        cursor.close()

    def GetSensorData(self, process_id:str):
        sensorDataList:List[SensorData] = []

        cursor = self.connection.cursor()
        cursor.execute("SELECT humidity, temperature, ec, ph, nitrogen, phosphorus, potassium FROM sensor_data WHERE process_id = ?", (process_id,))

        rows = cursor.fetchall()
        for row in rows:
            sensorDataList.append(SensorData(
                humidity = row[0],
                temperature = row[1],
                ec = row[2],
                ph = row[3],
                nitrogen = row[4],
                phosphorus = row[5],
                potassium = row[6]
            ))
        cursor.close()
        return sensorDataList

if __name__ == '__main__':
    databaseHelper:DatabaseHelper = DatabaseHelper()
