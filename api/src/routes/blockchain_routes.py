from flask import Blueprint, request
from src.controllers.blockchain_controller import BlockchainController


blockchain_bp = Blueprint("blockchain_bp", __name__)
blockchain_controller = BlockchainController()


@blockchain_bp.route("/batches", methods=["POST"])
def create_batch():
    return blockchain_controller.create_batch(request.get_json())


@blockchain_bp.route("/batches/transfer", methods=["POST"])
def transfer_batch():
    return blockchain_controller.transfer_batch(request.json)


@blockchain_bp.route("/batches/delivered", methods=["POST"])
def mark_batch_delivered():
    return blockchain_controller.mark_batch_delivered(request.json)


@blockchain_bp.route("/batches/<string:batch_id>", methods=["GET"])
def get_batch(batch_id):
    return blockchain_controller.get_batch(batch_id)


@blockchain_bp.route("/batches/<string:batch_id>/history", methods=["GET"])
def get_batch_history(batch_id):
    return blockchain_controller.get_batch_history(batch_id)
