from werkzeug.exceptions import NotFound, BadRequest
from src.repositories.blockchain_repository import BlockchainRepository
from src.repositories.inventory_repository import InventoryRepository
from src.services.auth_service import AuthService
from src.utils.constants import UserRole


class BlockchainService:
    def __init__(self, fabric_client):
        self.repository = BlockchainRepository(fabric_client)
        self.inventory_repository = InventoryRepository()
        self.auth_service = AuthService()

    def _get_current_user(self):
        user = self.auth_service.return_user_from_token()
        if user is None:
            raise BadRequest("Authentication required")
        return user

    def create_batch(self, data):
        user = self._get_current_user()
        if user.role not in [UserRole.ADMIN.value, UserRole.MANUFACTURER.value]:
            raise BadRequest("You are not allowed to create batches")

        if not data:
            raise BadRequest("Invalid payload")

        # Create batch on blockchain
        blockchain_result = self.repository.create_batch(data)
        
        # Also add to inventory if organization_id is provided
        if user.organization_id and "unit_price" in data:
            try:
                inventory_data = {
                    'organization_id': user.organization_id,
                    'batch_id': data['batch_id'],
                    'product_name': data['product_name'],
                    'available_quantity': data['total_quantity'],
                    'unit_dosage': data['unit_dosage'],
                    'manufacture_date': data['manufacture_date'],
                    'expiry_date': data['expiry_date'],
                    'unit_price': data['unit_price']
                }
                self.inventory_repository.create(inventory_data)
            except Exception as e:
                # Log error but don't fail the batch creation
                print(f"Warning: Could not add to inventory: {str(e)}")
        
        return blockchain_result

    def transfer_batch(self, data):
        user = self._get_current_user()
        if user.role not in [
            UserRole.ADMIN.value,
            UserRole.MANUFACTURER.value,
            UserRole.DISTRIBUTOR.value,
            UserRole.PHARMACIST.value,
        ]:
            raise BadRequest("You are not allowed to transfer batches")

        if not data:
            raise BadRequest("Invalid payload")

        return self.repository.transfer_batch(data)

    def mark_batch_delivered(self, data):
        user = self._get_current_user()
        if user.role not in [UserRole.ADMIN.value, UserRole.PHARMACIST.value]:
            raise BadRequest("You are not allowed to mark delivery")

        if "batch_id" not in data or "delivered_to_org_id" not in data or "quantity" not in data:
            raise BadRequest("batch_id, delivered_to_org_id and quantity are required")

        return self.repository.mark_batch_delivered(
            data["batch_id"], data["delivered_to_org_id"], data["quantity"]
        )

    def get_batch(self, batch_id: str):
        # You can decide: allow all authenticated users
        user = self._get_current_user()
        result = self.repository.get_batch(batch_id)
        if not result:
            raise NotFound("Batch not found")
        return result

    def get_batch_history(self, batch_id: str):
        user = self._get_current_user()
        return self.repository.get_batch_history(batch_id)
