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


def apply_group_discount(subtotal: float, num_members: int) -> tuple[float, float]:
    if num_members >= 2:
        discount = subtotal * GROUP_DISCOUNT_RATE
        return subtotal - discount, discount
    return subtotal, 0.0


def apply_special_offer(total_after_group: float) -> tuple[float, float]:
    for threshold, discount_amt in SPECIAL_DISCOUNT_THRESHOLDS:
        if total_after_group > threshold:
            return total_after_group - discount_amt, discount_amt
    return total_after_group, 0.0
