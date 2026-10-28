
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.shared.database import Base


class PetModel(Base):
    __tablename__ = "pets"
    __table_args__ = (
        UniqueConstraint(
            "studentId",
            "name",
            name="uq_pets_student_name",
        ),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True)

    studentId: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("students.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    name: Mapped[str] = mapped_column(String(50), nullable=False)
    species: Mapped[str] = mapped_column(String(50), nullable=False)
    age: Mapped[int | None] = mapped_column(Integer, nullable=True)

    createdAt: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    updatedAt: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )

    student: Mapped["StudentModel"] = relationship(back_populates="pets")
