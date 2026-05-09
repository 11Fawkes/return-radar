# ============================================================
# recommendations.py
# Selects the 3 most relevant actions from the ACTION_LIBRARY
# based on the user's specific situation
# ============================================================

from modules.benchmarks import ACTION_LIBRARY


def get_recommendations(
    category: str,
    price: float,
    return_rate: float,
    risk_score: float,
) -> list:
    """
    Evaluates all 12 actions in ACTION_LIBRARY against the user's inputs.
    Returns the top 3 most relevant actions as a list of dicts.

    Parameters:
        category    : product category string
        price       : product price in EUR
        return_rate : return rate as decimal
        risk_score  : composite risk score 0-100

    Returns:
        list of 3 dicts, each with:
            title       : str
            explanation : str
            impact      : str ('High' / 'Medium' / 'Low')
            priority    : int (1=highest)
    """

    triggered = []

    for action in ACTION_LIBRARY:
        try:
            if action["trigger"](category, price, return_rate, risk_score):
                triggered.append(action)
        except Exception:
            # If trigger evaluation fails, skip this action
            continue

    # Sort by priority (1 first), then by impact level
    impact_order = {"High": 0, "Medium": 1, "Low": 2}
    triggered.sort(key=lambda x: (x["priority"], impact_order.get(x["impact"], 3)))

    # Always return exactly 3 — pad with low-priority actions if needed
    if len(triggered) < 3:
        for action in ACTION_LIBRARY:
            if action not in triggered:
                triggered.append(action)
            if len(triggered) == 3:
                break

    return [
        {
            "title":       a["title"],
            "explanation": a["explanation"],
            "impact":      a["impact"],
        }
        for a in triggered[:3]
    ]