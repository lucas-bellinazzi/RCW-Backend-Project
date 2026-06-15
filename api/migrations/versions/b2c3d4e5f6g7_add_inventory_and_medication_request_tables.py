"""add inventory and medication request tables

Revision ID: b2c3d4e5f6g7
Revises: a1b2c3d4e5f6
Create Date: 2025-11-24 10:30:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID


# revision identifiers, used by Alembic.
revision = 'b2c3d4e5f6g7'
down_revision = 'a1b2c3d4e5f6'
branch_labels = None
depends_on = None


def upgrade():
    # Create inventory table
    op.create_table('inventory',
        sa.Column('id', UUID(as_uuid=True), nullable=False),
        sa.Column('organization_id', UUID(as_uuid=True), nullable=False),
        sa.Column('batch_id', sa.String(length=100), nullable=False),
        sa.Column('product_name', sa.String(length=255), nullable=False),
        sa.Column('available_quantity', sa.Integer(), nullable=False),
        sa.Column('reserved_quantity', sa.Integer(), nullable=False),
        sa.Column('unit_dosage', sa.String(length=100), nullable=False),
        sa.Column('manufacture_date', sa.String(length=50), nullable=False),
        sa.Column('expiry_date', sa.String(length=50), nullable=False),
        sa.Column('unit_price', sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column('status', sa.String(length=20), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['organization_id'], ['organization.id'])
    )
    
    # Create medication_request table
    op.create_table('medication_request',
        sa.Column('id', UUID(as_uuid=True), nullable=False),
        sa.Column('request_number', sa.String(length=50), nullable=False),
        sa.Column('consumer_id', UUID(as_uuid=True), nullable=False),
        sa.Column('product_name', sa.String(length=255), nullable=False),
        sa.Column('requested_quantity', sa.Integer(), nullable=False),
        sa.Column('unit_dosage', sa.String(length=100), nullable=False),
        sa.Column('prescription_required', sa.Boolean(), nullable=False),
        sa.Column('prescription_document', sa.String(length=500), nullable=True),
        sa.Column('assigned_manufacturer_id', UUID(as_uuid=True), nullable=True),
        sa.Column('batch_id', sa.String(length=100), nullable=True),
        sa.Column('status', sa.String(length=20), nullable=False),
        sa.Column('rejection_reason', sa.String(length=500), nullable=True),
        sa.Column('approved_at', sa.DateTime(), nullable=True),
        sa.Column('approved_by', UUID(as_uuid=True), nullable=True),
        sa.Column('delivered_at', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('request_number'),
        sa.ForeignKeyConstraint(['consumer_id'], ['user.id']),
        sa.ForeignKeyConstraint(['approved_by'], ['user.id']),
        sa.ForeignKeyConstraint(['assigned_manufacturer_id'], ['organization.id'])
    )
    
    # Create notification table
    op.create_table('notification',
        sa.Column('id', UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', UUID(as_uuid=True), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('message', sa.Text(), nullable=False),
        sa.Column('notification_type', sa.String(length=50), nullable=False),
        sa.Column('related_entity_type', sa.String(length=50), nullable=True),
        sa.Column('related_entity_id', sa.String(length=100), nullable=True),
        sa.Column('is_read', sa.Boolean(), nullable=False),
        sa.Column('read_at', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'])
    )


def downgrade():
    op.drop_table('notification')
    op.drop_table('medication_request')
    op.drop_table('inventory')
