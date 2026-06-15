from flask import Blueprint, request
from src.controllers.user_controller import UserController
from src.utils.constants import UserRole

user_bp = Blueprint('user_bp', __name__)
user_controller = UserController()

@user_bp.route('/', methods=['GET'])
def get_all_users():
    source = request.args.get('source', False)

    return user_controller.get_all_users(source)
    
@user_bp.route('/', methods=['POST'])
def create_user():
    data = request.json
    return user_controller.create_user(data)

@user_bp.route('/<uuid:user_id>', methods=['PATCH'])
def update_user(user_id):
    data = request.json
    return user_controller.update_user(user_id, data)

@user_bp.route('/<uuid:user_id>', methods=['DELETE'])
def delete_user(user_id):
    return user_controller.delete_user(user_id)
