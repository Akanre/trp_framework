# backend/app/models.py
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from .database import Base
from sqlalchemy.types import TypeDecorator
import datetime

class NaiveDateTime(TypeDecorator):
    impl = DateTime
    cache_ok = True

    def process_bind_param(self, value, dialect):
        if value is not None and value.tzinfo is not None:
            raise ValueError('NaiveDateTime cannot store timezone-aware datetimes')
        return value

    def process_result_value(self, value, dialect):
        return value

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    full_name = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    role = Column(Integer, default=1)  # 1-Инженер, 2-Менеджер, 3-Руководитель
    created_at = Column(NaiveDateTime, default=datetime.datetime.utcnow)

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, nullable=True)
    status = Column(String, default="active")  # active, completed, cancelled
    created_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(NaiveDateTime, default=datetime.datetime.utcnow)
    
    creator = relationship("User")

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, nullable=True)
    status = Column(String, default="todo")  # todo, in_progress, done
    priority = Column(String, default="medium")  # low, medium, high
    project_id = Column(Integer, ForeignKey("projects.id"))
    assigned_to = Column(Integer, ForeignKey("users.id"))
    created_by = Column(Integer, ForeignKey("users.id"))
    due_date = Column(NaiveDateTime, nullable=True)
    created_at = Column(NaiveDateTime, default=datetime.datetime.utcnow)
    
    project = relationship("Project")
    assignee = relationship("User", foreign_keys=[assigned_to])
    author = relationship("User", foreign_keys=[created_by])