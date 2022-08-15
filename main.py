from fastapi import FastAPI
import uvicorn
from sqlmodel import SQLModel

from models.drone_model import Drone
from models.medication_model import Medication
from configs.db import engine
from routers.v1 import drone_router, medication_router


app = FastAPI()
app.include_router(drone_router.router)
app.include_router(medication_router.router)


@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, port=8000)
