import uuid
from config.database import db, ma
from datetime import datetime, timezone
from sqlalchemy.dialects.postgresql import UUID
from marshmallow import validate


class Notification(db.Model):
    __tablename__ = 'notification'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    message = db.Column(db.Text, nullable=False)
    notification_type = db.Column(db.String(50), nullable=False)  # request_created, request_approved, transfer_received, etc
    related_entity_type = db.Column(db.String(50), nullable=True)  # medication_request, batch_transfer, etc
    related_entity_id = db.Column(db.String(100), nullable=True)
    is_read = db.Column(db.Boolean, nullable=False, default=False)
    read_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    
    # Relationship
    user = db.relationship('User', backref='notifications')
    
    def __repr__(self):
        return f"<Notification {self.title} for User {self.user_id}>"
    
    def mark_as_read(self):
        self.is_read = True
        self.read_at = datetime.now(timezone.utc)


class NotificationOutput(ma.Schema):
    id = ma.UUID()
    user_id = ma.UUID()
    title = ma.String()
    message = ma.String()
    notification_type = ma.String()
    related_entity_type = ma.String()
    related_entity_id = ma.String()
    is_read = ma.Boolean()
    read_at = ma.DateTime()
    created_at = ma.DateTime()


class NotificationInputCreate(ma.Schema):
    user_id = ma.UUID(required=True)
    title = ma.String(required=True, validate=validate.Length(min=3, max=255))
    message = ma.String(required=True, validate=validate.Length(min=1))
    notification_type = ma.String(required=True, validate=validate.Length(min=3, max=50))
    related_entity_type = ma.String(validate=validate.Length(max=50))
    related_entity_id = ma.String(validate=validate.Length(max=100))


notification_output = NotificationOutput()
notifications_output = NotificationOutput(many=True)
notification_input_create = NotificationInputCreate()
