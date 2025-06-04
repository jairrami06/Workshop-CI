from gym import (
    prompt_plan_selection,
    prompt_features_selection,
    prompt_num_members,
    calculate_final_cost,
    confirm_and_finalize,
    ValidationError,
)

def main() -> int:
    try:
        plan = prompt_plan_selection()
        features = prompt_features_selection()
        num_members = prompt_num_members()
        breakdown = calculate_final_cost(plan, features, num_members)
        return confirm_and_finalize(plan, features, num_members, breakdown)
    except ValidationError as e:
        print(f"ERROR: {e}")
        return -1
    except KeyboardInterrupt:
        print("\nOperation interrupted by user.")
        return -1


if __name__ == "__main__":
    result = main()
