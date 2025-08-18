from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.dao.database import Base


class User(Base):
    __tablename__ = 'users'
    id: Mapped[UUID] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True)
    email_verified: Mapped[bool]
    name: Mapped[str]
    preferred_username: Mapped[str]
    given_name: Mapped[str]
    family_name: Mapped[str]
    tasks: Mapped[list["Task"]] = relationship(back_populates="user")
