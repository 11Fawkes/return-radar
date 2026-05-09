# ============================================================
# benchmarks.py
# All static reference data for Return Radar
# Sources: McKinsey, Bitkom, NRF, Zalando corporate reports
# ============================================================

# ----------------------------------------------------------
# CATEGORY BENCHMARKS
# avg_return_rate : industry average return rate for category
# bracket_buy_risk: likelihood customers order multiple sizes
# ----------------------------------------------------------
CATEGORY_BENCHMARKS = {
    "Dresses": {
        "avg_return_rate": 0.38,
        "bracket_buy_risk": "high"
    },
    "Tops & Shirts": {
        "avg_return_rate": 0.32,
        "bracket_buy_risk": "medium"
    },
    "Trousers & Jeans": {
        "avg_return_rate": 0.35,
        "bracket_buy_risk": "high"
    },
    "Shoes": {
        "avg_return_rate": 0.35,
        "bracket_buy_risk": "medium"
    },
    "Accessories": {
        "avg_return_rate": 0.12,
        "bracket_buy_risk": "low"
    },
    "Sportswear": {
        "avg_return_rate": 0.28,
        "bracket_buy_risk": "medium"
    },
    "Other": {
        "avg_return_rate": 0.25,
        "bracket_buy_risk": "low"
    },
}

# ----------------------------------------------------------
# FINANCIAL CONSTANTS
# ----------------------------------------------------------
HOLDING_COST_RATE  = 0.03   # 3% of product value per month (industry midpoint)
SECONDARY_DISCOUNT = 0.40   # 40% discount when selling on secondary market
RESALE_VELOCITY    = 0.60   # 60% of backlog resold/disposed per month

# ----------------------------------------------------------
# ZALANDO PENALTY THRESHOLDS (estimated from policy language)
# ----------------------------------------------------------
THRESHOLD_MONITOR  = 0.40   # Above this = Monitor (amber)
THRESHOLD_ACTION   = 0.50   # Above this = Action Required (red)

# ----------------------------------------------------------
# RECOMMENDATION ACTION LIBRARY
# 12 possible actions — tool picks top 3 based on user inputs
# Each action has:
#   title       : short headline
#   explanation : 2-sentence plain English description
#   impact      : "High" / "Medium" / "Low"
#   priority    : 1 (highest) to 3 (lowest) — used for sorting
# ----------------------------------------------------------
ACTION_LIBRARY = [
    {
        "id": "size_guide",
        "title": "Upgrade your size guide immediately",
        "explanation": (
            "Sizing issues cause 70% of fashion returns. "
            "Switching from generic S/M/L labels to exact measurements in cm "
            "can reduce return rates by 15–20% within 60 days."
        ),
        "impact": "High",
        "priority": 1,
        "trigger": lambda cat, price, rate, score: (
            cat in ["Dresses", "Tops & Shirts", "Trousers & Jeans"] and rate > 0.30
        ),
    },
    {
        "id": "product_video",
        "title": "Add product videos to your listings",
        "explanation": (
            "Zalando's own data shows video product pages reduce returns by 15–25%. "
            "A 30-second video showing fit, fabric movement, and true colour is your "
            "fastest lever for reducing returns without changing the product itself."
        ),
        "impact": "High",
        "priority": 1,
        "trigger": lambda cat, price, rate, score: rate > 0.35 or score > 60,
    },
    {
        "id": "secondary_market",
        "title": "Route backlog stock to a secondary market",
        "explanation": (
            "Your returned inventory is accumulating holding costs every day it sits unsold. "
            "Listing on Vinted, Back Market, or your own outlet at a 30–40% discount "
            "recovers cash faster than waiting for full-price resale."
        ),
        "impact": "High",
        "priority": 1,
        "trigger": lambda cat, price, rate, score: rate > 0.40 and price > 30,
    },
    {
        "id": "penalty_warning",
        "title": "You are approaching Zalando's penalty threshold",
        "explanation": (
            "Zalando begins reducing seller visibility when return rates consistently exceed 40%. "
            "At your current rate you risk receiving a formal warning — "
            "which means fewer customers will even see your products."
        ),
        "impact": "High",
        "priority": 1,
        "trigger": lambda cat, price, rate, score: rate >= 0.40,
    },
    {
        "id": "bracket_buying",
        "title": "Address bracket-buying behaviour",
        "explanation": (
            "29% of German online shoppers intentionally order multiple sizes to try at home. "
            "Adding a 'find your size' quiz or a fit consultation option directly on your "
            "listing page can reduce this behaviour by 10–15%."
        ),
        "impact": "Medium",
        "priority": 2,
        "trigger": lambda cat, price, rate, score: (
            CATEGORY_BENCHMARKS.get(cat, {}).get("bracket_buy_risk") == "high"
            and rate > 0.30
        ),
    },
    {
        "id": "product_descriptions",
        "title": "Rewrite your product descriptions with return data in mind",
        "explanation": (
            "Vague descriptions like 'relaxed fit' or 'true to size' are the leading cause "
            "of expectation mismatch. Rewrite descriptions to include exact measurements, "
            "fabric weight, and model height/size worn."
        ),
        "impact": "Medium",
        "priority": 2,
        "trigger": lambda cat, price, rate, score: rate > 0.28,
    },
    {
        "id": "seasonal_clearance",
        "title": "Plan a seasonal clearance for returned stock",
        "explanation": (
            "Fashion items lose 10–15% of their resale value every month they sit in warehouse. "
            "A structured clearance sale every 60 days prevents dead stock from compounding "
            "into a larger write-off at end of season."
        ),
        "impact": "Medium",
        "priority": 2,
        "trigger": lambda cat, price, rate, score: rate > 0.30 and price < 80,
    },
    {
        "id": "price_anchor",
        "title": "Review your pricing relative to return cost",
        "explanation": (
            "At your price point, each return costs approximately the same as your margin "
            "on 1–2 successful sales. Building a small return cost buffer into your pricing "
            "protects profitability without changing your return rate."
        ),
        "impact": "Medium",
        "priority": 2,
        "trigger": lambda cat, price, rate, score: price > 100 and rate > 0.25,
    },
    {
        "id": "benchmark_advantage",
        "title": "Your return rate is a competitive advantage — use it",
        "explanation": (
            "Your return rate is below the industry average for your category. "
            "This is rare and valuable. Mention it in your Zalando brand profile "
            "and use it in supplier and retail partnership negotiations."
        ),
        "impact": "Medium",
        "priority": 2,
        "trigger": lambda cat, price, rate, score: (
            rate < CATEGORY_BENCHMARKS.get(cat, {}).get("avg_return_rate", 0.25) * 0.85
        ),
    },
    {
        "id": "inspection_process",
        "title": "Build a faster returned-item inspection process",
        "explanation": (
            "The longer a returned item takes to be inspected and relisted, the more value it loses. "
            "A simple checklist-based inspection process targeting same-day or next-day "
            "re-listing can recover 20–30% more value from your return volume."
        ),
        "impact": "Low",
        "priority": 3,
        "trigger": lambda cat, price, rate, score: rate > 0.20,
    },
    {
        "id": "customer_feedback",
        "title": "Collect structured return reason data from customers",
        "explanation": (
            "Most sellers only see that a return happened — not why. "
            "Adding a mandatory 3-option return reason selector to your post-purchase "
            "flow gives you the data to fix the root cause, not just manage the symptom."
        ),
        "impact": "Low",
        "priority": 3,
        "trigger": lambda cat, price, rate, score: True,  # always relevant
    },
    {
        "id": "zalando_tools",
        "title": "Use Zalando's free fit and size tools for your listings",
        "explanation": (
            "Zalando offers free 360-degree imagery, size advice widgets, and augmented reality "
            "fitting features to partner brands. Many small sellers never activate these. "
            "Enabling them costs nothing and can reduce sizing-related returns by up to 25%."
        ),
        "impact": "Low",
        "priority": 3,
        "trigger": lambda cat, price, rate, score: True,  # always relevant
    },
]