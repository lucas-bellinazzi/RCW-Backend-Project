from flask import jsonify

class ApiResponse:
    @staticmethod
    def response(success, message, data=None, status_code=200):
        response = {
            'success': success,
            'message': message,
            'data': data
        }
            
        return jsonify(response), status_code
        