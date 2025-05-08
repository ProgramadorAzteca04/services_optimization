from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from router import router
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi import Request
import uvicorn
from app.utilities.utils import program_daily_jobs, programming_hour
import threading
import schedule
import time

app = FastAPI()

app.include_router(router)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors(), "body": exc.body},
    )


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def run_scheduled_tasks():
    while True:
        schedule.run_pending()
        time.sleep(60)


if __name__ == "__main__":
    program_daily_jobs(programming_hour)

    programmed_job = threading.Thread(
        target=run_scheduled_tasks, name="SchedulerThread", daemon=True
    )
    programmed_job.start()
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
