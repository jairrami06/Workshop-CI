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
        
    def test_apply_group_discount_single_member(self):
        total, disc = apply_group_discount(150.0, 1)
        self.assertEqual(total, 150.0)
        self.assertEqual(disc, 0.0)

    def test_apply_group_discount_multiple_members(self):
        total, disc = apply_group_discount(300.0, 3)
        self.assertAlmostEqual(disc, 30.0)
        self.assertAlmostEqual(total, 270.0)

    def test_special_offer_none(self):
        total, disc = apply_special_offer(199.99)
        self.assertEqual(total, 199.99)
        self.assertEqual(disc, 0.0)

    def test_special_offer_20(self):
        total, disc = apply_special_offer(250.00)
        self.assertEqual(disc, 20.0)
        self.assertEqual(total, 230.0)

    def test_special_offer_50(self):
        total, disc = apply_special_offer(450.00)
        self.assertEqual(disc, 50.0)
        self.assertEqual(total, 400.0)

    def test_needs_premium_surcharge_due_to_plan(self):
        self.assertTrue(needs_premium_surcharge("Premium", []))

    def test_needs_premium_surcharge_due_to_feature(self):
        self.assertTrue(needs_premium_surcharge("Basic", ["Sauna Access"]))

    def test_needs_premium_surcharge_false(self):
        self.assertFalse(needs_premium_surcharge("Basic", ["Personal Training"]))

    def test_apply_premium_surcharge(self):
        new_total, surcharge = apply_premium_surcharge(200.0)
        self.assertAlmostEqual(surcharge, 30.0)
        self.assertAlmostEqual(new_total, 230.0) 
        
    def test_calculate_final_cost_basic_single(self):
        breakdown = calculate_final_cost("Basic", [], 1)
        self.assertEqual(breakdown["subtotal"], 100.00)
        self.assertEqual(breakdown["group_discount"], 0.00)
        self.assertEqual(breakdown["special_discount"], 0.00)
        self.assertEqual(breakdown["surcharge"], 0.00)
        self.assertEqual(breakdown["final_total"], 100.00)

    def test_calculate_final_cost_group_discount_only(self):
        breakdown = calculate_final_cost("Basic", [], 2)
        self.assertEqual(breakdown["subtotal"], 200.00)
        self.assertEqual(breakdown["group_discount"], 20.00)
        self.assertEqual(breakdown["special_discount"], 0.00)
        self.assertEqual(breakdown["surcharge"], 0.00)
        self.assertEqual(breakdown["final_total"], 180.00)

    def test_calculate_final_cost_special_and_surcharge(self):
        breakdown = calculate_final_cost("Premium", ["Group Classes"], 1)
        self.assertEqual(breakdown["subtotal"], 180.00)
        self.assertEqual(breakdown["group_discount"], 0.00)
        self.assertEqual(breakdown["special_discount"], 0.00)
        self.assertAlmostEqual(breakdown["surcharge"], 27.00)
        self.assertAlmostEqual(breakdown["final_total"], 207.00)

    def test_calculate_final_cost_all_discounts_and_surcharge(self):
        breakdown = calculate_final_cost("Family", ["Sauna Access"], 3)
        self.assertEqual(breakdown["subtotal"], 675.00)
        self.assertAlmostEqual(breakdown["group_discount"], 67.50)
        self.assertAlmostEqual(breakdown["special_discount"], 50.00)
        expected_surcharge = round((607.50 - 50.00) * 0.15, 2)
        self.assertAlmostEqual(breakdown["surcharge"], expected_surcharge)
        expected_final = round((607.50 - 50.00) * 1.15, 2)
        self.assertAlmostEqual(breakdown["final_total"], expected_final)

    def test_calculate_final_cost_invalid_plan(self):
        with self.assertRaises(ValidationError):
            calculate_final_cost("Gold", [], 1)

    def test_calculate_final_cost_invalid_feature(self):
        with self.assertRaises(ValidationError):
            calculate_final_cost("Basic", ["Swimming"], 1)

    def test_calculate_final_cost_invalid_num_members(self):
        with self.assertRaises(ValidationError):
            calculate_final_cost("Basic", [], 0)

    def test_special_offer_exact_thresholds(self):
        total1, disc1 = apply_special_offer(200.00)
        self.assertEqual(disc1, 0.00)
        self.assertEqual(total1, 200.00)

        total2, disc2 = apply_special_offer(400.00)
        self.assertEqual(disc2, 20.00)
        self.assertEqual(total2, 380.00)


if __name__ == "__main__":
    unittest.main()
