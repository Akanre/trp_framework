# backend/app/crud.py
from sqlalchemy.orm import Session
from .models import User, Project, Task
from .schemas import UserCreate, ProjectCreate, TaskCreate
from .auth import get_password_hash

def create_user(db: Session, user: UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        full_name=user.full_name,
        role=user.role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_project(db: Session, project: ProjectCreate, user_id: int):
    db_project = Project(**project.dict(), created_by=user_id)
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project

def create_task(db: Session, task: TaskCreate, user_id: int):
    db_task = Task(**task.dict(), created_by=user_id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def get_projects(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Project).offset(skip).limit(limit).all()

def get_tasks(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Task).offset(skip).limit(limit).all()