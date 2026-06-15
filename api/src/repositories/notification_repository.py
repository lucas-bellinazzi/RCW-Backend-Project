from config.database import db
from src.models.notification_model import Notification
from typing import Optional, List
import uuid


class NotificationRepository:
    def create(self, data: dict) -> Notification:
        notification = Notification(
            user_id=data['user_id'],
            title=data['title'],
            message=data['message'],
            notification_type=data['notification_type'],
            related_entity_type=data.get('related_entity_type'),
            related_entity_id=data.get('related_entity_id'),
            is_read=False
        )
        
        db.session.add(notification)
        db.session.commit()
        return notification
    
    def find_by_id(self, notification_id: uuid.UUID) -> Optional[Notification]:
        return Notification.query.filter_by(id=notification_id).first()
    
    def find_by_user(self, user_id: uuid.UUID, unread_only: bool = False) -> List[Notification]:
        query = Notification.query.filter_by(user_id=user_id)
        
        if unread_only:
            query = query.filter_by(is_read=False)
        
        return query.order_by(Notification.created_at.desc()).all()
    
    def mark_as_read(self, notification_id: uuid.UUID) -> Optional[Notification]:
        notification = self.find_by_id(notification_id)
        if not notification:
            return None
        
        notification.mark_as_read()
        db.session.commit()
        return notification
    
    def mark_all_as_read(self, user_id: uuid.UUID) -> int:
        notifications = Notification.query.filter_by(user_id=user_id, is_read=False).all()
        count = len(notifications)
        
        for notification in notifications:
            notification.mark_as_read()
        
        db.session.commit()
        return count
    
    def delete(self, notification_id: uuid.UUID) -> bool:
        notification = self.find_by_id(notification_id)
        if not notification:
            return False
        
        db.session.delete(notification)
        db.session.commit()
        return True
