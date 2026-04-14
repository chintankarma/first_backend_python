from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.user_schema import LoginRequest
from app.domain.services.auth_service import AuthService
from app.core.deps import get_db
from app.core.security import get_current_user
from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session
from app.domain.services.auth_service import AuthService
from app.core.deps import get_db
from app.schemas.user_schema import UpdateProfileRequest

router = APIRouter()

@router.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):
    return AuthService.login_user(db, data)

@router.get("/me")
def get_me(
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return AuthService.get_profile(db, current_user)

@router.post("/signup")
def signup(
    title: str = Form(...),
    name: str = Form(...),
    mobile_no: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),

    indian_citizen: bool = Form(...),
    gender: str = Form(...),
    date_of_birth: str = Form(...),

    address: str = Form(...),
    state: str = Form(...),
    district: str = Form(...),
    pincode: str = Form(...),

    profile_pic: UploadFile = File(...),

    db: Session = Depends(get_db)
):
    return AuthService.signup_user(
        db,
        title, name, mobile_no, email, password,
        indian_citizen, gender, date_of_birth,
        address, state, district, pincode,
        profile_pic
    )


@router.put("/update-profile")
def update_profile(
    data: UpdateProfileRequest,
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return AuthService.update_profile(db, current_user, data)