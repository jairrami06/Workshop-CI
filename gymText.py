import unittest
from gym import (
    validate_plan,
    validate_features,
    calculate_subtotal,
    apply_group_discount,
    apply_special_offer,
    needs_premium_surcharge,
    apply_premium_surcharge,
    calculate_final_cost,
    ValidationError,
)


class TestGymLogic(unittest.TestCase):
    def test_validate_plan_valid(self):
        for p in ["Basic", "Premium", "Family"]:
            validate_plan(p)

    def test_validate_plan_invalid(self):
        with self.assertRaises(ValidationError) as cm:
            validate_plan("Gold")
        self.assertIn("Plan 'Gold' is not available", str(cm.exception))

    def test_validate_features_empty(self):
        validate_features([])

    def test_validate_features_valid(self):
        validate_features(["Personal Training", "Sauna Access"])

    def test_validate_features_invalid(self):
        with self.assertRaises(ValidationError) as cm:
            validate_features(["Personal Training", "Swimming"])
        self.assertIn("Feature(s) not available: Swimming", str(cm.exception))
        
    def test_calculate_subtotal_no_features_one_member(self):
        subtotal = calculate_subtotal("Basic", [], 1)
        self.assertEqual(subtotal, 100.0)

    def test_calculate_subtotal_with_features_multiple_members(self):
        subtotal = calculate_subtotal(
            "Premium", ["Personal Training", "Group Classes"], 2
        )
        self.assertEqual(subtotal, 460.0)