from fastapi import Depends, HTTPException, APIRouter, Query, Path, Body, status, UploadFile, File

from services.medication_service import MedicationService
from schemas.schema import MedicationCreate, MedicationRead, MedicationReadWithDrone, MedicationUpdate
from models.medication_model import Medication


router = APIRouter(prefix="/api/v1/medications", tags=["medication"])


@router.get("/", response_model=list[MedicationReadWithDrone])
def get_medications(offset: int = 0,
                    limit: int = Query(default=100, le=100),
                    medication_service: MedicationService = Depends()) -> list[Medication]:
    return medication_service.get_all(offset=offset, limit=limit)


@router.get("/{medication_id}", response_model=MedicationReadWithDrone)
def get_medication_by_id(medication_id: int,
                         medication_service: MedicationService = Depends()) -> Medication | None:
    medication = medication_service.get_by_id(medication_id)
    if not medication:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Medication with id {medication_id} not found")
    return medication


@router.post("/", response_model=MedicationRead, status_code=status.HTTP_201_CREATED)
async def add_medication(medication: MedicationCreate = Depends(MedicationCreate.as_form),
                         img_file: UploadFile | None = File(default=None),
                         medication_service: MedicationService = Depends()) -> Medication:
    return await medication_service.add(medication, img_file)


@router.patch("/{medication_id}", response_model=MedicationReadWithDrone)
async def update_medication(medication_id: int,
                            new_medication_data: MedicationUpdate = Depends(
                                MedicationUpdate.as_form),
                            img_file: UploadFile | None = File(default=None),
                            medication_service: MedicationService = Depends()) -> Medication | None:
    medication = medication_service.get_by_id(medication_id)
    if not medication:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Medication with id {medication_id} not found")
    return await medication_service.update(medication_id, new_medication_data, img_file)


@router.delete("/{medication_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_medication(medication_id: int,
                      medication_service: MedicationService = Depends()) -> dict:
    medication = medication_service.get_by_id(medication_id)
    if medication:
        medication_service.remove(medication_id)
        return {"ok": True}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Medication with id {medication_id} not found")
