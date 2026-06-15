import uuid
from config.database import db, ma
from datetime import datetime, timezone
from sqlalchemy.dialects.postgresql import UUID
from marshmallow import validate, post_dump
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    phone = db.Column(db.String(255), nullable=False)
    hashed_password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    organization_id = db.Column(UUID(as_uuid=True), db.ForeignKey('organization.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=lambda:datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda:datetime.now(timezone.utc), onupdate=lambda:datetime.now(timezone.utc))
    
    # Relationship
    organization = db.relationship('Organization', back_populates='users')
    
    def __repr__(self):
        return f"<User {self.name}>"

class UserOutputBase(ma.Schema):
    id = ma.UUID()
    name = ma.String()
    email = ma.String()
    phone = ma.String()
    organization_id = ma.UUID()
    
class UserOutputAdmin(UserOutputBase):
    role = ma.String()    

class UserOutputLogin(UserOutputAdmin):
    access_token = ma.String()
    refresh_token = ma.String()

class UserOutputRefresh(ma.Schema):
    access_token = ma.String()

class UserInputLogin(ma.Schema):
    email = ma.String(required=True, validate=validate.Email(error="Invalid email"))
    password = ma.String(required=True, validate=validate.Length(min=8))

class UserInputCreate(ma.Schema):
    name = ma.String(required=True, validate=validate.Length(min=3))
    email = ma.String(required=True, validate=validate.Email(error="Invalid email"))
    phone = ma.String(required=True, validate=validate.Length(min=9))
    password = ma.String(required=True, validate=validate.Length(min=8))
    organization_id = ma.UUID(required=False)

class UserInputUpdate(ma.Schema):
    name = ma.String(required=False, validate=validate.Length(min=3))
    email = ma.String(required=False, validate=validate.Email(error="Invalid email"))
    phone = ma.String(required=False, validate=validate.Length(min=9))
    password = ma.String(required=False, validate=validate.Length(min=8))


users_output = UserOutputBase(many=True)
user_output_admin = UserOutputAdmin()
users_output_admin = UserOutputAdmin(many=True)
user_output_login = UserOutputLogin()
user_output_refresh = UserOutputRefresh()
user_input_login = UserInputLogin()
user_input_create = UserInputCreate()
user_input_update = UserInputUpdate()
