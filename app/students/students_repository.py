
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.pets.pets_models import PetModel  # noqa: F401
from app.shared.database import session_scope
from app.students.students_models import StudentModel
from app.students.students_schemas import Student


class StudentsRepository:
    def __init__(self, session: Session | None = None) -> None:
        self.session = session

    def find_all(self, session: Session | None = None) -> list[Student]:
        active_session = session if session is not None else self.session

        with session_scope(active_session) as db:
            statement = select(StudentModel).order_by(
                StudentModel.createdAt.desc()
            )
            models = db.scalars(statement).all()
            return [Student.model_validate(model) for model in models]

    def find_by_id(
        self, student_id: str, session: Session | None = None
    ) -> Student | None:
        active_session = session if session is not None else self.session

        with session_scope(active_session) as db:
            model = db.get(StudentModel, student_id)
            return Student.model_validate(model) if model else None

    def find_by_email(
        self, email: str, session: Session | None = None
    ) -> Student | None:
        active_session = session if session is not None else self.session

        with session_scope(active_session) as db:
            statement = select(StudentModel).where(
                StudentModel.email == email
            )
            model = db.scalars(statement).first()
            return Student.model_validate(model) if model else None

    def find_by_username(
        self, username: str, session: Session | None = None
    ) -> Student | None:
        active_session = session if session is not None else self.session

        with session_scope(active_session) as db:
            statement = select(StudentModel).where(
                StudentModel.username == username
            )
            model = db.scalars(statement).first()
            return Student.model_validate(model) if model else None

    def save(
        self, student: Student, session: Session | None = None
    ) -> Student:
        active_session = session if session is not None else self.session

        with session_scope(active_session) as db:
            model = db.get(StudentModel, student.id)

            if model is None:
                model = StudentModel(id=student.id)
                db.add(model)

            model.name = student.name
            model.username = student.username
            model.email = str(student.email)
            model.age = student.age
            model.createdAt = student.createdAt
            model.updatedAt = student.updatedAt

            db.flush()
            return Student.model_validate(model)

    def delete(
        self, student_id: str, session: Session | None = None
    ) -> None:
        active_session = session if session is not None else self.session

        with session_scope(active_session) as db:
            model = db.get(StudentModel, student_id)

            if model is not None:
                db.delete(model)
                db.flush()
students_repository = StudentsRepository()