from fastapi import Depends, HTTPException, status

from repositories.drone_repository import DroneRepository
from models.drone_model import Drone, State as DroneState
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
        drone_data = new_drone_data.dict()
        new_state = drone_data["state"]
        if new_state == DroneState.LOADING:
            drone = self.drone_repository.get_by_id(id)
            if drone and drone.battery_capacity < 25:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail=f"Drone battery level below 25%")
        return self.drone_repository.update(id, new_drone_data)

    def remove(self, id: int) -> None:
        self.drone_repository.remove(id)

    def add_medication(self, drone_id: int, medication_id: int) -> Drone | None:
        return self.drone_repository.add_medication(drone_id, medication_id)
