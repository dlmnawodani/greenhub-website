from aenum import Enum, auto, unique

@unique
class UserRole(Enum):
    """Enum for user roles"""
    ADMIN = "ADMIN" # auto()
    GUEST = "GUEST" # auto()

__all__ = [
    'UserRole'
]

