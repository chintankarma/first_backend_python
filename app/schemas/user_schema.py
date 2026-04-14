from pydantic import BaseModel, EmailStr
from typing import Optional

class LoginRequest(BaseModel):
    email: str
    password: str

class SignupRequest(BaseModel):
    title: str
    name: str
    mobile_no: str
    email: EmailStr
    password: str
    indian_citizen: bool
    gender: str
    date_of_birth: str
    address: str
    state: str
    district: str
    pincode: str
    profile_pic: Optional[str] = None

class UpdateProfileRequest(BaseModel):
    name: str
    address: str
    state: str
    district: str
    pincode: str
    profile_pic: Optional[str] = None