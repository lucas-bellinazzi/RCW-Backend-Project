from werkzeug.exceptions import NotFound, BadRequest, Forbidden
from src.repositories.inventory_repository import InventoryRepository
from src.repositories.organization_repository import OrganizationRepository
from src.services.auth_service import AuthService
from src.utils.constants import UserRole


class InventoryService:
    def __init__(self):
        self.repository = InventoryRepository()
        self.organization_repository = OrganizationRepository()
        self.auth_service = AuthService()

    def _get_current_user(self):
        user = self.auth_service.return_user_from_token()
        if user is None:
            raise BadRequest("Authentication required")
        return user

    def create_inventory_item(self, data):
        user = self._get_current_user()
        
        if user.role not in [UserRole.ADMIN.value, UserRole.MANUFACTURER.value]:
            raise BadRequest("Only manufacturers or admins can add inventory")
        
        # Verify organization exists
        organization = self.organization_repository.find_by_id(data['organization_id'])
        if not organization:
            raise NotFound("Organization not found")
        
        # Check if user belongs to this organization (unless admin)
        if user.role != UserRole.ADMIN.value and user.organization_id != data['organization_id']:
            raise Forbidden("You can only add inventory to your own organization")
        
        return self.repository.create(data)
    
    def get_my_inventory(self):
        user = self._get_current_user()
        
        if user.role == UserRole.ADMIN.value:
            # Admin can see all inventory items - for now return empty, could be enhanced
            return []
        
        if not user.organization_id:
            raise BadRequest("User not associated with an organization")
        
        return self.repository.find_by_organization(user.organization_id)
    
    def get_inventory_by_organization(self, organization_id):
        user = self._get_current_user()
        
        # Only admin or users from the same organization can view
        if user.role != UserRole.ADMIN.value and user.organization_id != organization_id:
            raise Forbidden("You don't have permission to view this inventory")
        
        return self.repository.find_by_organization(organization_id)
    
    def search_available_inventory(self, product_name, min_quantity):
        user = self._get_current_user()
        
        # All authenticated users can search
        return self.repository.find_available_by_product(product_name, min_quantity)
    
    def update_inventory_quantity(self, batch_id, quantity_change):
        user = self._get_current_user()
        
        if user.role not in [UserRole.ADMIN.value, UserRole.MANUFACTURER.value]:
            raise BadRequest("Only manufacturers or admins can update inventory")
        
        inventory = self.repository.find_by_batch_id(batch_id)
        if not inventory:
            raise NotFound("Inventory item not found")
        
        # Check if user belongs to this organization (unless admin)
        if user.role != UserRole.ADMIN.value and user.organization_id != inventory.organization_id:
            raise Forbidden("You can only update inventory from your own organization")
        
        return self.repository.update_quantity(batch_id, quantity_change)
