from fastapi import Depends, HTTPException, APIRouter, Query, Path, Body, status

from services.drone_service import DroneService
from schemas.schema import DroneCreate, DroneRead, DroneReadWithMedications, DroneUpdate
from models.drone_model import Drone, State as DroneState


router = APIRouter(prefix="/api/drones", tags=["drone"])


@router.get("/", response_model=list[DroneRead])
def get_drones(offset: int = 0,
               limit: int = Query(default=100, le=100),
               drone_state: DroneState | None = None,
               drone_service: DroneService = Depends()) -> list[Drone]:
    return drone_service.get_all(offset=offset, limit=limit, drone_state=drone_state)


@router.get("/availableForLoading", response_model=list[DroneRead])
def get_available_drones_for_loading(offset: int = 0,
                                     limit: int = Query(default=100, le=100),
                                     drone_service: DroneService = Depends()) -> list[Drone]:
    return drone_service.get_available_for_loading(offset=offset, limit=limit)


@router.get("/{drone_id}", response_model=DroneReadWithMedications)
def get_drone_by_id(drone_id: int,
                    drone_service: DroneService = Depends()) -> Drone | None:
    drone = drone_service.get_by_id(drone_id)
    if not drone:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Drone with id {drone_id} not found")
    return drone


@router.post("/", response_model=DroneRead, status_code=status.HTTP_201_CREATED)
def add_drone(drone: DroneCreate,
              drone_service: DroneService = Depends()) -> Drone:
    return drone_service.add(drone)


@router.patch("/{drone_id}", response_model=DroneReadWithMedications)
def update_drone(drone_id: int,
                 new_drone_data: DroneUpdate,
                 drone_service: DroneService = Depends()) -> Drone | None:
    drone = drone_service.get_by_id(drone_id)
    if not drone:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Drone with id {drone_id} not found")
    return drone_service.update(drone_id, new_drone_data)


@router.delete("/{drone_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_drone(drone_id: int,
                 drone_service: DroneService = Depends()) -> dict:
    drone = drone_service.get_by_id(drone_id)
    if drone:
        drone_service.remove(drone_id)
        return {"ok": True}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Drone with id {drone_id} not found")
