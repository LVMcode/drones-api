from sqlmodel import Field, Relationship, SQLModel
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .drone_model import Drone


class Medication(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(regex="^[\\w_-]+$")
    weight: float = Field(ge=0)
    code: str = Field(regex="^[A-Z_0-9]+$")
    image: str | None

    drone_id: int | None = Field(default=None, foreign_key="drone.id")
    drone: "Drone" = Relationship(back_populates="medications")
