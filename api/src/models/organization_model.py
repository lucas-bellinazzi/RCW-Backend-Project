import uuid
from config.database import db, ma
from datetime import datetime, timezone
from sqlalchemy.dialects.postgresql import UUID
from marshmallow import validate


class Organization(db.Model):
    __tablename__ = 'organization'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    org_id = db.Column(db.String(100), nullable=False, unique=True)
    name = db.Column(db.String(255), nullable=False)
    org_type = db.Column(db.String(50), nullable=False)  # manufacturer, distributor, pharmacy
    address = db.Column(db.String(500), nullable=True)
    contact_email = db.Column(db.String(255), nullable=False)
    contact_phone = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='active')
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
    # Relationship
    users = db.relationship('User', back_populates='organization', lazy=True)
    
    def __repr__(self):
        return f"<Organization {self.name} ({self.org_id})>"


class OrganizationOutput(ma.Schema):
    id = ma.UUID()
    org_id = ma.String()
    name = ma.String()
    org_type = ma.String()
    address = ma.String()
    contact_email = ma.String()
    contact_phone = ma.String()
    status = ma.String()
    created_at = ma.DateTime()
    updated_at = ma.DateTime()


class OrganizationInputCreate(ma.Schema):
    org_id = ma.String(required=True, validate=validate.Length(min=3, max=100))
    name = ma.String(required=True, validate=validate.Length(min=3, max=255))
    org_type = ma.String(required=True, validate=validate.OneOf(['manufacturer', 'distributor', 'pharmacy']))
    address = ma.String(validate=validate.Length(max=500))
    contact_email = ma.String(required=True, validate=validate.Email())
    contact_phone = ma.String(required=True, validate=validate.Length(min=9, max=50))


class OrganizationInputUpdate(ma.Schema):
    name = ma.String(validate=validate.Length(min=3, max=255))
    address = ma.String(validate=validate.Length(max=500))
    contact_email = ma.String(validate=validate.Email())
    contact_phone = ma.String(validate=validate.Length(min=9, max=50))
    status = ma.String(validate=validate.OneOf(['active', 'inactive']))


organization_output = OrganizationOutput()
organizations_output = OrganizationOutput(many=True)
organization_input_create = OrganizationInputCreate()
organization_input_update = OrganizationInputUpdate()
