"""
Mock data for organizations table.
"""

def get_organizations_data():
    """Return list of organization mock data."""
    return [
        {
            'org_id': 'MFR001',
            'name': 'PharmaCorp Manufacturing',
            'org_type': 'manufacturer',
            'address': '123 Industrial Blvd, Montreal, QC H3A 1A1',
            'contact_email': 'contact@pharmacorp.com',
            'contact_phone': '+1-514-555-0101',
            'status': 'active'
        },
        {
            'org_id': 'MFR002',
            'name': 'BioMed Industries',
            'org_type': 'manufacturer',
            'address': '456 Science Park, Toronto, ON M5H 2N2',
            'contact_email': 'info@biomed.com',
            'contact_phone': '+1-416-555-0102',
            'status': 'active'
        },
        {
            'org_id': 'DST001',
            'name': 'MediDistro Canada',
            'org_type': 'distributor',
            'address': '789 Logistics Way, Vancouver, BC V6B 1A1',
            'contact_email': 'operations@medidistro.com',
            'contact_phone': '+1-604-555-0201',
            'status': 'active'
        },
        {
            'org_id': 'DST002',
            'name': 'HealthSupply Networks',
            'org_type': 'distributor',
            'address': '321 Distribution Center, Calgary, AB T2P 1B4',
            'contact_email': 'logistics@healthsupply.com',
            'contact_phone': '+1-403-555-0202',
            'status': 'active'
        },
        {
            'org_id': 'PHM001',
            'name': 'Community Pharmacy Plus',
            'org_type': 'pharmacy',
            'address': '567 Main Street, Ottawa, ON K1A 0A1',
            'contact_email': 'pharmacy@communityplus.com',
            'contact_phone': '+1-613-555-0301',
            'status': 'active'
        },
        {
            'org_id': 'PHM002',
            'name': 'HealthFirst Pharmacy',
            'org_type': 'pharmacy',
            'address': '890 Health Ave, Quebec City, QC G1R 1A1',
            'contact_email': 'contact@healthfirst.com',
            'contact_phone': '+1-418-555-0302',
            'status': 'active'
        }
    ]
