# backend/app/main.py
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import timedelta
from typing import List

from .database import SessionLocal, engine, get_db
from .models import Base
from .schemas import User, UserCreate, UserLogin, Token, Project, ProjectCreate, Task, TaskCreate
from .auth import authenticate_user, create_access_token, get_current_active_user, get_password_hash
from .crud import create_user, get_user_by_username, get_user_by_email, create_project, create_task, get_projects, get_tasks

# Создаем таблицы
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Business Manager API", version="1.0.0")

# CORS для порта 4001
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4001", "http://127.0.0.1:4001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Auth routes
@app.post("/auth/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return create_user(db=db, user=user)

@app.post("/auth/login")
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    user = authenticate_user(db, user_data.username, user_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    # Добавляем имя роли в ответ
    from .schemas import get_role_name
    user_dict = {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "full_name": user.full_name,
        "role": user.role,
        "role_name": get_role_name(user.role),
        "is_active": user.is_active,
        "is_admin": user.is_admin,
        "created_at": user.created_at.isoformat() if user.created_at else None
    }
    
    return {"access_token": access_token, "token_type": "bearer", "user": user_dict}

# User routes
@app.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    from .schemas import get_role_name
    user_dict = {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "full_name": current_user.full_name,
        "role": current_user.role,
        "role_name": get_role_name(current_user.role),
        "is_active": current_user.is_active,
        "is_admin": current_user.is_admin,
        "created_at": current_user.created_at.isoformat() if current_user.created_at else None
    }
    return user_dict

# Project routes
@app.post("/projects/")
def create_new_project(
    project: ProjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    return create_project(db=db, project=project, user_id=current_user.id)

@app.get("/projects/")
def read_projects(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    projects = get_projects(db, skip=skip, limit=limit)
    return projects

# Task routes
@app.post("/tasks/")
def create_new_task(
    task: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    return create_task(db=db, task=task, user_id=current_user.id)

@app.get("/tasks/")
def read_tasks(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    tasks = get_tasks(db, skip=skip, limit=limit)
    return tasks

@app.get("/")
def read_root():
    return {"message": "Business Manager API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)