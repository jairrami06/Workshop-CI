from constants import (
    MEMBERSHIP_PLANS,
    ADDITIONAL_FEATURES,
    GROUP_DISCOUNT_RATE,
    SPECIAL_DISCOUNT_THRESHOLDS,
    PREMIUM_SURCHARGE_RATE,
)

class ValidationError(Exception):
    """Raised when user input is invalid."""

    pass