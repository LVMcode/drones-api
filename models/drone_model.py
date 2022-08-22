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
    serial_number: str = Field(max_length=100)
    model: Model
    weight_limit: float = Field(default=500, ge=0, le=500)
    battery_capacity: int = Field(default=100, ge=0, le=100)
    state: State

    medications: list["Medication"] = Relationship(back_populates="drone")
