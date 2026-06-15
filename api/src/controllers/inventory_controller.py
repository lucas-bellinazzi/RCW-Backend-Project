from flask import jsonify
from src.services.inventory_service import InventoryService
from src.models.inventory_model import (
    inventory_output,
    inventories_output,
    inventory_input_create,
    inventory_input_update
)
from src.utils.api_response import ApiResponse
from marshmallow import ValidationError


class InventoryController:
    def __init__(self):
        self.service = InventoryService()

    def create_inventory_item(self, data):
        try:
            validated_data = inventory_input_create.load(data)
            inventory = self.service.create_inventory_item(validated_data)
            return ApiResponse.response(True, 'Inventory item created successfully', inventory_output.dump(inventory), 201)
        
        except ValidationError as e:
            return ApiResponse.response(False, str(e.messages), None, 400)
        except Exception as e:
            return ApiResponse.response(False, str(e), None, 400)

    def get_my_inventory(self):
        try:
            inventory = self.service.get_my_inventory()
            return ApiResponse.response(True, 'Inventory retrieved successfully', inventories_output.dump(inventory), 200)
        except Exception as e:
            return ApiResponse.response(False, str(e), None, 400)

    def get_inventory_by_organization(self, organization_id):
        try:
            inventory = self.service.get_inventory_by_organization(organization_id)
            return ApiResponse.response(True, 'Inventory retrieved successfully', inventories_output.dump(inventory), 200)
        except Exception as e:
            return ApiResponse.response(False, str(e), None, 400)

    def search_available_inventory(self, product_name, min_quantity=1):
        try:
            inventory = self.service.search_available_inventory(product_name, int(min_quantity))
            return ApiResponse.response(True, 'Inventory search completed', inventories_output.dump(inventory), 200)
        except Exception as e:
            return ApiResponse.response(False, str(e), None, 400)

    def update_inventory_quantity(self, batch_id, data):
        try:
            quantity_change = data.get('quantity_change', 0)
            inventory = self.service.update_inventory_quantity(batch_id, quantity_change)
            return ApiResponse.response(True, 'Inventory updated successfully', inventory_output.dump(inventory), 200)
        except Exception as e:
            return ApiResponse.response(False, str(e), None, 400)
