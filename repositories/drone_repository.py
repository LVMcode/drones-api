from fastapi import Depends
from sqlmodel import Session, select

from configs.db import get_session
from models.drone_model import Drone
from schemas.schema import DroneCreate, DroneUpdate
from models.medication_model import Medication


class DroneRepository:

    def __init__(self, session: Session = Depends(get_session)) -> None:
        self.session = session

    def get_all(self, offset: int, limit: int) -> list[Drone]:
        return self.session.exec(select(Drone).offset(offset).limit(limit)).all()

    def get_by_id(self, id: int) -> Drone | None:
        drone = self.session.get(Drone, id)
        return drone

    def add(self, drone: DroneCreate) -> Drone:
        new_drone = Drone.from_orm(drone)
        self.session.add(new_drone)
        self.session.commit()
        self.session.refresh(new_drone)
        return new_drone

    def update(self, id: int, new_drone_data: DroneUpdate) -> Drone | None:
        drone = self.session.get(Drone, id)
        if drone:
            drone_data = new_drone_data.dict(exclude_unset=True)
            for key, value in drone_data.items():
                setattr(drone, key, value)
            self.session.add(drone)
            self.session.commit()
            self.session.refresh(drone)

        return drone

    def remove(self, id: int) -> None:
        drone = self.session.get(Drone, id)
        if drone:
            self.session.delete(drone)
            self.session.commit()

    def add_medication(self, drone_id: int, medication_id: int) -> Drone | None:
        drone = self.get_by_id(drone_id)
        medication = self.session.get(Medication, medication_id)
        if drone and medication:
            drone.medications.append(medication)
            self.session.add(drone)
            self.session.commit()
            self.session.refresh(drone)
            return drone
