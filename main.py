from utils import *

app = FastAPI(title='Compost Automation')


class BackgroundTasks(threading.Thread):
    def run(self,*args,**kwargs):
        pass
        # if SCRIPT_NAME != 'manager': 
        #     from process import poppy
        #     poppy([p.strip() for p in PROCESS_FEED_IDS.split(",") if p.strip()])
        #     killer.crash_it()

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

@app.get("/sensor_data/", status_code=200, tags=[FastAPITag.UI])
async def get_feed_data(process_id:str):
    try: 

    except Exception as ex: raise HTTPException(500, ex)

@app.post("/start", status_code=200, tags=[FastAPITag.UI])
def toggle_count():
    try:
        success = FeedManager.UpdateCount(feed_id, requestToggle)
        if success: return {"message": "Update Count - Success"}
        else: return {"message": "Update Count - Failed"}

    except Exception as ex: raise HTTPException(500, ex)


if __name__ == '__main__':
    bgTask = BackgroundTasks()
    bgTask.start()
    uvicorn.run(app, host="0.0.0.0", port=3000)
