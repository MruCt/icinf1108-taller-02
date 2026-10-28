
from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from app.pets.pets_models import PetModel
from app.pets.pets_schemas import Pet
from app.shared.database import session_scope
from app.students.students_models import StudentModel  # noqa: F401


class PetsRepository:
    def __init__(self, session: Session | None = None) -> None:
        self.session = session

    def find_all_by_student(
        self, student_id: str, session: Session | None = None
    ) -> list[Pet]:
        active_session = session if session is not None else self.session

        with session_scope(active_session) as db:
            statement = (
                select(PetModel)
                .where(PetModel.studentId == student_id)
                .order_by(PetModel.createdAt.desc())
            )
            models = db.scalars(statement).all()
            return [Pet.model_validate(model) for model in models]

    def find_by_id(
        self, pet_id: str, session: Session | None = None
    ) -> Pet | None:
        active_session = session if session is not None else self.session

        with session_scope(active_session) as db:
            model = db.get(PetModel, pet_id)
            return Pet.model_validate(model) if model else None

    def find_by_student_and_name(
        self,
        student_id: str,
        name: str,
        session: Session | None = None,
    ) -> Pet | None:
        active_session = session if session is not None else self.session

        with session_scope(active_session) as db:
            statement = select(PetModel).where(
                PetModel.studentId == student_id,
                PetModel.name == name,
            )
            model = db.scalars(statement).first()
            return Pet.model_validate(model) if model else None

    def save(
        self, pet: Pet, session: Session | None = None
    ) -> Pet:
        active_session = session if session is not None else self.session

        with session_scope(active_session) as db:
            model = db.get(PetModel, pet.id)

            if model is None:
                model = PetModel(id=pet.id)
                db.add(model)

            model.studentId = pet.studentId
            model.name = pet.name
            model.species = pet.species
            model.age = pet.age
            model.createdAt = pet.createdAt
            model.updatedAt = pet.updatedAt

            db.flush()
            return Pet.model_validate(model)

    def delete(
        self, pet_id: str, session: Session | None = None
    ) -> None:
        active_session = session if session is not None else self.session

        with session_scope(active_session) as db:
            model = db.get(PetModel, pet_id)

            if model is not None:
                db.delete(model)
                db.flush()

    def delete_by_student(
        self, student_id: str, session: Session | None = None
    ) -> None:
        active_session = session if session is not None else self.session

        with session_scope(active_session) as db:
            statement = delete(PetModel).where(
                PetModel.studentId == student_id
            )
            db.execute(statement)
            db.flush()
pets_repository = PetsRepository()