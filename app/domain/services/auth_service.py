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
                "pincode": user.pincode,
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

        # ✅ Save image
        file_path = os.path.join(UPLOAD_DIR, profile_pic.filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(profile_pic.file, buffer)

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
                "pincode": pincode,

                "profile_pic": f"/uploads/{profile_pic.filename}"
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
                "pincode": user.pincode,
                "profile_pic": user.profile_pic
            }
        }
    
    @staticmethod
    def update_profile(db, email, data):
        user = UserRepository.get_user_by_email(db, email)

        if not user:
            return {"success": False, "message": "User not found"}

        updated_user = UserRepository.update_user(db, user, data)

        return {
            "success": True,
            "message": "Profile updated successfully",
            "data": {
                "title": updated_user.title,
                "name": updated_user.name,
                "mobile_no": updated_user.mobile_no,
                "email": updated_user.email,
                "indian_citizen": updated_user.indian_citizen,
                "gender": updated_user.gender,
                "date_of_birth": updated_user.date_of_birth,
                "address": updated_user.address,
                "state": updated_user.state,
                "district": updated_user.district,
                "pincode": updated_user.pincode,
                "profile_pic": updated_user.profile_pic
            }
        }