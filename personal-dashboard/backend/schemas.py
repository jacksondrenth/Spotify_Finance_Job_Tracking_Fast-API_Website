from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# Job Application schemas
class JobApplicationCreate(BaseModel):
    company: str
    role: str
    status: str = "applied"
    notes: Optional[str] = None
    contact_name: Optional[str] = None
    contact_email: Optional[str] = None
    url: Optional[str] = None

class JobApplicationUpdate(BaseModel):
    company: Optional[str] = None
    role: Optional[str] = None
    status: Optional[str] = None
    notes: Optional[str] = None
    contact_name: Optional[str] = None
    contact_email: Optional[str] = None
    url: Optional[str] = None

class JobApplicationResponse(BaseModel):
    id: int
    company: str
    role: str
    status: str
    applied_date: datetime
    notes: Optional[str]
    contact_name: Optional[str]
    contact_email: Optional[str]
    url: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Transaction schemas
class TransactionResponse(BaseModel):
    id: int
    plaid_transaction_id: str
    name: str
    amount: float
    category: Optional[str]
    date: datetime
    account_id: Optional[str]

    class Config:
        from_attributes = True