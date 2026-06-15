from src.services.user_service import UserService
from werkzeug.exceptions import NotFound
from marshmallow.exceptions import ValidationError
from src.utils.api_response import ApiResponse
from jwt.exceptions import PyJWTError

class UserController:
    def __init__(self):
        self.user_service = UserService()

    def get_all_users(self, source=None):
        try:
            users = self.user_service.get_all_users(source)
            
            return ApiResponse.response(True, 'Users Found', users, 200)
        
        except PyJWTError:
            raise

        except Exception:
            return ApiResponse.response(False, 'An error occurred while getting all users', None, 500)

    def create_user(self, data):
        try:
            user = self.user_service.create_user(data)
            return ApiResponse.response(True, 'User created', user, 201)
        
        except ValidationError as e:
            return ApiResponse.response(False, e.messages, None, 400)

        except ValueError as e:
            return ApiResponse.response(False, e.args[0], None, 400)

        except Exception:
            return ApiResponse.response(False, 'An error occurred while creating a new user', None, 500)

    def update_user(self, user_id, data):
        try:            
            user = self.user_service.update_user(user_id, data)
            return ApiResponse.response(True, 'User updated', user, 200)
        
        except ValidationError as e:
            return ApiResponse.response(False, e.messages, None, 400)
        
        except NotFound:
            return ApiResponse.response(False, 'User not found', None, 404)
        
        except ValueError as e:
            return ApiResponse.response(False, e.args[0], None, 400)
        
        except Exception:
            return ApiResponse.response(False, 'An error occurred while updating the user', None, 500)
        
    def delete_user(self, user_id):
        try:
            self.user_service.delete_user(user_id)
            return ApiResponse.response(True, 'User deleted', None, 200)

        except NotFound:
            return ApiResponse.response(False, 'User not found', None, 404)

        except ValueError as e:
            return ApiResponse.response(False, e.args[0], None, 400)

        except Exception:
            return ApiResponse.response(False, 'An error occurred while deleting the user', None, 500)   