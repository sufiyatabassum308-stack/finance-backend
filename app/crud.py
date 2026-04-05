from sqlalchemy.orm import Session
from sqlalchemy import func
from . import models, schemas


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(name=user.name, email=user.email, role=user.role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_users(db: Session):
    return db.query(models.User).all()


def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def update_user(db: Session, user_id: int, user_update: schemas.UserUpdate):
    db_user = get_user_by_id(db, user_id)
    if not db_user:
        return None
    update_data = user_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_record(db: Session, record: schemas.RecordCreate):
    db_record = models.FinancialRecord(
        amount=record.amount,
        type=record.type,
        category=record.category,
        date=record.date,
        note=record.note,
        created_by=record.created_by
    )
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record


def get_records(db: Session, type: str = None, category: str = None):
    query = db.query(models.FinancialRecord)
    if type:
        query = query.filter(models.FinancialRecord.type == type)
    if category:
        query = query.filter(models.FinancialRecord.category == category)
    return query.order_by(models.FinancialRecord.date.desc()).all()


def get_record_by_id(db: Session, record_id: int):
    return db.query(models.FinancialRecord).filter(models.FinancialRecord.id == record_id).first()


def update_record(db: Session, record_id: int, record_update: schemas.RecordUpdate):
    db_record = get_record_by_id(db, record_id)
    if not db_record:
        return None
    update_data = record_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_record, key, value)
    db.commit()
    db.refresh(db_record)
    return db_record


def delete_record(db: Session, record_id: int):
    db_record = get_record_by_id(db, record_id)
    if not db_record:
        return None
    db.delete(db_record)
    db.commit()
    return db_record


def get_dashboard_summary(db: Session):
    total_income = db.query(func.sum(models.FinancialRecord.amount)).filter(
        models.FinancialRecord.type == "income"
    ).scalar() or 0

    total_expense = db.query(func.sum(models.FinancialRecord.amount)).filter(
        models.FinancialRecord.type == "expense"
    ).scalar() or 0

    return {
        "total_income": round(total_income, 2),
        "total_expenses": round(total_expense, 2),
        "net_balance": round(total_income - total_expense, 2)
    }