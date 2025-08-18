from sqlalchemy import Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.dao.database import Base


class Task(Base):
    __tablename__ = 'tasks'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    description: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[bool] = mapped_column(String, nullable='None')

    user_id: Mapped[str] = mapped_column(ForeignKey('user.id'))
    user: Mapped["User"] = relationship(back_populates="tasks")

    def __str__(self):
        return f"Task(id={self.id}, title={self.title}, description={self.description}, status={self.status})"

    def __repr__(self):
        return self.__str__()