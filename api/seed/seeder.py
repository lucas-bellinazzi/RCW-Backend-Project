"""
Main seeder script that coordinates all database seeding operations.
Handles database clearing and populating with mock data from individual data files.
"""

from config.database import db
from src.models.user_model import User
from src.models.organization_model import Organization
from src.models.inventory_model import Inventory
from src.models.medication_request_model import MedicationRequest
from sqlalchemy import inspect

from seed.organizations_data import get_organizations_data
from seed.users_data import get_users_data
from seed.inventory_data import get_inventory_data
from seed.medication_requests_data import get_medication_requests_data


def table_exists(table_name):
    """
    Check if a table exists in the database.
    
    Args:
        table_name: Name of the table to check.
    
    Returns:
        Boolean indicating if table exists.
    """
    inspector = inspect(db.engine)
    return table_name in inspector.get_table_names()


def clear_database():
    """Clear all data from the database."""
    print("Clearing database...")
    try:
        # Only delete from tables that exist
        if table_exists('medication_request'):
            MedicationRequest.query.delete()
        if table_exists('inventory'):
            Inventory.query.delete()
        if table_exists('user'):
            User.query.delete()
        if table_exists('organization'):
            Organization.query.delete()
        
        db.session.commit()
        print("✓ Database cleared successfully")
    except Exception as e:
        db.session.rollback()
        print(f"✗ Error clearing database: {str(e)}")
        raise


def seed_organizations():
    """Create mock organizations."""
    print("\nSeeding organizations...")
    
    if not table_exists('organization'):
        print("⚠ Warning: organization table does not exist. Skipping...")
        return []
    
    organizations_data = get_organizations_data()
    
    organizations = []
    for org_data in organizations_data:
        org = Organization(**org_data)
        db.session.add(org)
        organizations.append(org)
    
    db.session.commit()
    print(f"✓ Created {len(organizations)} organizations")
    return organizations


def seed_users(organizations):
    """Create mock users for different organizations and roles."""
    print("\nSeeding users...")
    
    if not table_exists('user'):
        print("⚠ Warning: user table does not exist. Skipping...")
        return []
    
    users_data = get_users_data(organizations)
    
    users = []
    for user_data in users_data:
        user = User(**user_data)
        db.session.add(user)
        users.append(user)
    
    db.session.commit()
    print(f"✓ Created {len(users)} users")
    print("  Default password for all users: 'password123'")
    return users


def seed_inventory(organizations):
    """Create mock inventory items."""
    print("\nSeeding inventory...")
    
    if not table_exists('inventory'):
        print("⚠ Warning: inventory table does not exist. Skipping...")
        return []
    
    inventory_data = get_inventory_data(organizations)
    
    inventory_items = []
    for inv_data in inventory_data:
        inventory = Inventory(**inv_data)
        db.session.add(inventory)
        inventory_items.append(inventory)
    
    db.session.commit()
    print(f"✓ Created {len(inventory_items)} inventory items")
    return inventory_items


def seed_medication_requests(users, organizations):
    """Create mock medication requests."""
    print("\nSeeding medication requests...")
    
    if not table_exists('medication_request'):
        print("⚠ Warning: medication_request table does not exist. Skipping...")
        return []
    
    medication_requests_data = get_medication_requests_data(users, organizations)
    
    medication_requests = []
    for req_data in medication_requests_data:
        request = MedicationRequest(**req_data)
        db.session.add(request)
        medication_requests.append(request)
    
    db.session.commit()
    print(f"✓ Created {len(medication_requests)} medication requests")
    return medication_requests


def print_summary(organizations, users, inventory_items, medication_requests):
    """Print a summary of seeded data."""
    print("\n" + "="*60)
    print("DATABASE SEEDING COMPLETED SUCCESSFULLY")
    print("="*60)
    
    if organizations:
        print(f"\nOrganizations: {len(organizations)}")
        for org in organizations:
            print(f"  - {org.name} ({org.org_id}) - {org.org_type}")
    
    if users:
        print(f"\nUsers: {len(users)}")
        role_counts = {}
        for user in users:
            role_counts[user.role] = role_counts.get(user.role, 0) + 1
        for role, count in role_counts.items():
            print(f"  - {role}: {count}")
    
    if inventory_items:
        print(f"\nInventory Items: {len(inventory_items)}")
        status_counts = {}
        for item in inventory_items:
            status_counts[item.status] = status_counts.get(item.status, 0) + 1
        for status, count in status_counts.items():
            print(f"  - {status}: {count}")
    
    if medication_requests:
        print(f"\nMedication Requests: {len(medication_requests)}")
        request_status_counts = {}
        for req in medication_requests:
            request_status_counts[req.status] = request_status_counts.get(req.status, 0) + 1
        for status, count in request_status_counts.items():
            print(f"  - {status}: {count}")
    
    print("\n" + "="*60)
    print("LOGIN CREDENTIALS (all users):")
    print("  Password: password123")
    print("\nSample login emails:")
    print("  Admin: admin@system.com")
    print("  Manufacturer: john.smith@pharmacorp.com")
    print("  Distributor: michael.chen@medidistro.com")
    print("  Pharmacist: david.brown@communityplus.com")
    print("  Consumer: alice.roberts@email.com")
    print("="*60 + "\n")


def run_seeder():
    """
    Execute all seeding operations.
    
    Returns:
        Tuple of (organizations, users, inventory_items, medication_requests)
    """
    # Clear existing data
    clear_database()
    
    # Seed data in order (respecting foreign key constraints)
    organizations = seed_organizations()
    users = seed_users(organizations)
    inventory_items = seed_inventory(organizations)
    medication_requests = seed_medication_requests(users, organizations)
    
    # Print summary
    print_summary(organizations, users, inventory_items, medication_requests)
    
    return organizations, users, inventory_items, medication_requests
