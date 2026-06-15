from flask_jwt_extended import JWTManager
from datetime import timedelta
from config.settings import JWT_SECRET_KEY
from src.utils.api_response import ApiResponse

jwt = JWTManager()

def configure_jwt(app):
    app.config['JWT_SECRET_KEY'] = JWT_SECRET_KEY
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=15)
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=15)

    jwt.init_app(app)

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return ApiResponse.response(False, "Missing authorization token", None, 401)

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return ApiResponse.response(False, "Token has expired", None, 401)

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return ApiResponse.response(False, "Invalid or malformed token", None, 401)

    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return ApiResponse.response(False, "Token has been revoked", None, 401)
