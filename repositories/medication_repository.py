from fastapi import Depends
from sqlmodel import Session, select

from configs.db import get_session
from models.medication_model import Medication
from schemas.schema import MedicationCreate, MedicationUpdate


class MedicationRepository:

    def __init__(self, session: Session = Depends(get_session)) -> None:
        self.session = session

    def get_all(self, offset: int, limit: int) -> list[Medication]:
        return self.session.exec(select(Medication).offset(offset).limit(limit)).all()

    def get_by_id(self, id: int) -> Medication | None:
        medication = self.session.get(Medication, id)
        return medication

    def add(self, medication: MedicationCreate) -> Medication:
        new_medication = Medication.from_orm(medication)
        self.session.add(new_medication)
        self.session.commit()
        self.session.refresh(new_medication)
        return new_medication

    def update(self, id: int, new_medication_data: MedicationUpdate) -> Medication | None:
        medication = self.session.get(Medication, id)
        if medication:
            medication_data = new_medication_data.dict(exclude_unset=True)
            medication_data.update(
                {"image": new_medication_data.dict()["image"]})
            for key, value in medication_data.items():
                setattr(medication, key, value)
            self.session.add(medication)
            self.session.commit()
            self.session.refresh(medication)

        return medication

    def remove(self, id: int) -> None:
        medication = self.session.get(Medication, id)
        if medication:
            self.session.delete(medication)
            self.session.commit()
