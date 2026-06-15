from src.utils.api_response import ApiResponse
from src.services.auth_service import AuthService
from marshmallow.exceptions import ValidationError

class AuthController:
    def __init__(self):
        self.auth_service = AuthService()

    def login(self, data):
        try:
            user = self.auth_service.login(data)
            return ApiResponse.response(True, 'Login successful', user, 200)

        except ValidationError as e:
            return ApiResponse.response(False, e.messages, None, 400)
        
        except ValueError as e:
            return ApiResponse.response(False, e.args[0], None, 400)

        except Exception:
            return ApiResponse.response(False, 'An error occurred while logging in', None, 500)
        
    def refresh(self):
        try:
            new_access_token = self.auth_service.refresh()
            return ApiResponse.response(True, 'Refresh successful', new_access_token, 200)
        
        except ValueError as e:
            return ApiResponse.response(False, e.args[0], None, 403)
        
        except Exception:
            return ApiResponse.response(False, 'An error occurred while refreshing token', None, 500)
        
    def get_me(self):
        try:
            user = self.auth_service.get_me()

            return ApiResponse.response(True, 'Validated token', user, 200)
        
        except ValueError:
            return ApiResponse.response(False, 'Invalid or expired token', None, 403)
        
        except Exception:
            return ApiResponse.response(False, 'An error occurred while validating token', None, 500)