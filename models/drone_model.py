from sqlmodel import Field, Relationship, SQLModel
from enum import Enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .medication_model import Medication


class Model(str, Enum):
    Lightweight = "Lightweight"
    Middleweight = "Middleweight"
    Cruiserweight = "Cruiserweight"
    Heavyweight = "Heavyweight"


class State(str, Enum):
    IDLE = "IDLE"
    LOADING = "LOADING"
    LOADED = "LOADED"
    DELIVERING = "DELIVERING"
    DELIVERED = "DELIVERED"
    RETURNING = "RETURNING"


class Drone(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    serial_number: str
    model: Model
    weight_limit: float = 500
    battery_capacity: int
    state: State

    medications: list["Medication"] = Relationship(back_populates="drone")
