import sys
import os
from os.path import dirname
sys.path.append(os.path.abspath(os.path.join(dirname(__file__), os.pardir)))

from datetime import datetime, timedelta
from enum import Enum
from fastapi import FastAPI, Request, Response, WebSocket, WebSocketDisconnect
from fastapi.exceptions import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from itertools import cycle
from pydantic import BaseModel, model_validator
from typing import List,Dict,Optional,Union,Tuple,Any
import asyncio
import base64
import copy
import hashlib
import json
import math
import nanoid
import numpy as np
import os
import pandas as pd
import pytz
import pytz
import queue
import random
import requests
import sqlite3
import statistics
import threading
import time
import traceback
import uvicorn


from utils.constants import *

import signal
class GracefulKiller:
    import signal
    kill_now = False
    last_ping = datetime.now()
    def __init__(self):
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)
        if os.name != 'nt': signal.signal(signal.SIGALRM, self.check_ping)

    def exit_gracefully(self, *args):
        self.kill_now = True

    def exit(self):
        os.kill(os.getpid(), signal.SIGTERM)

    def crash_it(self):
        print('Exiting Poppy. Crashing it.')
        os._exit(0)

    def update_ping(self):
        GracefulKiller.last_ping = datetime.now()

    def check_ping(self, *args):
        if os.name == 'nt': return
        print('Checking Ping')
        difference = datetime.now() - GracefulKiller.last_ping
        if difference.total_seconds() > 60: #- last ping was 1min ago
            self.crash_it()
        signal.alarm(300) #- repeat every 5 mins

killer = GracefulKiller()

def create_process_id():
    process_id = nanoid.generate(size=6)
    return process_id

def convert_datetime_to_string(dt:datetime):
    dt_string = datetime.strftime('%Y-%m-%d %H:%M:%S')
    return dt_string

def convert_string_to_datetime(dt_string:str):
    dt = datetime.strptime(dt_string, '%Y-%m-%d %H:%M:%S')
    return dt

    