
from datetime import datetime

from sqlalchemy import DateTime, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.shared.database import Base


class StudentModel(Base):
    __tablename__ = "students"
    __table_args__ = (
        UniqueConstraint("email", name="uq_students_email"),
        UniqueConstraint("username", name="uq_students_username"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    username: Mapped[str] = mapped_column(String(30), nullable=False)
    email: Mapped[str] = mapped_column(String(254), nullable=False)
    age: Mapped[int] = mapped_column(Integer, nullable=False)

    createdAt: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    updatedAt: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )

    pets: Mapped[list["PetModel"]] = relationship(
        back_populates="student",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
