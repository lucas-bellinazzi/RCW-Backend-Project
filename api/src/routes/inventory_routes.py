from flask import Blueprint, request
from src.controllers.inventory_controller import InventoryController


inventory_bp = Blueprint("inventory_bp", __name__)
inventory_controller = InventoryController()


@inventory_bp.route("/inventory", methods=["POST"])
def create_inventory_item():
    return inventory_controller.create_inventory_item(request.get_json())


@inventory_bp.route("/inventory", methods=["GET"])
def get_my_inventory():
    return inventory_controller.get_my_inventory()


@inventory_bp.route("/inventory/organization/<string:organization_id>", methods=["GET"])
def get_inventory_by_organization(organization_id):
    return inventory_controller.get_inventory_by_organization(organization_id)


@inventory_bp.route("/inventory/search", methods=["GET"])
def search_available_inventory():
    product_name = request.args.get('product_name', '')
    min_quantity = request.args.get('min_quantity', 1)
    return inventory_controller.search_available_inventory(product_name, min_quantity)


@inventory_bp.route("/inventory/<string:batch_id>/quantity", methods=["PATCH"])
def update_inventory_quantity(batch_id):
    return inventory_controller.update_inventory_quantity(batch_id, request.get_json())
