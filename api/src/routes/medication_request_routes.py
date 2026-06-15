from flask import Blueprint, request
from src.controllers.medication_request_controller import MedicationRequestController


medication_request_bp = Blueprint("medication_request_bp", __name__)
medication_request_controller = MedicationRequestController()


@medication_request_bp.route("/medication-requests", methods=["POST"])
def create_request():
    return medication_request_controller.create_request(request.get_json())


@medication_request_bp.route("/medication-requests", methods=["GET"])
def get_my_requests():
    return medication_request_controller.get_my_requests()


@medication_request_bp.route("/medication-requests/<string:request_id>", methods=["GET"])
def get_request_by_id(request_id):
    return medication_request_controller.get_request_by_id(request_id)


@medication_request_bp.route("/medication-requests/<string:request_id>/approve", methods=["POST"])
def approve_request(request_id):
    return medication_request_controller.approve_request(request_id, request.get_json())


@medication_request_bp.route("/medication-requests/<string:request_id>/reject", methods=["POST"])
def reject_request(request_id):
    return medication_request_controller.reject_request(request_id, request.get_json())


@medication_request_bp.route("/medication-requests/<string:request_id>/cancel", methods=["POST"])
def cancel_request(request_id):
    return medication_request_controller.cancel_request(request_id)
