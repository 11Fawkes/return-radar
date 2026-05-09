# ============================================================
# simulation.py
# Runs the 90-day inventory impact model (3 scenarios)
# ============================================================

import pandas as pd
from modules.benchmarks import HOLDING_COST_RATE, RESALE_VELOCITY


def simulate_inventory(
    monthly_units: int,
    return_rate: float,
    current_stock: int,
    price: float,
    days: int = 90
) -> dict:
    """
    Simulates inventory levels over 90 days under 3 scenarios.

    Parameters:
        monthly_units : units sold per month
        return_rate   : current return rate as decimal (e.g. 0.38)
        current_stock : units currently in warehouse
        price         : product price in EUR
        days          : simulation horizon (default 90)

    Returns a dict with:
        df            : DataFrame with daily stock levels per scenario
        summary       : dict with financial impact per scenario
    """

    daily_sales = monthly_units / 30

    scenarios = {
        "Current":   return_rate,
        "Optimised": max(0.0, return_rate - 0.10),
        "Worst Case": min(1.0, return_rate + 0.10),
    }

    results = {"day": list(range(1, days + 1))}
    summaries = {}

    for name, rate in scenarios.items():
        stock = float(current_stock)
        daily_stock = []

        for day in range(1, days + 1):
            returns_today = daily_sales * rate
            # resale velocity: fraction of backlog cleared per day
            resales_today = stock * (RESALE_VELOCITY / 30)
            stock = max(0.0, stock + returns_today - resales_today)
            daily_stock.append(round(stock, 1))

        results[name] = daily_stock

        # ── Financial summary at day 90 ──
        final_stock     = daily_stock[-1]
        holding_cost    = round(final_stock * price * HOLDING_COST_RATE, 2)
        dead_stock_value = round(final_stock * price * (1 - 0.40), 2)  # 40% secondary discount
        monthly_returns  = round(monthly_units * rate)

        summaries[name] = {
            "final_backlog_units":  round(final_stock),
            "holding_cost_eur":     holding_cost,
            "dead_stock_value_eur": dead_stock_value,
            "monthly_return_units": monthly_returns,
            "return_rate_pct":      round(rate * 100, 1),
        }

    df = pd.DataFrame(results)

    return {
        "df":      df,
        "summary": summaries,
    }


def get_financial_table(summary: dict) -> pd.DataFrame:
    """
    Converts the simulation summary into a clean display table.

    Returns a DataFrame ready to display in Streamlit.
    """
    rows = []
    for scenario, data in summary.items():
        rows.append({
            "Scenario":              scenario,
            "Return Rate":           f"{data['return_rate_pct']}%",
            "Monthly Returns (units)": data["monthly_return_units"],
            "90-Day Backlog (units)": data["final_backlog_units"],
            "Holding Cost / Month":  f"€{data['holding_cost_eur']:,.0f}",
            "Recoverable Value":     f"€{data['dead_stock_value_eur']:,.0f}",
        })
    return pd.DataFrame(rows)