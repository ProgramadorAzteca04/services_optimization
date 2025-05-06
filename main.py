from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi import Request
import schedule
import time




app = FastAPI()

app.include_router()

app.exception_handler = (RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors(), "body": exc.body},
    )


origin = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origin,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def run_scheduled_task():
    while True:
        schedule.run_pending()
        time.sleep(60)  # Espera un minuto entre cada verificación de tareas programadas


if __name__ == "__main__":
   """Ejecuta la aplicacion FastAPI en el puerto 8000 y habilita el modo de recarga automatica."""
   print("Ejecutando FastAPI en el puerto 8000")


