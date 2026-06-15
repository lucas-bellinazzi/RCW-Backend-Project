"""add organization table

Revision ID: a1b2c3d4e5f6
Revises: c9dfaf8d51d6
Create Date: 2025-11-24 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID


# revision identifiers, used by Alembic.
revision = 'a1b2c3d4e5f6'
down_revision = 'c9dfaf8d51d6'
branch_labels = None
depends_on = None


def upgrade():
    # Create organization table
    op.create_table('organization',
        sa.Column('id', UUID(as_uuid=True), nullable=False),
        sa.Column('org_id', sa.String(length=100), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('org_type', sa.String(length=50), nullable=False),
        sa.Column('address', sa.String(length=500), nullable=True),
        sa.Column('contact_email', sa.String(length=255), nullable=False),
        sa.Column('contact_phone', sa.String(length=50), nullable=False),
        sa.Column('status', sa.String(length=20), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('org_id')
    )
    
    # Add organization_id column to user table
    op.add_column('user', sa.Column('organization_id', UUID(as_uuid=True), nullable=True))
    op.create_foreign_key('fk_user_organization', 'user', 'organization', ['organization_id'], ['id'])


def downgrade():
    # Remove foreign key and column from user table
    op.drop_constraint('fk_user_organization', 'user', type_='foreignkey')
    op.drop_column('user', 'organization_id')
    
    # Drop organization table
    op.drop_table('organization')
