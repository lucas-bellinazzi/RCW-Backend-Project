from src.models.user_model import User, db
from src.utils.constants import UserStatus

class UserRepository:

    def get_active_user_by_email(self, email):
        try:
            user = User.query.filter_by(email=email, status=UserStatus.ACTIVE.value).first()
            return user
        except Exception:
            db.session.rollback()
            raise

    def get_all_user_by_email(self, email):
        try:
            user = User.query.filter_by(email=email).first()
            return user
        except Exception:
            db.session.rollback()
            raise

    def get_user_by_email_and_different_id(self, email, user_id):
        try:
            user = User.query.filter(User.email == email, User.id != user_id).first()
            return user
        except Exception:
            db.session.rollback()
            raise

    def get_all_users(self):
        try: 
            users = User.query.filter_by(status=UserStatus.ACTIVE.value).all()
            return users
        except Exception:
            db.session.rollback()
            raise
        

    def get_user(self, user_id):
        try:
            user = User.query.filter_by(id=user_id, status=UserStatus.ACTIVE.value).first()
            return user
        except Exception:
            db.session.rollback()
            raise

    def create_user(self, user):
        try:
            db.session.add(user)
            db.session.commit()
            return user
        except Exception:
            db.session.rollback()
            raise

    def update_user(self, user, data):
        try:
            for key, value in data.items():
                setattr(user, key, value)
            db.session.commit()
            return user
        except Exception:
            db.session.rollback()
            raise

    def delete_user(self, user):
        try:
            user.status = UserStatus.INACTIVE.value
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise