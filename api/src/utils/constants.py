from enum import Enum

class UserRole(Enum):
    ADMIN = 'admin'
    GUEST = 'guest'
    MANUFACTURER = 'manufacturer'
    DISTRIBUTOR = 'distributor'
    PHARMACIST = 'pharmacist'
    CONSUMER = 'consumer'

class UserStatus(Enum):
    ACTIVE = 'active'
    INACTIVE = 'inactive'

class AllowedPaymentMethods(Enum):
    PIX = 'pix'
    CREDIT_CARD = 'credit_card'
    DEBIT_CARD = 'debit_card'
    BILLET = 'billet'

class AllowedPaymentStatus(Enum):
    APPROVED = 'approved'
    REJECTED = 'rejected'
    PENDING = 'pending'
    FAILED = 'failed'

class RequestSource(Enum):
    DASHBOARD = 'dashboard'

class ENVIRONMENTS(Enum):
    LOCAL = 'local'
    PRODUCTION = 'production'
