"""
Mock data for medication_request table.
"""
from datetime import datetime, timezone, timedelta


def get_medication_requests_data(users, organizations):
    """
    Return list of medication request mock data.
    
    Args:
        users: List of User objects to link requests to.
        organizations: List of Organization objects to link requests to.
    
    Returns:
        List of medication request dictionaries with mock data.
    """
    # Get consumer users
    consumers = [user for user in users if user.role == 'consumer']
    # Get pharmacist users for approvals
    pharmacists = [user for user in users if user.role == 'pharmacist']
    # Get manufacturer organizations
    manufacturers = [org for org in organizations if org.org_type == 'manufacturer']
    
    now = datetime.now(timezone.utc)
    
    return [
        # Pending request
        {
            'request_number': 'REQ-2024-001',
            'consumer_id': consumers[0].id,
            'product_name': 'Amoxicillin 500mg',
            'requested_quantity': 30,
            'unit_dosage': '500mg',
            'prescription_required': True,
            'prescription_document': 'https://prescriptions.example.com/doc/001.pdf',
            'status': 'pending',
            'assigned_manufacturer_id': None,
            'batch_id': None
        },
        # Approved request
        {
            'request_number': 'REQ-2024-002',
            'consumer_id': consumers[1].id,
            'product_name': 'Ibuprofen 400mg',
            'requested_quantity': 60,
            'unit_dosage': '400mg',
            'prescription_required': False,
            'prescription_document': None,
            'status': 'approved',
            'assigned_manufacturer_id': manufacturers[0].id,
            'batch_id': 'BTH-2024-002',
            'approved_at': now - timedelta(days=2),
            'approved_by': pharmacists[0].id
        },
        # In transit request
        {
            'request_number': 'REQ-2024-003',
            'consumer_id': consumers[2].id,
            'product_name': 'Metformin 850mg',
            'requested_quantity': 90,
            'unit_dosage': '850mg',
            'prescription_required': True,
            'prescription_document': 'https://prescriptions.example.com/doc/003.pdf',
            'status': 'in_transit',
            'assigned_manufacturer_id': manufacturers[0].id,
            'batch_id': 'BTH-2024-003',
            'approved_at': now - timedelta(days=5),
            'approved_by': pharmacists[1].id
        },
        # Delivered request
        {
            'request_number': 'REQ-2024-004',
            'consumer_id': consumers[0].id,
            'product_name': 'Atorvastatin 20mg',
            'requested_quantity': 30,
            'unit_dosage': '20mg',
            'prescription_required': True,
            'prescription_document': 'https://prescriptions.example.com/doc/004.pdf',
            'status': 'delivered',
            'assigned_manufacturer_id': manufacturers[1].id,
            'batch_id': 'BIO-2024-101',
            'approved_at': now - timedelta(days=10),
            'approved_by': pharmacists[0].id,
            'delivered_at': now - timedelta(days=3)
        },
        # Rejected request
        {
            'request_number': 'REQ-2024-005',
            'consumer_id': consumers[1].id,
            'product_name': 'Controlled Substance XYZ',
            'requested_quantity': 100,
            'unit_dosage': '10mg',
            'prescription_required': True,
            'prescription_document': None,
            'status': 'rejected',
            'rejection_reason': 'Invalid prescription or missing documentation',
            'approved_by': pharmacists[1].id
        },
        # Additional pending requests
        {
            'request_number': 'REQ-2024-006',
            'consumer_id': consumers[2].id,
            'product_name': 'Lisinopril 10mg',
            'requested_quantity': 30,
            'unit_dosage': '10mg',
            'prescription_required': True,
            'prescription_document': 'https://prescriptions.example.com/doc/006.pdf',
            'status': 'pending',
            'assigned_manufacturer_id': None,
            'batch_id': None
        },
        {
            'request_number': 'REQ-2024-007',
            'consumer_id': consumers[0].id,
            'product_name': 'Omeprazole 20mg',
            'requested_quantity': 60,
            'unit_dosage': '20mg',
            'prescription_required': False,
            'prescription_document': None,
            'status': 'pending',
            'assigned_manufacturer_id': None,
            'batch_id': None
        }
    ]
