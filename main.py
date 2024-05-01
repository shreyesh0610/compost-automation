import os
import sys

from utils import *
from helper import *

app = FastAPI(title='Compost Automation')

class BackgroundTasks(threading.Thread):
    def run(self,*args,**kwargs):
        while True:
            BackgroundProcess()
            killer.crash_it()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

@app.exception_handler(Exception)
def exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=exc.status_code if hasattr(exc, 'status_code') else 500,
        content={'message': 'Error', 'detail': str(exc)},
    )

@app.get("/data/sensor", status_code=200)
async def get_sensor_data(process_id:str, only_one:bool=True):
    try:
        if not MOCK_API:
            return {
                'process_id': process_id,
                'results': [sD.convert_to_dict() for sD in databaseHelper.GetSensorData(process_id=process_id, only_one=only_one)]
            }
        else:
            return {
                'process_id': process_id,
                'results' : [SensorData(
                    process_id = process_id,
                    humidity = random.uniform(1.0,100.0),
                    temperature = random.uniform(1.0,100.0),
                    ec = random.uniform(1.0,100.0),
                    ph = random.uniform(1.0,100.0),
                    nitrogen = random.uniform(1.0,100.0),
                    phosphorus = random.uniform(1.0,100.0),
                    potassium = random.uniform(1.0,100.0),
                    timestamp = datetime.now()
                ).convert_to_dict() for _ in range(random.randint(1,10))]
            }
    except Exception as ex: raise HTTPException(500, ex)

@app.get("/data/history", status_code=200)
async def get_sensor_history():
    return_list = []
    try:
        if not MOCK_API:

            process_id_list = databaseHelper.GetCollectProcessIDs()
            for process_id in process_id_list:

                sensorDataList:List[SensorData] = databaseHelper.GetSensorData(process_id=process_id, only_one=True)
                sensorData = sensorDataList[0] if sensorDataList else None

                if sensorData:
                    return_list.append({
                        'process_id': process_id,
                        'result': sensorData.convert_to_dict()
                    })
                else:
                    return_list.append({
                        'process_id': process_id,
                        'result': None
                    })
            return {
                'results': return_list
            }
        else:
            return {
                'results': [
                    {
                        'process_id': process_id,
                        'result' : SensorData(
                            process_id = process_id,
                            humidity = random.uniform(1.0,100.0),
                            temperature = random.uniform(1.0,100.0),
                            ec = random.uniform(1.0,100.0),
                            ph = random.uniform(1.0,100.0),
                            nitrogen = random.uniform(1.0,100.0),
                            phosphorus = random.uniform(1.0,100.0),
                            potassium = random.uniform(1.0,100.0),
                            timestamp = datetime.now()
                        )
                    }
                ]
            }
    except Exception as ex: raise HTTPException(500, ex)

@app.post("/start", status_code=200)
def start_process(is_mature_process:bool=False):
    try:
        if not MOCK_API:
            return {
                'process_id': StartNewProcess(is_mature_process),
                'message': 'Process Started'
            }
        else:
            return {
                'process_id' : create_process_id(),
                'message': 'Process Started'
            }
    except Exception as ex: raise HTTPException(500, ex)

@app.post("/stop", status_code=200)
def stop_process(process_id:str):
    try:
        if not MOCK_API:
            return {
                'process_id': StopProcess(process_id),
                'message': 'Process Stopped'
            }
        else:
            return {
                'process_id' : create_process_id(),
                'message': 'Process Stopped'
            }
    except Exception as ex: raise HTTPException(500, ex)

@app.post("/collect", status_code=200)
def collect_process(process_id:str):
    try:
        if not MOCK_API:
            return {
                'process_id': CollectProcess(process_id),
                'message': 'Process Collected/Saved'
            }
        else:
            return {
                'process_id' : process_id,
                'message': 'Process Collected/Saved'
            }
    except Exception as ex: raise HTTPException(500, ex)

@app.get("/data/process", status_code=200)
async def get_process_data(process_id:str):
    try:
        if not MOCK_API:
            processData:ProcessData = databaseHelper.GetProcessData(process_id = process_id)
            return {
                'process_id': process_id,
                'result': processData.convert_to_dict() if processData else {}
            }
        else:
            return {
                'process_id': process_id,
                'result' : ProcessData(
                    process_id = 'random_process_id',
                    start_time = datetime.now() - timedelta(hours=2),
                    end_time = datetime.now(),
                    current_phase = 'Phase 1',
                    mature_percentage = 67.5,
                    mature_result = 'Immature',
                    is_mature_process = False
                ).convert_to_dict()
            }
    except Exception as ex: raise HTTPException(500, ex)

@app.get("/current_process", status_code=200)
async def get_current_process_id():
    try:
        if not MOCK_API: return {'process_id': GetCurrentProcessID()}
        else: return {'process_id': create_process_id()}

    except Exception as ex: raise HTTPException(500, ex)


if __name__ == '__main__':
    bgTask = BackgroundTasks()
    bgTask.start()
    uvicorn.run(app, host="0.0.0.0", port=3000)
