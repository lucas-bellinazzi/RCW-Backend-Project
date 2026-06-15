import uuid
from config.database import db, ma
from datetime import datetime, timezone
from sqlalchemy.dialects.postgresql import UUID
from marshmallow import validate


class MedicationRequest(db.Model):
    __tablename__ = 'medication_request'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    request_number = db.Column(db.String(50), nullable=False, unique=True)
    consumer_id = db.Column(UUID(as_uuid=True), db.ForeignKey('user.id'), nullable=False)
    product_name = db.Column(db.String(255), nullable=False)
    requested_quantity = db.Column(db.Integer, nullable=False)
    unit_dosage = db.Column(db.String(100), nullable=False)
    prescription_required = db.Column(db.Boolean, nullable=False, default=True)
    prescription_document = db.Column(db.String(500), nullable=True)  # URL/path to prescription
    
    # Fulfillment info
    assigned_manufacturer_id = db.Column(UUID(as_uuid=True), db.ForeignKey('organization.id'), nullable=True)
    batch_id = db.Column(db.String(100), nullable=True)
    
    # Status workflow: pending -> approved -> in_transit -> delivered / rejected / cancelled
    status = db.Column(db.String(20), nullable=False, default='pending')
    rejection_reason = db.Column(db.String(500), nullable=True)
    
    # Tracking
    approved_at = db.Column(db.DateTime, nullable=True)
    approved_by = db.Column(UUID(as_uuid=True), db.ForeignKey('user.id'), nullable=True)
    delivered_at = db.Column(db.DateTime, nullable=True)
    
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
    # Relationships
    consumer = db.relationship('User', foreign_keys=[consumer_id], backref='medication_requests')
    approver = db.relationship('User', foreign_keys=[approved_by])
    assigned_manufacturer = db.relationship('Organization', backref='assigned_requests')
    
    def __repr__(self):
        return f"<MedicationRequest {self.request_number} - {self.status}>"


class MedicationRequestOutput(ma.Schema):
    id = ma.UUID()
    request_number = ma.String()
    consumer_id = ma.UUID()
    product_name = ma.String()
    requested_quantity = ma.Integer()
    unit_dosage = ma.String()
    prescription_required = ma.Boolean()
    prescription_document = ma.String()
    assigned_manufacturer_id = ma.UUID()
    batch_id = ma.String()
    status = ma.String()
    rejection_reason = ma.String()
    approved_at = ma.DateTime()
    approved_by = ma.UUID()
    delivered_at = ma.DateTime()
    created_at = ma.DateTime()
    updated_at = ma.DateTime()


class MedicationRequestInputCreate(ma.Schema):
    product_name = ma.String(required=True, validate=validate.Length(min=3, max=255))
    requested_quantity = ma.Integer(required=True, validate=validate.Range(min=1))
    unit_dosage = ma.String(required=True, validate=validate.Length(min=1, max=100))
    prescription_required = ma.Boolean(required=True)
    prescription_document = ma.String(validate=validate.Length(max=500))


class MedicationRequestInputApprove(ma.Schema):
    batch_id = ma.String(required=True, validate=validate.Length(min=1, max=100))
    assigned_manufacturer_id = ma.UUID(required=True)


class MedicationRequestInputReject(ma.Schema):
    rejection_reason = ma.String(required=True, validate=validate.Length(min=10, max=500))


medication_request_output = MedicationRequestOutput()
medication_requests_output = MedicationRequestOutput(many=True)
medication_request_input_create = MedicationRequestInputCreate()
medication_request_input_approve = MedicationRequestInputApprove()
medication_request_input_reject = MedicationRequestInputReject()
