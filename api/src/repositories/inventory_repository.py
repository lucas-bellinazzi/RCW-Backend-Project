from config.database import db
from src.models.inventory_model import Inventory
from typing import Optional, List
import uuid


class InventoryRepository:
    def create(self, data: dict) -> Inventory:
        inventory = Inventory(
            organization_id=data['organization_id'],
            batch_id=data['batch_id'],
            product_name=data['product_name'],
            available_quantity=data['available_quantity'],
            reserved_quantity=0,
            unit_dosage=data['unit_dosage'],
            manufacture_date=data['manufacture_date'],
            expiry_date=data['expiry_date'],
            unit_price=data['unit_price'],
            status='available'
        )
        
        db.session.add(inventory)
        db.session.commit()
        return inventory
    
    def find_by_id(self, inventory_id: uuid.UUID) -> Optional[Inventory]:
        return Inventory.query.filter_by(id=inventory_id).first()
    
    def find_by_batch_id(self, batch_id: str) -> Optional[Inventory]:
        return Inventory.query.filter_by(batch_id=batch_id).first()
    
    def find_by_organization(self, organization_id: uuid.UUID) -> List[Inventory]:
        return Inventory.query.filter_by(organization_id=organization_id).order_by(Inventory.created_at.desc()).all()
    
    def find_available_by_product(self, product_name: str, min_quantity: int) -> List[Inventory]:
        return Inventory.query.filter(
            Inventory.product_name.ilike(f'%{product_name}%'),
            Inventory.available_quantity >= min_quantity,
            Inventory.status == 'available'
        ).all()
    
    def update_quantity(self, batch_id: str, quantity_change: int) -> Optional[Inventory]:
        inventory = self.find_by_batch_id(batch_id)
        if not inventory:
            return None
        
        inventory.available_quantity += quantity_change
        
        # Update status based on quantity
        if inventory.available_quantity == 0:
            inventory.status = 'out_of_stock'
        elif inventory.available_quantity < 10:  # threshold can be configurable
            inventory.status = 'low_stock'
        else:
            inventory.status = 'available'
        
        db.session.commit()
        return inventory
    
    def reserve_quantity(self, batch_id: str, quantity: int) -> Optional[Inventory]:
        inventory = self.find_by_batch_id(batch_id)
        if not inventory or inventory.available_quantity < quantity:
            return None
        
        inventory.available_quantity -= quantity
        inventory.reserved_quantity += quantity
        
        if inventory.available_quantity == 0:
            inventory.status = 'out_of_stock'
        elif inventory.available_quantity < 10:
            inventory.status = 'low_stock'
        
        db.session.commit()
        return inventory
    
    def release_reserved_quantity(self, batch_id: str, quantity: int) -> Optional[Inventory]:
        inventory = self.find_by_batch_id(batch_id)
        if not inventory or inventory.reserved_quantity < quantity:
            return None
        
        inventory.reserved_quantity -= quantity
        # Quantity is actually shipped, so don't add back to available
        
        db.session.commit()
        return inventory
    
    def delete(self, inventory_id: uuid.UUID) -> bool:
        inventory = self.find_by_id(inventory_id)
        if not inventory:
            return False
        
        db.session.delete(inventory)
        db.session.commit()
        return True
