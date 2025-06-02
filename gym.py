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


def validate_plan(plan_name: str) -> None:
    if plan_name not in MEMBERSHIP_PLANS:
        raise ValidationError(f"Plan '{plan_name}' is not available.")


def validate_features(feature_list: list[str]) -> None:
    invalid = [feat for feat in feature_list if feat not in ADDITIONAL_FEATURES]
    if invalid:
        raise ValidationError(f"Feature(s) not available: {', '.join(invalid)}")
