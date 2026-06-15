"""
Mock data for users table.
"""
from werkzeug.security import generate_password_hash


def get_users_data(organizations):
    """
    Return list of user mock data.
    
    Args:
        organizations: List of Organization objects to link users to.
    
    Returns:
        List of user dictionaries with mock data.
    """
    # Password hash for 'password123'
    default_password = generate_password_hash('password123')
    
    return [
        # Admin users
        {
            'name': 'System Administrator',
            'email': 'admin@system.com',
            'phone': '+1-514-555-9999',
            'hashed_password': default_password,
            'role': 'admin',
            'status': 'active',
            'organization_id': None
        },
        # Manufacturer users
        {
            'name': 'John Smith',
            'email': 'john.smith@pharmacorp.com',
            'phone': '+1-514-555-1001',
            'hashed_password': default_password,
            'role': 'manufacturer',
            'status': 'active',
            'organization_id': organizations[0].id  # PharmaCorp
        },
        {
            'name': 'Sarah Johnson',
            'email': 'sarah.johnson@biomed.com',
            'phone': '+1-416-555-1002',
            'hashed_password': default_password,
            'role': 'manufacturer',
            'status': 'active',
            'organization_id': organizations[1].id  # BioMed
        },
        # Distributor users
        {
            'name': 'Michael Chen',
            'email': 'michael.chen@medidistro.com',
            'phone': '+1-604-555-2001',
            'hashed_password': default_password,
            'role': 'distributor',
            'status': 'active',
            'organization_id': organizations[2].id  # MediDistro
        },
        {
            'name': 'Emma Wilson',
            'email': 'emma.wilson@healthsupply.com',
            'phone': '+1-403-555-2002',
            'hashed_password': default_password,
            'role': 'distributor',
            'status': 'active',
            'organization_id': organizations[3].id  # HealthSupply
        },
        # Pharmacy users
        {
            'name': 'David Brown',
            'email': 'david.brown@communityplus.com',
            'phone': '+1-613-555-3001',
            'hashed_password': default_password,
            'role': 'pharmacist',
            'status': 'active',
            'organization_id': organizations[4].id  # Community Pharmacy
        },
        {
            'name': 'Lisa Martin',
            'email': 'lisa.martin@healthfirst.com',
            'phone': '+1-418-555-3002',
            'hashed_password': default_password,
            'role': 'pharmacist',
            'status': 'active',
            'organization_id': organizations[5].id  # HealthFirst
        },
        # Consumer users
        {
            'name': 'Patient Alice Roberts',
            'email': 'alice.roberts@email.com',
            'phone': '+1-514-555-4001',
            'hashed_password': default_password,
            'role': 'consumer',
            'status': 'active',
            'organization_id': None
        },
        {
            'name': 'Patient Bob Anderson',
            'email': 'bob.anderson@email.com',
            'phone': '+1-416-555-4002',
            'hashed_password': default_password,
            'role': 'consumer',
            'status': 'active',
            'organization_id': None
        },
        {
            'name': 'Patient Carol White',
            'email': 'carol.white@email.com',
            'phone': '+1-604-555-4003',
            'hashed_password': default_password,
            'role': 'consumer',
            'status': 'active',
            'organization_id': None
        }
    ]
