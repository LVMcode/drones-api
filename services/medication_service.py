from fastapi import Depends, UploadFile, HTTPException, status
import os
import uuid

from repositories.medication_repository import MedicationRepository
from models.medication_model import Medication
from schemas.schema import MedicationCreate, MedicationUpdate
from utils import size_converters
from configs import dirs


class MedicationService:

    def __init__(self, medication_repositorty: MedicationRepository = Depends()) -> None:
        self.medication_repository = medication_repositorty

    def get_all(self, offset, limit) -> list[Medication]:
        return self.medication_repository.get_all(offset=offset, limit=limit)

    def get_by_id(self, id) -> Medication | None:
        return self.medication_repository.get_by_id(id)

    async def add(self, medication: MedicationCreate, img_file: UploadFile | None):
        if img_file:
            if img_file.content_type not in ['image/jpeg', 'image/png']:
                raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                                    detail="Only .jpeg or .png  files allowed")
            img_dir = dirs.MEDICATION_IMAGES_PATH
            ext = os.path.splitext(img_file.filename)
            content = await img_file.read()
            img_file_size = len(content)
            img_file_size_limit = 3
            if size_converters.file_size_convert_to(img_file_size, size_converters.FileSizeUnit.MB) > img_file_size_limit:
                raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                                    detail=f"Only images files of {img_file_size_limit} MB or less are allowed")
            filename = f"{uuid.uuid4().hex}{ext[-1]}"
            with open(os.path.join(img_dir, filename), mode='wb') as f:
                f.write(content)
            medication.image = f"http://127.0.0.1:8000/{img_dir}/{filename}"
        return self.medication_repository.add(medication)

    async def update(self, id: int, new_medication_data: MedicationUpdate, img_file: UploadFile | None) -> Medication | None:
        img_dir = dirs.MEDICATION_IMAGES_PATH
        img_file_size_limit = 3
        medication = self.get_by_id(id)
        if medication:
            old_img_file_path = os.path.join(
                img_dir, medication.image.split("/")[-1]) if medication.image else None
            if img_file:
                if img_file.content_type not in ['image/jpeg', 'image/png']:
                    raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                                        detail="Only .jpeg or .png  files allowed")
                ext = os.path.splitext(img_file.filename)
                content = await img_file.read()
                img_file_size = len(content)
                if size_converters.file_size_convert_to(img_file_size, size_converters.FileSizeUnit.MB) > img_file_size_limit:
                    raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                                        detail=f"Only images files of {img_file_size_limit} MB or less are allowed")
                MedicationService.remove_file(old_img_file_path)
                filename = f"{uuid.uuid4().hex}{ext[-1]}"
                with open(os.path.join(img_dir, filename), mode='wb') as f:
                    f.write(content)
                new_medication_data.image = f"http://127.0.0.1:8000/{img_dir}/{filename}"
            MedicationService.remove_file(old_img_file_path)
        return self.medication_repository.update(id, new_medication_data)

    def remove(self, id: int) -> None:
        medication = self.get_by_id(id)
        if medication:
            img_dir = dirs.MEDICATION_IMAGES_PATH
            old_img_file_path = os.path.join(
                img_dir, medication.image.split("/")[-1]) if medication.image else None
            MedicationService.remove_file(old_img_file_path)
        self.medication_repository.remove(id)

    @staticmethod
    def remove_file(file_path: str | None) -> None:
        if file_path and os.path.exists(file_path):
            os.remove(file_path)
