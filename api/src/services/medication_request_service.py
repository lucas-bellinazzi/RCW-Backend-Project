from werkzeug.exceptions import NotFound, BadRequest, Forbidden
from src.repositories.medication_request_repository import MedicationRequestRepository
from src.repositories.inventory_repository import InventoryRepository
from src.repositories.notification_repository import NotificationRepository
from src.repositories.organization_repository import OrganizationRepository
from src.services.auth_service import AuthService
from src.utils.constants import UserRole


class MedicationRequestService:
    def __init__(self):
        self.repository = MedicationRequestRepository()
        self.inventory_repository = InventoryRepository()
        self.notification_repository = NotificationRepository()
        self.organization_repository = OrganizationRepository()
        self.auth_service = AuthService()

    def _get_current_user(self):
        user = self.auth_service.return_user_from_token()
        if user is None:
            raise BadRequest("Authentication required")
        return user

    def create_request(self, data):
        user = self._get_current_user()
        
        if user.role != UserRole.CONSUMER.value:
            raise BadRequest("Only consumers can create medication requests")
        
        # Create the request
        medication_request = self.repository.create(data, user.id)
        
        # Notify all manufacturers about the new request
        manufacturers = self.organization_repository.find_by_type('manufacturer')
        for manufacturer in manufacturers:
            # Find users from this manufacturer organization
            for manufacturer_user in manufacturer.users:
                if manufacturer_user.role == UserRole.MANUFACTURER.value:
                    self.notification_repository.create({
                        'user_id': manufacturer_user.id,
                        'title': 'Nova Solicitação de Medicamento',
                        'message': f'Nova solicitação #{medication_request.request_number} para {medication_request.product_name} - Quantidade: {medication_request.requested_quantity}',
                        'notification_type': 'request_created',
                        'related_entity_type': 'medication_request',
                        'related_entity_id': str(medication_request.id)
                    })
        
        return medication_request
    
    def get_my_requests(self):
        user = self._get_current_user()
        
        if user.role == UserRole.CONSUMER.value:
            return self.repository.find_by_consumer(user.id)
        elif user.role == UserRole.MANUFACTURER.value:
            if not user.organization_id:
                raise BadRequest("User not associated with an organization")
            return self.repository.find_by_manufacturer(user.organization_id)
        elif user.role == UserRole.ADMIN.value:
            return self.repository.find_pending_requests()
        else:
            raise Forbidden("You don't have permission to view requests")
    
    def get_request_by_id(self, request_id):
        user = self._get_current_user()
        medication_request = self.repository.find_by_id(request_id)
        
        if not medication_request:
            raise NotFound("Medication request not found")
        
        # Check permissions
        if user.role == UserRole.CONSUMER.value and medication_request.consumer_id != user.id:
            raise Forbidden("You can only view your own requests")
        
        return medication_request
    
    def approve_request(self, request_id, data):
        user = self._get_current_user()
        
        if user.role not in [UserRole.ADMIN.value, UserRole.MANUFACTURER.value]:
            raise BadRequest("Only manufacturers or admins can approve requests")
        
        medication_request = self.repository.find_by_id(request_id)
        if not medication_request:
            raise NotFound("Medication request not found")
        
        if medication_request.status != 'pending':
            raise BadRequest(f"Request is already {medication_request.status}")
        
        # Check inventory availability
        inventory = self.inventory_repository.find_by_batch_id(data['batch_id'])
        if not inventory:
            raise NotFound("Batch not found in inventory")
        
        if inventory.available_quantity < medication_request.requested_quantity:
            raise BadRequest("Insufficient quantity in inventory")
        
        # Reserve the quantity
        self.inventory_repository.reserve_quantity(data['batch_id'], medication_request.requested_quantity)
        
        # Approve the request
        approved_request = self.repository.approve_request(
            request_id,
            user.id,
            data['batch_id'],
            data['assigned_manufacturer_id']
        )
        
        # Notify consumer
        self.notification_repository.create({
            'user_id': medication_request.consumer_id,
            'title': 'Solicitação Aprovada',
            'message': f'Sua solicitação #{medication_request.request_number} foi aprovada e será processada em breve.',
            'notification_type': 'request_approved',
            'related_entity_type': 'medication_request',
            'related_entity_id': str(medication_request.id)
        })
        
        return approved_request
    
    def reject_request(self, request_id, data):
        user = self._get_current_user()
        
        if user.role not in [UserRole.ADMIN.value, UserRole.MANUFACTURER.value]:
            raise BadRequest("Only manufacturers or admins can reject requests")
        
        medication_request = self.repository.find_by_id(request_id)
        if not medication_request:
            raise NotFound("Medication request not found")
        
        if medication_request.status != 'pending':
            raise BadRequest(f"Request is already {medication_request.status}")
        
        rejected_request = self.repository.reject_request(request_id, data['rejection_reason'])
        
        # Notify consumer
        self.notification_repository.create({
            'user_id': medication_request.consumer_id,
            'title': 'Solicitação Rejeitada',
            'message': f'Sua solicitação #{medication_request.request_number} foi rejeitada. Motivo: {data["rejection_reason"]}',
            'notification_type': 'request_rejected',
            'related_entity_type': 'medication_request',
            'related_entity_id': str(medication_request.id)
        })
        
        return rejected_request
    
    def cancel_request(self, request_id):
        user = self._get_current_user()
        medication_request = self.repository.find_by_id(request_id)
        
        if not medication_request:
            raise NotFound("Medication request not found")
        
        # Only consumer who created or admin can cancel
        if user.role != UserRole.ADMIN.value and medication_request.consumer_id != user.id:
            raise Forbidden("You can only cancel your own requests")
        
        if medication_request.status not in ['pending', 'approved']:
            raise BadRequest(f"Cannot cancel request with status {medication_request.status}")
        
        # If approved, release reserved quantity
        if medication_request.status == 'approved' and medication_request.batch_id:
            inventory = self.inventory_repository.find_by_batch_id(medication_request.batch_id)
            if inventory:
                inventory.reserved_quantity -= medication_request.requested_quantity
                inventory.available_quantity += medication_request.requested_quantity
        
        return self.repository.cancel_request(request_id)
