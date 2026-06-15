import uuid
from config.database import db, ma
from datetime import datetime, timezone
from sqlalchemy.dialects.postgresql import UUID
from marshmallow import validate


class Inventory(db.Model):
    __tablename__ = 'inventory'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id = db.Column(UUID(as_uuid=True), db.ForeignKey('organization.id'), nullable=False)
    batch_id = db.Column(db.String(100), nullable=False)
    product_name = db.Column(db.String(255), nullable=False)
    available_quantity = db.Column(db.Integer, nullable=False, default=0)
    reserved_quantity = db.Column(db.Integer, nullable=False, default=0)
    unit_dosage = db.Column(db.String(100), nullable=False)
    manufacture_date = db.Column(db.String(50), nullable=False)
    expiry_date = db.Column(db.String(50), nullable=False)
    unit_price = db.Column(db.Numeric(10, 2), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='available')  # available, low_stock, out_of_stock
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
    # Relationship
    organization = db.relationship('Organization', backref='inventory_items')
    
    def __repr__(self):
        return f"<Inventory {self.product_name} - {self.batch_id}>"
    
    @property
    def total_quantity(self):
        return self.available_quantity + self.reserved_quantity


class InventoryOutput(ma.Schema):
    id = ma.UUID()
    organization_id = ma.UUID()
    batch_id = ma.String()
    product_name = ma.String()
    available_quantity = ma.Integer()
    reserved_quantity = ma.Integer()
    total_quantity = ma.Integer()
    unit_dosage = ma.String()
    manufacture_date = ma.String()
    expiry_date = ma.String()
    unit_price = ma.Decimal(as_string=True)
    status = ma.String()
    created_at = ma.DateTime()
    updated_at = ma.DateTime()


class InventoryInputCreate(ma.Schema):
    organization_id = ma.UUID(required=True)
    batch_id = ma.String(required=True, validate=validate.Length(min=1, max=100))
    product_name = ma.String(required=True, validate=validate.Length(min=3, max=255))
    available_quantity = ma.Integer(required=True, validate=validate.Range(min=0))
    unit_dosage = ma.String(required=True, validate=validate.Length(min=1, max=100))
    manufacture_date = ma.String(required=True)
    expiry_date = ma.String(required=True)
    unit_price = ma.Decimal(required=True, as_string=True)


class InventoryInputUpdate(ma.Schema):
    available_quantity = ma.Integer(validate=validate.Range(min=0))
    reserved_quantity = ma.Integer(validate=validate.Range(min=0))
    status = ma.String(validate=validate.OneOf(['available', 'low_stock', 'out_of_stock']))


inventory_output = InventoryOutput()
inventories_output = InventoryOutput(many=True)
inventory_input_create = InventoryInputCreate()
inventory_input_update = InventoryInputUpdate()
