from flask import Blueprint, request
from src.controllers.auth_controller import AuthController
from flask_jwt_extended import jwt_required

auth_bp = Blueprint('auth_bp', __name__)
auth_controller = AuthController()

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    return auth_controller.login(data)

@auth_bp.route('/refresh', methods=['GET'])
@jwt_required(refresh=True) 
def refresh():
    return auth_controller.refresh()

@auth_bp.route('/get_me', methods=['GET'])
@jwt_required() 
def get_me():
    return auth_controller.get_me()