from pydantic import BaseModel


class SUserId(BaseModel):
    user_id: str

class AddUser(BaseModel):
    id: str
    email: str
    email_verified: bool
    name: str
    preferred_username: str
    given_name: str
    family_name: str


class AddTask(BaseModel):
    id: str
    task_name: str

class AddTaskWithUserId(AddTask, SUserId):
    pass

