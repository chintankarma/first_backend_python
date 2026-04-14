from sqlalchemy.orm import Session
from app.domain.models import user
from app.domain.models.user import User
from app.core.security import hash_password

class UserRepository:

    @staticmethod
    def get_user_by_email(db, email: str):
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def create_user(db, data):
        from app.core.security import hash_password

        user = User(
            title=data["title"],
            name=data["name"],
            mobile_no=data["mobile_no"],
            email=data["email"],
            password=hash_password(data["password"]),

            indian_citizen=data["indian_citizen"],
            gender=data["gender"],
            date_of_birth=data["date_of_birth"],

            address=data["address"],
            state=data["state"],
            district=data["district"],
            pincode=data["pincode"],

            profile_pic=data["profile_pic"]
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        return user

    @staticmethod
    def update_user(db, user, data):
        user.name = data.name
        user.address = data.address
        user.state = data.state
        user.district = data.district
        user.pincode = data.pincode
    
        db.commit()
        db.refresh(user)
    
        return user