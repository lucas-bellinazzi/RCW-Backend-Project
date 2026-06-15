from config.database import db
from src.models.organization_model import Organization
from typing import Optional, List
import uuid


class OrganizationRepository:
    def create(self, data: dict) -> Organization:
        organization = Organization(
            org_id=data['org_id'],
            name=data['name'],
            org_type=data['org_type'],
            address=data.get('address'),
            contact_email=data['contact_email'],
            contact_phone=data['contact_phone'],
            status='active'
        )
        
        db.session.add(organization)
        db.session.commit()
        return organization
    
    def find_by_id(self, organization_id: uuid.UUID) -> Optional[Organization]:
        return Organization.query.filter_by(id=organization_id).first()
    
    def find_by_org_id(self, org_id: str) -> Optional[Organization]:
        return Organization.query.filter_by(org_id=org_id).first()
    
    def find_by_type(self, org_type: str) -> List[Organization]:
        return Organization.query.filter_by(org_type=org_type, status='active').all()
    
    def find_all(self) -> List[Organization]:
        return Organization.query.filter_by(status='active').all()
    
    def update(self, organization_id: uuid.UUID, data: dict) -> Optional[Organization]:
        organization = self.find_by_id(organization_id)
        if not organization:
            return None
        
        if 'name' in data:
            organization.name = data['name']
        if 'address' in data:
            organization.address = data['address']
        if 'contact_email' in data:
            organization.contact_email = data['contact_email']
        if 'contact_phone' in data:
            organization.contact_phone = data['contact_phone']
        if 'status' in data:
            organization.status = data['status']
        
        db.session.commit()
        return organization
    
    def delete(self, organization_id: uuid.UUID) -> bool:
        organization = self.find_by_id(organization_id)
        if not organization:
            return False
        
        organization.status = 'inactive'
        db.session.commit()
        return True
