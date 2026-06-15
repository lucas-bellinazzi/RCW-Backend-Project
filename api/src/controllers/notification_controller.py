from flask import jsonify
from src.services.notification_service import NotificationService
from src.models.notification_model import notification_output, notifications_output
from src.utils.api_response import ApiResponse


class NotificationController:
    def __init__(self):
        self.service = NotificationService()

    def get_my_notifications(self, unread_only=False):
        try:
            notifications = self.service.get_my_notifications(unread_only)
            return ApiResponse.response(True, "Notifications retrieved successfully", notifications_output.dump(notifications), 200)
        except Exception as e:
            return ApiResponse.response(False, str(e), None, 400)

    def mark_as_read(self, notification_id):
        try:
            notification = self.service.mark_notification_as_read(notification_id)
            return ApiResponse.response(True, "Notification marked as read successfully", notification_output.dump(notification), 200)
        except Exception as e:
            return ApiResponse.response(False, str(e), None, 400)

    def mark_all_as_read(self):
        try:
            count = self.service.mark_all_as_read()
            return ApiResponse.response(True, f"{count} notifications marked as read", {'count': count}, 200)
        except Exception as e:
            return ApiResponse.response(False, str(e), None, 400)

    def delete_notification(self, notification_id):
        try:
            success = self.service.delete_notification(notification_id)
            return ApiResponse.response(True, "Notification deleted successfully", {'success': success}, 200)
        except Exception as e:
            return ApiResponse.response(False, str(e), None, 400)