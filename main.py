from fastapi import FastAPI
import uvicorn
from sqlmodel import SQLModel, Session, select
from fastapi_utils.tasks import repeat_every

from models.drone_model import Drone
from models.medication_model import Medication
from configs import db, loggers, dirs
from routers.v1 import drone_router as v1_drone_router, medication_router as v1_medication_router


app = FastAPI()
app.include_router(v1_drone_router.router)
app.include_router(v1_medication_router.router)


@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(db.engine)
    dirs.create_paths()


logger = loggers.get_battery_level_logger()


@app.on_event("startup")
@repeat_every(seconds=60*60)
def check_db():
    pretty_drones = []
    with Session(db.engine) as session:
        drones = session.exec(
            select(Drone.serial_number, Drone.battery_capacity))
        for dron in drones:
            pretty_drones.append(
                (f"SERIAL: {dron[0]} BATTERY LEVEL: {dron[1]}%"))
    logger.info(pretty_drones)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, port=8000)
