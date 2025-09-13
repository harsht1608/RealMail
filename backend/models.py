from pydantic import BaseModel, EmailStr
from datetime import datetime

class EmailRequest(BaseModel):
    # name: str
    recipient: EmailStr
    industry: str
    role: str
    pain_point: str
    tone: str
    template: str

class EmailHistory(BaseModel):
    # name: str
    recipient: EmailStr
    industry: str
    role: str
    pain_point: str
    tone: str
    template: str
    generated_email: str
    created_at: datetime
