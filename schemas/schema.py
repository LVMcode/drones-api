from pydantic import BaseModel

from models.drone_model import Model, State


class DroneBase(BaseModel):
    serial_number: str
    model: Model
    weight_limit: float = 500
    battery_capacity: int
    state: State

    class Config:
        orm_mode = True


class DroneCreate(DroneBase):

    class Config:
        schema_extra = {
            "example": {
                "serial_number": "DA0144",
                "model": Model.Middleweight,
                "weight_limit": 500,
                "battery_capacity": 100,
                "state": State.IDLE
            }
        }


class DroneRead(DroneCreate):
    id: int


class DroneUpdate(BaseModel):
    weight_limit: float | None = None
    battery_capacity: int | None = None
    state: State | None = None

    class Config:
        schema_extra = {
            "example": {
                "weight_limit": 400,
                "battery_capacity": 70,
                "state": State.RETURNING
            }
        }


class MedicationBase(BaseModel):
    name: str
    weight: float
    code: str
    image: str | None

    class Config:
        orm_mode = True


class MedicationCreate(MedicationBase):

    class Config:
        schema_extra = {
            "example": {
                "name": "TestMed",
                "weight": 0.5,
                "code": "AZ00_5B",
                "image": None
            }
        }


class MedicationRead(MedicationCreate):
    id: int


class MedicationUpdate(BaseModel):
    image: str | None = None


class DroneReadWithMedications(DroneRead):
    medications: list[MedicationRead] = []


class MedicationReadWithDrone(MedicationRead):
    drone: DroneRead | None = None
