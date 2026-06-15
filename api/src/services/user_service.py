import bcrypt
from src.repositories.user_repository import UserRepository
from src.models.user_model import User, user_input_create, user_input_update, users_output, users_output_admin, user_output_admin
from src.utils.constants import UserRole, UserStatus, RequestSource
from werkzeug.exceptions import NotFound
from src.services.auth_service import AuthService


class UserService:
    def __init__(self):
        self.user_repository = UserRepository()
        self.auth_service = AuthService()

    def get_all_users(self,source=None):    
        users = self.user_repository.get_all_users()

        user = self.auth_service.return_user_from_token(optional=True)

        if user is not None and source == RequestSource.DASHBOARD.value and user.role == UserRole.ADMIN.value:           
            return users_output_admin.dump(users)
            
        return users_output.dump(users)

    def create_user(self, data):
        user_data = user_input_create.load(data)
        if self.user_repository.get_all_user_by_email(user_data['email']):
            raise ValueError('This email already exists')

        hashed_password = bcrypt.hashpw(user_data['password'].encode('utf-8'), bcrypt.gensalt())
        user = User(
            name=user_data['name'],
            email=user_data['email'],
            phone=user_data['phone'],
            hashed_password=hashed_password.decode('utf-8'),
            role=UserRole.GUEST.value,
            status=UserStatus.ACTIVE.value
        )
        created_user = self.user_repository.create_user(user)
        return user_output_admin.dump(created_user)

    def update_user(self, user_id, data):
        user_data = user_input_update.load(data)
        user = self.user_repository.get_user(user_id)
        if not user:
            raise NotFound("User not found")

        if user_data.get('email') is not None:   
            if self.user_repository.get_user_by_email_and_different_id(user_data['email'], user_id):
                raise ValueError('This email already exists')
        
        if user_data.get('password') is not None:
            hashed_password = bcrypt.hashpw(user_data['password'].encode('utf-8'), bcrypt.gensalt())
            user_data['password'] = hashed_password.decode('utf-8')

        updated_user = self.user_repository.update_user(user, user_data)
        return user_output_admin.dump(updated_user)
    
    def delete_user(self, user_id):
        current_user = self.auth_service.return_user_from_token()

        if not current_user:
            raise ValueError("Something went wrong")
        if current_user.id == user_id:
            raise ValueError("You are not allowed to perform this action")

        user = self.user_repository.get_user(user_id)  

        if not user:
            raise NotFound("User not found")
        if user.role == UserRole.ADMIN.value:
            raise ValueError("You cannot delete an admin user")

        self.user_repository.delete_user(user)

        return None