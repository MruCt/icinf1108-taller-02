
from uuid import uuid4

import pytest
from sqlalchemy import func, select

from app.pets.pets_models import PetModel
from app.shared.database import SessionLocal
from app.shared.datetimes import utc_now
from app.students.students_models import StudentModel


def test_rollback_elimina_estudiante_y_mascota():
    student_id = str(uuid4())
    pet_id = str(uuid4())
    now = utc_now()

    # Estos nombres e identificadores son exclusivos de esta prueba.
    student = StudentModel(
        id=student_id,
        name="Estudiante Prueba Rollback",
        username=f"rollback_{uuid4().hex[:12]}",
        email=f"rollback_{uuid4().hex}@example.com",
        age=20,
        createdAt=now,
        updatedAt=now,
    )

    pet = PetModel(
        id=pet_id,
        studentId=student_id,
        name="Mascota Prueba Rollback",
        species="Perro",
        age=3,
        createdAt=now,
        updatedAt=now,
    )

    # La excepción fuerza el rollback de la transacción.
    with pytest.raises(RuntimeError, match="Forzar rollback"):
        with SessionLocal.begin() as session:
            session.add(student)
            session.flush()

            session.add(pet)
            session.flush()

            raise RuntimeError("Forzar rollback")

    # Comprobar que ninguno de los registros quedó guardado.
    with SessionLocal() as session:
        student_count = session.scalar(
            select(func.count())
            .select_from(StudentModel)
            .where(StudentModel.id == student_id)
        )
        pet_count = session.scalar(
            select(func.count())
            .select_from(PetModel)
            .where(PetModel.id == pet_id)
        )

    assert student_count == 0
    assert pet_count == 0
