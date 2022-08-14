from sqlmodel import Field, Relationship, SQLModel
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .drone_model import Drone


class Medication(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    weight: float
    code: str
    image: str

    drone_id: int = Field(foreign_key="drone.id")
    drone: "Drone" = Relationship(back_populates="medications")
