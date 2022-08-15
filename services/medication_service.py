from fastapi import Depends

from repositories.medication_repository import MedicationRepository
from models.medication_model import Medication
from schemas.schema import MedicationCreate, MedicationUpdate


class MedicationService:

    def __init__(self, medication_repositorty: MedicationRepository = Depends()) -> None:
        self.medication_repository = medication_repositorty

    def get_all(self, offset, limit) -> list[Medication]:
        return self.medication_repository.get_all(offset=offset, limit=limit)

    def get_by_id(self, id) -> Medication | None:
        return self.medication_repository.get_by_id(id)

    def add(self, medication: MedicationCreate):
        return self.medication_repository.add(medication)

    def update(self, id: int, new_medication_data: MedicationUpdate) -> Medication | None:
        return self.medication_repository.update(id, new_medication_data)

    def remove(self, id: int) -> None:
        self.medication_repository.remove(id)
