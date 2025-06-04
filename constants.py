MEMBERSHIP_PLANS = {
    "Basic": {
        "base_cost": 100.0,
        "description": "Access to gym equipment and locker room.",
    },
    "Premium": {
        "base_cost": 150.0,
        "description": "Includes Basic benefits + access to premium facilities.",
    },
    "Family": {
        "base_cost": 200.0,
        "description": "Up to 4 family members under one plan.",
    },
}

ADDITIONAL_FEATURES = {
    "Personal Training": {
        "cost": 50.0,
        "is_premium_feature": False,
        "description": "One-on-one sessions with a certified trainer.",
    },
    "Group Classes": {
        "cost": 30.0,
        "is_premium_feature": False,
        "description": "Unlimited group fitness classes.",
    },
    "Sauna Access": {
        "cost": 25.0,
        "is_premium_feature": True,
        "description": "Access to sauna and steam room.",
    },
    "Specialized Training Program": {
        "cost": 100.0,
        "is_premium_feature": True,
        "description": "Custom training program designed by experts.",
    },
}

GROUP_DISCOUNT_RATE = 0.10
SPECIAL_DISCOUNT_THRESHOLDS = [
    (400.0, 50.0),
    (200.0, 20.0),
]
PREMIUM_SURCHARGE_RATE = 0.15
