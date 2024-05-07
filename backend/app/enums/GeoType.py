from aenum import Enum, auto, unique

@unique
class GeoType(Enum):
    """Enum for geo types"""
    POINT = "Point" # auto()

__all__ = [
    'GeoType'
]

