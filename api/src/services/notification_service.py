from werkzeug.exceptions import NotFound, BadRequest, Forbidden
from src.repositories.notification_repository import NotificationRepository
from src.services.auth_service import AuthService


class NotificationService:
    def __init__(self):
        self.repository = NotificationRepository()
        self.auth_service = AuthService()

    def _get_current_user(self):
        user = self.auth_service.return_user_from_token()
        if user is None:
            raise BadRequest("Authentication required")
        return user

    def get_my_notifications(self, unread_only=False):
        user = self._get_current_user()
        return self.repository.find_by_user(user.id, unread_only)
    
    def mark_notification_as_read(self, notification_id):
        user = self._get_current_user()
        notification = self.repository.find_by_id(notification_id)
        
        if not notification:
            raise NotFound("Notification not found")
        
        if notification.user_id != user.id:
            raise Forbidden("You can only mark your own notifications as read")
        
        return self.repository.mark_as_read(notification_id)
    
    def mark_all_as_read(self):
        user = self._get_current_user()
        return self.repository.mark_all_as_read(user.id)
    
    def delete_notification(self, notification_id):
        user = self._get_current_user()
        notification = self.repository.find_by_id(notification_id)
        
        if not notification:
            raise NotFound("Notification not found")
        
        if notification.user_id != user.id:
            raise Forbidden("You can only delete your own notifications")
        
        return self.repository.delete(notification_id)
