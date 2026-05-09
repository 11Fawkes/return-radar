# ============================================================
# scoring.py
# Calculates the composite Return Risk Score (0-100)
# ============================================================

from modules.benchmarks import CATEGORY_BENCHMARKS, THRESHOLD_MONITOR, THRESHOLD_ACTION
import math


def calculate_risk_score(category: str, price: float, monthly_units: int, return_rate: float) -> dict:
    """
    Calculates a composite return risk score for a Zalando seller.

    Parameters:
        category      : product category string (must match CATEGORY_BENCHMARKS key)
        price         : product price in EUR
        monthly_units : units sold per month
        return_rate   : return rate as decimal (e.g. 0.38 for 38%)

    Returns a dict with:
        score         : float 0-100 (composite risk)
        band          : str 'Low Risk' | 'Monitor' | 'Action Required'
        benchmark_sub : float 0-100
        threshold_sub : float 0-100
        price_sub     : float 0-100
        volume_sub    : float 0-100
        interpretation: str (2-sentence plain English)
        benchmark_rate: float (category average for reference)
    """

    benchmark = CATEGORY_BENCHMARKS.get(category, {}).get("avg_return_rate", 0.25)

    # ── Sub-score 1: How far above your category benchmark are you? ──
    # 50 = exactly at benchmark, 100 = double the benchmark
    benchmark_sub = min((return_rate / benchmark) * 50, 100) if benchmark > 0 else 50

    # ── Sub-score 2: How close to Zalando's penalty threshold? ──
    if return_rate < 0.30:
        threshold_sub = 10
    elif return_rate < 0.40:
        threshold_sub = 35
    elif return_rate < 0.50:
        threshold_sub = 65
    elif return_rate < 0.60:
        threshold_sub = 85
    else:
        threshold_sub = 100

    # ── Sub-score 3: Price band risk factor ──
    # Higher price = higher return tendency due to purchase anxiety
    if price < 30:
        price_sub = 10
    elif price < 70:
        price_sub = 25
    elif price < 150:
        price_sub = 50
    elif price < 300:
        price_sub = 75
    else:
        price_sub = 90

    # ── Sub-score 4: Volume amplification ──
    # Higher volume = larger absolute backlog even at same rate
    volume_sub = (math.log10(monthly_units + 1) / math.log10(1001)) * 100

    # ── Composite score (weighted) ──
    score = (
        benchmark_sub  * 0.40 +
        threshold_sub  * 0.35 +
        price_sub      * 0.15 +
        volume_sub     * 0.10
    )
    score = round(min(score, 100), 1)

    # ── Risk band ──
    if score < 31:
        band = "Low Risk"
    elif score < 61:
        band = "Monitor"
    else:
        band = "Action Required"

    # ── Plain English interpretation ──
    interpretation = _build_interpretation(score, band, return_rate, benchmark, category)

    return {
        "score":          score,
        "band":           band,
        "benchmark_sub":  round(benchmark_sub, 1),
        "threshold_sub":  round(threshold_sub, 1),
        "price_sub":      round(price_sub, 1),
        "volume_sub":     round(volume_sub, 1),
        "interpretation": interpretation,
        "benchmark_rate": benchmark,
    }


def _build_interpretation(score, band, return_rate, benchmark, category):
    """Generates a plain English 2-sentence interpretation of the risk score."""
    rate_pct      = round(return_rate * 100, 1)
    benchmark_pct = round(benchmark * 100, 1)
    diff          = round((return_rate - benchmark) * 100, 1)

    if band == "Low Risk":
        return (
            f"Your return rate of {rate_pct}% is {abs(diff)} points below "
            f"the {category} category average of {benchmark_pct}%. "
            f"Your Zalando account is not at risk — focus on maintaining "
            f"your current product quality and descriptions."
        )
    elif band == "Monitor":
        return (
            f"Your return rate of {rate_pct}% is {diff} points above "
            f"the {category} category average of {benchmark_pct}%. "
            f"You are not in immediate danger but should act now to bring "
            f"your rate down before it approaches Zalando's penalty threshold."
        )
    else:
        return (
            f"Your return rate of {rate_pct}% is significantly above "
            f"the {category} category average of {benchmark_pct}% and is "
            f"approaching or exceeding Zalando's estimated penalty threshold. "
            f"Your account visibility may already be affected — immediate action is required."
        )