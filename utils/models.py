import sys
import os

# from utils.helper import *
from typing import List,Dict,Optional,Union,Tuple,Any
from pydantic import BaseModel, model_validator
from enum import Enum
import threading
from datetime import datetime, timedelta
import pytz

class FastAPITag(Enum):
    def __str__(self): return self.value    
    UI = "UI"
    Internal = "Internal"

class SensorData:
    def __init__(self,
                humidity:float,
                temperature:float,
                ec:float,
                ph:float,
                nitrogen:float,
                phosphorus:float,
                potassium:float 
    ):
        
        self.humidity = humidity
        self.temperature = temperature
        self.ec = ec
        self.ph = ph
        self.nitrogen = nitrogen
        self.phosphorus = phosphorus
        self.potassium = potassium