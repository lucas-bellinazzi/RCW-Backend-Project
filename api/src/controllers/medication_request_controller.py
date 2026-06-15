from flask import jsonify
from src.services.medication_request_service import MedicationRequestService
from src.models.medication_request_model import (
    medication_request_output,
    medication_requests_output,
    medication_request_input_create,
    medication_request_input_approve,
    medication_request_input_reject
)
from src.utils.api_response import ApiResponse
from marshmallow import ValidationError


class MedicationRequestController:
    def __init__(self):
        self.service = MedicationRequestService()

    def create_request(self, data):
        try:
            validated_data = medication_request_input_create.load(data)
            medication_request = self.service.create_request(validated_data)
            return ApiResponse.response(True, "Medication request created successfully", medication_request_output.dump(medication_request), 201)
        except ValidationError as e:
            return ApiResponse.response(False, str(e.messages), None, 400)
        except Exception as e:
            return ApiResponse.response(False, str(e), None, 400)
    
    def get_my_requests(self):
        try:
            requests = self.service.get_my_requests()
            return ApiResponse.response(True, "Medication requests retrieved successfully", medication_requests_output.dump(requests), 200)
        except Exception as e:
            return ApiResponse.response(False, str(e), None, 400)

    def get_request_by_id(self, request_id):
        try:
            medication_request = self.service.get_request_by_id(request_id)
            return ApiResponse.response(True, "Request retrieved successfully", medication_request_output.dump(medication_request), 200)
        except Exception as e:
            return ApiResponse.response(False, str(e), None, 404)

    def approve_request(self, request_id, data):
        try:
            validated_data = medication_request_input_approve.load(data)
            medication_request = self.service.approve_request(request_id, validated_data)
            return ApiResponse.response(True, "Request approved successfully", medication_request_output.dump(medication_request), 200)
        except ValidationError as e:
            return ApiResponse.response(False, str(e.messages), None, 400)
        except Exception as e:
            return ApiResponse.response(False, str(e), None, 400)
    
    def reject_request(self, request_id, data):
        try:
            validated_data = medication_request_input_reject.load(data)
            medication_request = self.service.reject_request(request_id, validated_data)
            return ApiResponse.response(True, "Request rejected successfully", medication_request_output.dump(medication_request), 200)
        except ValidationError as e:
            return ApiResponse.response(False, str(e.messages), None, 400)
        except Exception as e:
            return ApiResponse.response(False, str(e), None, 400)
    
    def cancel_request(self, request_id):
        try:
            medication_request = self.service.cancel_request(request_id)
            return ApiResponse.response(True, "Request canceled successfully", medication_request_output.dump(medication_request), 200)
        except Exception as e:
            return ApiResponse.response(False, str(e), None, 400)