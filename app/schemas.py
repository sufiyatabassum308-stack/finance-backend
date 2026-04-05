from pydantic import BaseModel, EmailStr, field_validator
from datetime import date as dt_date, datetime
from typing import Optional


class UserBase(BaseModel):
    name: str
    email: EmailStr
    role: str

    @field_validator("name")
    @classmethod
    def validate_name(cls, value):
        if not value.strip():
            raise ValueError("Name cannot be empty")
        return value.strip()

    @field_validator("role")
    @classmethod
    def validate_role(cls, value):
        if value not in ["viewer", "analyst", "admin"]:
            raise ValueError("Role must be viewer, analyst, or admin")
        return value


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[str] = None
    is_active: Optional[bool] = None

    @field_validator("name")
    @classmethod
    def validate_name(cls, value):
        if value is not None and not value.strip():
            raise ValueError("Name cannot be empty")
        return value.strip() if value else value

    @field_validator("role")
    @classmethod
    def validate_role(cls, value):
        if value is not None and value not in ["viewer", "analyst", "admin"]:
            raise ValueError("Role must be viewer, analyst, or admin")
        return value


class UserResponse(UserBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True


class RecordBase(BaseModel):
    amount: float
    type: str
    category: str
    date: dt_date
    note: Optional[str] = None

    @field_validator("amount")
    @classmethod
    def validate_amount(cls, value):
        if value <= 0:
            raise ValueError("Amount must be greater than 0")
        return value

    @field_validator("type")
    @classmethod
    def validate_type(cls, value):
        if value not in ["income", "expense"]:
            raise ValueError("Type must be income or expense")
        return value

    @field_validator("category")
    @classmethod
    def validate_category(cls, value):
        if not value.strip():
            raise ValueError("Category cannot be empty")
        return value.strip()

    @field_validator("note")
    @classmethod
    def validate_note(cls, value):
        if value is not None:
            return value.strip()
        return value


class RecordCreate(RecordBase):
    created_by: int


class RecordUpdate(BaseModel):
    amount: Optional[float] = None
    type: Optional[str] = None
    category: Optional[str] = None
    date: Optional[dt_date] = None
    note: Optional[str] = None

    @field_validator("amount")
    @classmethod
    def validate_amount(cls, value):
        if value is not None and value <= 0:
            raise ValueError("Amount must be greater than 0")
        return value

    @field_validator("type")
    @classmethod
    def validate_type(cls, value):
        if value is not None and value not in ["income", "expense"]:
            raise ValueError("Type must be income or expense")
        return value

    @field_validator("category")
    @classmethod
    def validate_category(cls, value):
        if value is not None and not value.strip():
            raise ValueError("Category cannot be empty")
        return value.strip() if value else value

    @field_validator("note")
    @classmethod
    def validate_note(cls, value):
        if value is not None:
            return value.strip()
        return value


class RecordResponse(RecordBase):
    id: int
    created_by: int
    created_at: datetime

    class Config:
        from_attributes = True