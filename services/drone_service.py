from fastapi import Depends

from repositories.drone_repository import DroneRepository
from models.drone_model import Drone
from schemas.schema import DroneCreate, DroneUpdate


class DroneService:

    def __init__(self, drone_repository: DroneRepository = Depends()) -> None:
        self.drone_repository = drone_repository

    def get_all(self, offset, limit) -> list[Drone]:
        return self.drone_repository.get_all(offset=offset, limit=limit)

    def get_by_id(self, id) -> Drone | None:
        return self.drone_repository.get_by_id(id)

    def add(self, drone: DroneCreate):
        return self.drone_repository.add(drone)

    def update(self, id: int, new_drone_data: DroneUpdate) -> Drone | None:
        return self.drone_repository.update(id, new_drone_data)

    def remove(self, id: int) -> None:
        self.drone_repository.remove(id)
