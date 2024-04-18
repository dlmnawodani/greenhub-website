from aenum import Enum, auto, unique

@unique
class OrderStatus(Enum):
    """Enum for order status"""
    PENDING = "PENDING" # auto()  # Order is pending, waiting to be processed [represents the initial state of the order, where it is awaiting processing.]
    PROCESSING = "PROCESSING" # auto()  # Order is being processed [indicates that the order is currently being processed.]
    PARTIALLY_SHIPPED = "PARTIALLY_SHIPPED" # auto()  # Some items in the order have been shipped [signifies that some items in the order have been shipped, but not all.]
    SHIPPED = "SHIPPED" # auto()  # Order has been shipped [means that the entire order has been shipped.]
    DELIVERED = "DELIVERED" # auto()  # Order has been delivered to the customer [indicates that the order has been successfully delivered to the customer.]
    PAYMENT_COMPLETE = "PAYMENT_COMPLETE" # auto()  # Payment for the order is complete [represents the completion of payment for the order.]
    REFUNDED = "REFUNDED" # auto()  # Order has been refunded [indicates that the order has been refunded.]
    CANCELLED = "CANCELLED" # auto()  # Order is cancelled [represents the cancellation of the order.]
    ON_HOLD = "ON_HOLD" # auto()  # Order is on hold, waiting for further action [signifies that the order is on hold, awaiting further action]

__all__ = [
    'OrderStatus'
]

