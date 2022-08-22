from pydantic import BaseModel, Field
from fastapi import Form

from models.drone_model import Model, State


class DroneBase(BaseModel):
    serial_number: str = Field(max_length=100)
    model: Model
    weight_limit: float = Field(default=500, ge=0, le=500)
    battery_capacity: int = Field(default=100, ge=0, le=100)
    state: State

    class Config:
        orm_mode = True


class DroneCreate(DroneBase):

    class Config:
        schema_extra = {
            "example": {
                "serial_number": "DA0144",
                "model": Model.Middleweight,
                "weight_limit": 350,
                "battery_capacity": 100,
                "state": State.IDLE
            }
        }


class DroneRead(DroneCreate):
    id: int


class DroneUpdateBase(BaseModel):
    weight_limit: float | None = Field(default=None, ge=0, le=500)
    battery_capacity: int | None = Field(default=None, ge=0, le=100)
    state: State | None = None


class DroneUpdate(DroneUpdateBase):
    medication_ids: list[int] | None = None

    class Config:
        schema_extra = {
            "example": {
                "weight_limit": 400,
                "battery_capacity": 70,
                "state": State.RETURNING,
                "medication_ids": [1, 3, 18]
            }
        }


class MedicationBase(BaseModel):
    name: str = Field(regex="^[\\w_-]+$")
    weight: float = Field(ge=0)
    code: str = Field(regex="^[A-Z_0-9]+$")
    image: str | None = None

    class Config:
        orm_mode = True


class MedicationCreate(MedicationBase):

    @classmethod
    def as_form(cls,
                name: str = Form(regex="^[\\w_-]+$"),
                weight: float = Form(ge=0),
                code: str = Form(regex="^[A-Z_0-9]+$")):
        return cls(name=name, weight=weight, code=code)

    class Config:
        schema_extra = {
            "example": {
                "name": "TestMed",
                "weight": 0.5,
                "code": "AZ00_5B"
            }
        }


class MedicationRead(MedicationCreate):
    id: int

    class Config:
        schema_extra = {
            "example": {
                "name": "TestMed",
                "weight": 0.5,
                "code": "AZ00_5B",
                "image": "http://server.com/image_name.jpg",
                "id": "1"
            }
        }


class MedicationUpdate(BaseModel):
    image: str | None = None

    @classmethod
    def as_form(cls):
        return cls()


class DroneReadWithMedications(DroneRead):
    medications: list[MedicationRead] = []

    class Config:
        schema_extra = {
            "example": {
                "serial_number": "DA0144",
                "model": Model.Middleweight,
                "weight_limit": 500,
                "battery_capacity": 100,
                "state": State.IDLE,
                "medications": []
            }
        }


class MedicationReadWithDrone(MedicationRead):
    drone: DroneRead | None = None
