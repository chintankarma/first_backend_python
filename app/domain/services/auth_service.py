import uuid

from app.infrastructure.repositories.user_repo import UserRepository
from app.core.security import verify_password, create_access_token
import os
import shutil

UPLOAD_DIR = "uploads"

class AuthService:

    @staticmethod
    def login_user(db, data):
        user = UserRepository.get_user_by_email(db, data.email)

        if not user:
            return {"success": False, "message": "User not found"}

        if not verify_password(data.password, user.password):
            return {"success": False, "message": "Wrong password"}

        token = create_access_token({"sub": user.email})

        return {
            "success": True,
            "message": "Login successful",
            "access_token": token,
            "token_type": "bearer",
            "user": { 
                "id": user.id, 
                "email": user.email,
                "name": user.name,
                "mobile_no": user.mobile_no,
                "indian_citizen": user.indian_citizen,
                "gender": user.gender,
                "date_of_birth": user.date_of_birth,
                "address": user.address,
                "state": user.state,
                "district": user.district,
                "profile_pic": user.profile_pic
            }
        }
    

    @staticmethod
    def signup_user(
        db,
        title, name, mobile_no, email, password,
        indian_citizen, gender, date_of_birth,
        address, state, district, pincode,
        profile_pic
    ):
        existing_user = UserRepository.get_user_by_email(db, email)

        if existing_user:
            return {"success": False, "message": "User already exists"}

        existing_mobile = UserRepository.get_user_by_mobile(db, mobile_no)

        if existing_mobile:
            return {"success": False, "message": "Mobile already registered"}

        # ✅ Save image
        filename = f"{uuid.uuid4()}_{profile_pic.filename}"
        file_path = os.path.join(UPLOAD_DIR, filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(profile_pic.file, buffer)

        if profile_pic:
            import uuid
            filename = f"{uuid.uuid4()}_{profile_pic.filename}"
            file_path = os.path.join(UPLOAD_DIR, filename)

            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(profile_pic.file, buffer)

            profile_pic_url = f"/uploads/{filename}"
        else:
            profile_pic_url = None

        # ✅ Save user
        user = UserRepository.create_user(
            db,
            {
                "title": title,
                "name": name,
                "mobile_no": mobile_no,
                "email": email,
                "password": password,
                "indian_citizen": indian_citizen,
                "gender": gender,
                "date_of_birth": date_of_birth,
                "address": address,
                "state": state,
                "district": district,
                "profile_pic": profile_pic_url
            }
        )

        return {
            "success": True,
            "message": "User created successfully",
            "user": {"email": user.email}
        }

    @staticmethod
    def get_profile(db, email):
        user = UserRepository.get_user_by_email(db, email)  

        if not user:
            return {"success": False, "message": "User not found"}  

        return {
            "success": True,
            "data": {
                "title": user.title,
                "name": user.name,
                "mobile_no": user.mobile_no,
                "email": user.email,
                "indian_citizen": user.indian_citizen,
                "gender": user.gender,
                "date_of_birth": user.date_of_birth,
                "address": user.address,
                "state": user.state,
                "district": user.district,
                "profile_pic": user.profile_pic
            }
        }
    
    @staticmethod
    def update_profile(db, email, data):
        user = UserRepository.get_user_by_email(db, email)
    
        if not user:
            return {"success": False, "message": "User not found"}
    
        UserRepository.update_user(db, user, data)
    
        return {"success": True, "message": "Profile updated"}
    
    @staticmethod
    def delete_user(db, user_id: int, current_email: str):
        user = UserRepository.get_user_by_id(db, user_id)

        if not user:
            return {"success": False, "message": "User not found"}

        if user.email != current_email:
            return {"success": False, "message": "Not authorized"}
    
        db.delete(user)
        try:
            db.commit()
        except Exception:
            db.rollback()
            raise
    
        return {"success": True, "message": "Profile deleted"}