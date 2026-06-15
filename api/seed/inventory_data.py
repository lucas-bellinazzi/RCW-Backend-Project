"""
Mock data for inventory table.
"""


def get_inventory_data(organizations):
    """
    Return list of inventory mock data.
    
    Args:
        organizations: List of Organization objects to link inventory to.
    
    Returns:
        List of inventory dictionaries with mock data.
    """
    # Get manufacturer organizations
    manufacturers = [org for org in organizations if org.org_type == 'manufacturer']
    
    return [
        # PharmaCorp inventory
        {
            'organization_id': manufacturers[0].id,
            'batch_id': 'BTH-2024-001',
            'product_name': 'Amoxicillin 500mg',
            'available_quantity': 10000,
            'reserved_quantity': 500,
            'unit_dosage': '500mg',
            'manufacture_date': '2024-01-15',
            'expiry_date': '2026-01-15',
            'unit_price': 2.50,
            'status': 'available'
        },
        {
            'organization_id': manufacturers[0].id,
            'batch_id': 'BTH-2024-002',
            'product_name': 'Ibuprofen 400mg',
            'available_quantity': 15000,
            'reserved_quantity': 200,
            'unit_dosage': '400mg',
            'manufacture_date': '2024-02-20',
            'expiry_date': '2026-02-20',
            'unit_price': 1.75,
            'status': 'available'
        },
        {
            'organization_id': manufacturers[0].id,
            'batch_id': 'BTH-2024-003',
            'product_name': 'Metformin 850mg',
            'available_quantity': 8000,
            'reserved_quantity': 1000,
            'unit_dosage': '850mg',
            'manufacture_date': '2024-03-10',
            'expiry_date': '2026-03-10',
            'unit_price': 3.20,
            'status': 'available'
        },
        # BioMed inventory
        {
            'organization_id': manufacturers[1].id,
            'batch_id': 'BIO-2024-101',
            'product_name': 'Atorvastatin 20mg',
            'available_quantity': 12000,
            'reserved_quantity': 300,
            'unit_dosage': '20mg',
            'manufacture_date': '2024-01-25',
            'expiry_date': '2026-01-25',
            'unit_price': 4.50,
            'status': 'available'
        },
        {
            'organization_id': manufacturers[1].id,
            'batch_id': 'BIO-2024-102',
            'product_name': 'Lisinopril 10mg',
            'available_quantity': 9000,
            'reserved_quantity': 600,
            'unit_dosage': '10mg',
            'manufacture_date': '2024-02-15',
            'expiry_date': '2026-02-15',
            'unit_price': 2.80,
            'status': 'available'
        },
        {
            'organization_id': manufacturers[1].id,
            'batch_id': 'BIO-2024-103',
            'product_name': 'Omeprazole 20mg',
            'available_quantity': 500,
            'reserved_quantity': 100,
            'unit_dosage': '20mg',
            'manufacture_date': '2024-03-05',
            'expiry_date': '2026-03-05',
            'unit_price': 3.75,
            'status': 'low_stock'
        },
        {
            'organization_id': manufacturers[1].id,
            'batch_id': 'BIO-2024-104',
            'product_name': 'Levothyroxine 50mcg',
            'available_quantity': 0,
            'reserved_quantity': 0,
            'unit_dosage': '50mcg',
            'manufacture_date': '2024-04-01',
            'expiry_date': '2026-04-01',
            'unit_price': 5.20,
            'status': 'out_of_stock'
        }
    ]
