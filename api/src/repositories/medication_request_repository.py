from config.database import db
from src.models.medication_request_model import MedicationRequest
from datetime import datetime, timezone
from typing import Optional, List
import uuid


class MedicationRequestRepository:
    def create(self, data: dict, consumer_id: uuid.UUID) -> MedicationRequest:
        # Generate unique request number
        request_number = f"REQ-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}-{str(uuid.uuid4())[:8]}"
        
        medication_request = MedicationRequest(
            request_number=request_number,
            consumer_id=consumer_id,
            product_name=data['product_name'],
            requested_quantity=data['requested_quantity'],
            unit_dosage=data['unit_dosage'],
            prescription_required=data['prescription_required'],
            prescription_document=data.get('prescription_document'),
            status='pending'
        )
        
        db.session.add(medication_request)
        db.session.commit()
        return medication_request
    
    def find_by_id(self, request_id: uuid.UUID) -> Optional[MedicationRequest]:
        return MedicationRequest.query.filter_by(id=request_id).first()
    
    def find_by_request_number(self, request_number: str) -> Optional[MedicationRequest]:
        return MedicationRequest.query.filter_by(request_number=request_number).first()
    
    def find_by_consumer(self, consumer_id: uuid.UUID) -> List[MedicationRequest]:
        return MedicationRequest.query.filter_by(consumer_id=consumer_id).order_by(MedicationRequest.created_at.desc()).all()
    
    def find_pending_requests(self) -> List[MedicationRequest]:
        return MedicationRequest.query.filter_by(status='pending').order_by(MedicationRequest.created_at.asc()).all()
    
    def find_by_manufacturer(self, manufacturer_id: uuid.UUID) -> List[MedicationRequest]:
        return MedicationRequest.query.filter_by(assigned_manufacturer_id=manufacturer_id).order_by(MedicationRequest.created_at.desc()).all()
    
    def approve_request(self, request_id: uuid.UUID, approver_id: uuid.UUID, batch_id: str, manufacturer_id: uuid.UUID) -> MedicationRequest:
        medication_request = self.find_by_id(request_id)
        if not medication_request:
            return None
        
        medication_request.status = 'approved'
        medication_request.approved_at = datetime.now(timezone.utc)
        medication_request.approved_by = approver_id
        medication_request.batch_id = batch_id
        medication_request.assigned_manufacturer_id = manufacturer_id
        medication_request.updated_at = datetime.now(timezone.utc)
        
        db.session.commit()
        return medication_request
    
    def reject_request(self, request_id: uuid.UUID, rejection_reason: str) -> MedicationRequest:
        medication_request = self.find_by_id(request_id)
        if not medication_request:
            return None
        
        medication_request.status = 'rejected'
        medication_request.rejection_reason = rejection_reason
        medication_request.updated_at = datetime.now(timezone.utc)
        
        db.session.commit()
        return medication_request
    
    def update_status(self, request_id: uuid.UUID, status: str) -> MedicationRequest:
        medication_request = self.find_by_id(request_id)
        if not medication_request:
            return None
        
        medication_request.status = status
        medication_request.updated_at = datetime.now(timezone.utc)
        
        if status == 'delivered':
            medication_request.delivered_at = datetime.now(timezone.utc)
        
        db.session.commit()
        return medication_request
    
    def cancel_request(self, request_id: uuid.UUID) -> MedicationRequest:
        medication_request = self.find_by_id(request_id)
        if not medication_request:
            return None
        
        medication_request.status = 'cancelled'
        medication_request.updated_at = datetime.now(timezone.utc)
        
        db.session.commit()
        return medication_request
