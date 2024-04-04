import sys
import os
from os.path import dirname
sys.path.append(os.path.abspath(os.path.join(dirname(__file__), os.pardir)))

from typing import List,Dict

CURRENT_DIRECTORY = os.getenv("CURRENT_DIRECTORY", f"{os.getcwd()}")
DEBUGGING = True if os.getenv('DEBUGGING') and str(os.getenv('DEBUGGING')).upper() == 'TRUE' else False
MOCK_API = True if os.getenv('MOCK_API') and str(os.getenv('MOCK_API')).upper() == 'TRUE' else False

DATABASE_PATH = os.getenv('DATABASE_PATH', f'{CURRENT_DIRECTORY}/compost.db')