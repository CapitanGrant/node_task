from typing import Optional

from pydantic import BaseModel, Field
from enum import Enum
from datetime import datetime


class STaskStatus(str, Enum):
    pending = "pending"
    in_progress = "in_progress"
    done = "done"


class TaskFilter(BaseModel):
    status: Optional[STaskStatus] = None


class STaskBase(BaseModel):
    title: str = Field(..., description="Заголовок задачи")
    description: str = Field(None, description="Описание задачи")
    status: STaskStatus = Field(STaskStatus.pending, description="Статус задачи")


class STaskCreate(STaskBase):
    pass


class STaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    status: STaskStatus | None = None


class STaskID(BaseModel):
    id: int = Field(..., description="ID задачи")


class STaskOut(STaskBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
