import sys
import os

from utils.helper import *

class SensorData:
    def __init__(self,
                 process_id:str,
                 humidity:float,
                 temperature:float,
                 ec:float,
                 ph:float,
                 nitrogen:float,
                 phosphorus:float,
                 potassium:float,
                 timestamp:datetime
    ):
        self.process_id = process_id
        self.humidity = humidity
        self.temperature = temperature
        self.ec = ec
        self.ph = ph
        self.nitrogen = nitrogen
        self.phosphorus = phosphorus
        self.potassium = potassium
        self.timestamp = timestamp
    
    def convert_to_dict(self):
        return {
            'process_id': self.process_id,
            "humidity": self.humidity,
            "temperature": self.temperature,
            "ec": self.ec,
            'ph': self.ph,
            'nitrogen': self.nitrogen,
            'phosphorus': self.phosphorus,
            'potassium': self.potassium,
            'timestamp': convert_datetime_to_string(self.timestamp)
        }

class ProcessData:
    def __init__(self,
                process_id:str,
                start_time:datetime,
                end_time:datetime,
                current_phase:str,
                mature_percentage:float,
                mature_result:str
    ):
        
        self.process_id = process_id
        self.start_time = start_time
        self.end_time = end_time
        self.current_phase = current_phase
        self.mature_percentage = mature_percentage
        self.mature_result = mature_result
    
    def convert_to_dict(self):
        return {
            'process_id': self.process_id,
            'start_time': convert_datetime_to_string(self.start_time),
            'end_time': convert_datetime_to_string(self.end_time),
            'current_phase': self.current_phase,
            'mature_percentage': self.mature_percentage,
            'mature_result': self.mature_result
        }