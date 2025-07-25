from app.dao.base import BaseDAO
from app.tasks.models import Task


class TasksDAO(BaseDAO):
    model = Task
