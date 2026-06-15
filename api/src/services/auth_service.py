import bcrypt
from src.models.user_model import user_input_login, user_output_login, user_output_refresh
from src.repositories.user_repository import UserRepository
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, verify_jwt_in_request

class AuthService:

    def __init__(self):
        self.user_repository = UserRepository()

    def login(self, data):

        validated_data = user_input_login.load(data)

        user = self.user_repository.get_active_user_by_email(validated_data['email'])
        if not user:
            raise ValueError('Invalid email or password')
        
        check_password = bcrypt.checkpw(password=validated_data['password'].encode('utf-8'), hashed_password=user.hashed_password.encode('utf-8'))
        if not check_password:
            raise ValueError('Invalid email or password')

        user.access_token = create_access_token(identity=user.id)
        user.refresh_token = create_refresh_token(identity=user.id)
        
        return user_output_login.dump(user)
    
    def refresh(self):
        identity = get_jwt_identity()
        user = self.user_repository.get_user(identity)

        if not user:
            raise ValueError("User is no longer active")

        token = create_access_token(identity=identity)

        return user_output_refresh.dump({'access_token': token})
    
    def get_me(self):  
        
        user = self.return_user_from_token(optional=False)
        
        if not user:
            raise ValueError("Unauthorized")

        return user_output_login.dump(user)
    
    def return_user_from_token(self, optional=False):        

        verify_jwt_in_request(optional=optional)
        user_id = get_jwt_identity()

        if user_id is None:
            return None

        return self.user_repository.get_user(user_id)
