# backend/app/schemas.py
from pydantic import BaseModel, EmailStr, validator
from datetime import datetime
from typing import Optional, List

def get_role_name(role_id: int) -> str:
    roles = {
        1: 'Инженер',
        2: 'Менеджер', 
        3: 'Руководитель'
    }
    return roles.get(role_id, 'Неизвестная роль')

# User schemas
class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None
    role: Optional[int] = 1

class UserCreate(UserBase):
    password: str

    @validator('password')
    def validate_password(cls, v):
        if len(v) < 6:
            raise ValueError('Пароль должен быть не менее 6 символов')
        return v

class UserLogin(BaseModel):
    username: str
    password: str

class User(UserBase):
    id: int
    is_active: bool
    is_admin: bool
    role_name: str
    created_at: datetime

    class Config:
        from_attributes = True

# Project schemas
class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None
    status: str = "active"

class ProjectCreate(ProjectBase):
    pass

class Project(ProjectBase):
    id: int
    created_by: int
    created_at: datetime
    creator: Optional[User] = None

    class Config:
        from_attributes = True

# Task schemas
class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: str = "todo"
    priority: str = "medium"
    due_date: Optional[datetime] = None

class TaskCreate(TaskBase):
    project_id: int
    assigned_to: Optional[int] = None

class Task(TaskBase):
    id: int
    project_id: int
    assigned_to: Optional[int]
    created_by: int
    created_at: datetime
    project: Optional[Project] = None
    assignee: Optional[User] = None
    author: Optional[User] = None

    class Config:
        from_attributes = True

# Token schemas
class Token(BaseModel):
    access_token: str
    token_type: str
    user: User

class TokenData(BaseModel):
    username: Optional[str] = None