from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional

from .database import Base, engine, get_db
from . import schemas, crud
from .auth import require_roles

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Finance Data Processing and Access Control Backend")


@app.get("/")
def root():
    return {"message": "Finance backend is running"}


@app.post("/users", response_model=schemas.UserResponse, status_code=201)
def create_user(
    user: schemas.UserCreate,
    db: Session = Depends(get_db),
    role: str = Depends(require_roles(["admin"]))
):
    existing_user = crud.get_user_by_email(db, user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already exists")
    return crud.create_user(db, user)


@app.get("/users", response_model=list[schemas.UserResponse])
def list_users(
    db: Session = Depends(get_db),
    role: str = Depends(require_roles(["admin"]))
):
    return crud.get_users(db)


@app.post("/records", response_model=schemas.RecordResponse, status_code=201)
def create_record(
    record: schemas.RecordCreate,
    db: Session = Depends(get_db),
    role: str = Depends(require_roles(["admin"]))
):
    user = crud.get_user_by_id(db, record.created_by)
    if not user:
        raise HTTPException(status_code=404, detail="Creator user not found")
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user cannot create records")
    return crud.create_record(db, record)


@app.get("/records", response_model=list[schemas.RecordResponse])
def list_records(
    type: Optional[str] = None,
    category: Optional[str] = None,
    db: Session = Depends(get_db),
    role: str = Depends(require_roles(["admin", "analyst"]))
):
    return crud.get_records(db, type=type, category=category)


@app.get("/dashboard/summary")
def dashboard_summary(
    db: Session = Depends(get_db),
    role: str = Depends(require_roles(["admin", "analyst", "viewer"]))
):
    return crud.get_dashboard_summary(db)