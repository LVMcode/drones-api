from fastapi import Depends, HTTPException, status

from repositories.drone_repository import DroneRepository
from repositories.medication_repository import MedicationRepository
from models.drone_model import Drone, State as DroneState
from schemas.schema import DroneCreate, DroneUpdate


class DroneService:

    def __init__(self, drone_repository: DroneRepository = Depends(),
                 medication_repository: MedicationRepository = Depends()) -> None:
        self.drone_repository = drone_repository
        self.medication_repository = medication_repository

    def get_all(self, offset: int, limit: int, drone_state: DroneState | None = None) -> list[Drone]:
        return self.drone_repository.get_all(offset=offset, limit=limit, drone_state=drone_state)

    def get_available_for_loading(self, offset: int, limit: int) -> list[Drone]:
        available_drones: list[Drone] = []
        drones = self.drone_repository.get_all(
            offset=offset, limit=limit, drone_state=DroneState.IDLE)
        for drone in drones:
            if DroneService.check_load_capacity(drone):
                available_drones.append(drone)
        return available_drones

    def get_by_id(self, id: int) -> Drone | None:
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
        medication_ids: list[int] = drone_data["medication_ids"]
        if len(medication_ids) > 0:
            medications_weight: float = 0
            drone = self.drone_repository.get_by_id(id)
            if drone:
                for medication_id in medication_ids:
                    medication = self.medication_repository.get_by_id(
                        medication_id)
                    if medication:
                        medications_weight += medication.weight
                        if not DroneService.check_load_capacity(drone, medications_weight):
                            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                                detail=f"Total weight of medications above drone weight limit")
        return self.drone_repository.update(id, new_drone_data)

    def remove(self, id: int) -> None:
        self.drone_repository.remove(id)

    def add_medication(self, drone_id: int, medication_id: int) -> Drone | None:
        return self.drone_repository.add_medication(drone_id, medication_id)

    @staticmethod
    def check_load_capacity(drone: Drone, new_load: float = 0) -> bool:
        used_load_capacity: float = 0
        for medication in drone.medications:
            used_load_capacity += medication.weight if medication else 0
        new_used_load_capacity = used_load_capacity + new_load
        return True if new_used_load_capacity <= drone.weight_limit else False
