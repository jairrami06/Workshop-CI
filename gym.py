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


def apply_premium_surcharge(total_before_surcharge: float) -> tuple[float, float]:
    surcharge = total_before_surcharge * PREMIUM_SURCHARGE_RATE
    return total_before_surcharge + surcharge, surcharge


def needs_premium_surcharge(plan_name: str, feature_list: list[str]) -> bool:
    if plan_name == "Premium":
        return True
    return any(ADDITIONAL_FEATURES[feat]["is_premium_feature"] for feat in feature_list)


def calculate_subtotal(
    plan_name: str, feature_list: list[str], num_members: int
) -> float:
    base = MEMBERSHIP_PLANS[plan_name]["base_cost"]
    features_cost = sum(ADDITIONAL_FEATURES[feat]["cost"] for feat in feature_list)
    return (base + features_cost) * num_members


def calculate_final_cost(
    plan_name: str, feature_list: list[str], num_members: int
) -> dict:
    validate_plan(plan_name)
    validate_features(feature_list)
    if num_members < 1:
        raise ValidationError("Number of members must be at least 1.")
    subtotal = calculate_subtotal(plan_name, feature_list, num_members)
    after_group, grp_disc = apply_group_discount(subtotal, num_members)
    after_special, spec_disc = apply_special_offer(after_group)
    surcharge = 0.0
    if needs_premium_surcharge(plan_name, feature_list):
        after_special, surcharge = apply_premium_surcharge(after_special)
    final_total = round(after_special, 2)
    if final_total < 0:
        raise ValidationError("Final total negative.")
    return {
        "subtotal": round(subtotal, 2),
        "group_discount": round(grp_disc, 2),
        "special_discount": round(spec_disc, 2),
        "surcharge": round(surcharge, 2),
        "final_total": final_total,
    }


def prompt_plan_selection() -> str:
    display = "\n".join(
        f"  - {n} (${i['base_cost']:.2f}): {i['description']}"
        for n, i in MEMBERSHIP_PLANS.items()
    )
    print(f"Available Membership Plans:\n{display}")
    plan = input("Enter the plan you want: ").strip()
    try:
        validate_plan(plan)
    except ValidationError as e:
        print(f"ERROR: {e}")
        return prompt_plan_selection()
    return plan


def prompt_features_selection() -> list[str]:
    display = "\n".join(
        f"  - {n} (${i['cost']:.2f}){' (Premium Feature)' if i['is_premium_feature'] else ''}: {i['description']}"
        for n, i in ADDITIONAL_FEATURES.items()
    )
    print(
        f"\nAvailable Additional Features:\n{display}\nType feature names separated by commas, or leave empty if none."
    )
    raw = input("Enter features: ").strip()
    if not raw:
        return []
    chosen = [f.strip() for f in raw.split(",") if f.strip()]
    try:
        validate_features(chosen)
    except ValidationError as e:
        print(f"ERROR: {e}")
        return prompt_features_selection()
    return chosen


def prompt_num_members() -> int:
    raw = input("\nEnter number of members signing up together: ").strip()
    if not raw.isdigit() or int(raw) < 1:
        print("ERROR: Must enter a positive integer ≥ 1.")
        return prompt_num_members()
    return int(raw)


def resumen(
    plan_name: str, feature_list: list[str], num_members: int, breakdown: dict
) -> str:
    group_discount_str = (
        f"Group Discount: -${breakdown['group_discount']:.2f}\n"
        if breakdown['group_discount'] > 0
        else ""
    )
    special_discount_str = (
        f"Special Discount: -${breakdown['special_discount']:.2f}\n"
        if breakdown['special_discount'] > 0
        else ""
    )
    surcharge_str = (
        f"Premium Surcharge: +${breakdown['surcharge']:.2f}\n"
        if breakdown['surcharge'] > 0
        else ""
    )
    return (
        f"\n----- Membership Summary -----\n"
        f"Plan: {plan_name}\n"
        f"Additional Features: {', '.join(feature_list) if feature_list else 'None'}\n"
        f"Number of Members: {num_members}\n"
        f"Subtotal: ${breakdown['subtotal']:.2f}\n"
        f"{group_discount_str}"
        f"{special_discount_str}"
        f"{surcharge_str}"
        f"Final Total: ${breakdown['final_total']:.2f}\n"
        f"------------------------------"
    )


def confirm_and_finalize(
    plan_name: str, feature_list: list[str], num_members: int, breakdown: dict
) -> int:
    s = resumen(plan_name, feature_list, num_members, breakdown)
    print(s)
    a = input("Confirm membership? (y/n): ").strip().lower()
    return (
        int(breakdown["final_total"])
        if a == "y"
        and (
            print(
                f"Membership confirmed. Total amount due: ${breakdown['final_total']:.2f}"
            )
            or True
        )
        else (print("Membership canceled. No charges applied.") or -1)
    )
