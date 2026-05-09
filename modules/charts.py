# ============================================================
# charts.py
# Builds all Plotly charts for Return Radar
# ============================================================

import plotly.graph_objects as go
import pandas as pd


# Colour palette matching the app theme
COLOURS = {
    "Current":    "#E94560",   # red — current state
    "Optimised":  "#00C49A",   # green — best case
    "Worst Case": "#FF8C42",   # orange — worst case
}


def build_inventory_chart(df: pd.DataFrame) -> go.Figure:
    """
    Builds the 90-day inventory projection line chart.

    Parameters:
        df : DataFrame from simulate_inventory()
             Columns: day, Current, Optimised, Worst Case

    Returns:
        Plotly Figure object
    """

    fig = go.Figure()

    for scenario in ["Current", "Optimised", "Worst Case"]:
        fig.add_trace(
            go.Scatter(
                x=df["day"],
                y=df[scenario],
                name=scenario,
                mode="lines",
                line=dict(
                    color=COLOURS[scenario],
                    width=2.5,
                    dash="solid" if scenario == "Current" else (
                        "dot" if scenario == "Optimised" else "dash"
                    ),
                ),
                hovertemplate=(
                    f"<b>{scenario}</b><br>"
                    "Day %{x}<br>"
                    "Backlog: %{y:.0f} units<extra></extra>"
                ),
            )
        )

    # Add reference lines at key days
    for day, label in [(30, "30 days"), (60, "60 days"), (90, "90 days")]:
        fig.add_vline(
            x=day,
            line_dash="dot",
            line_color="rgba(255,255,255,0.15)",
            annotation_text=label,
            annotation_position="top",
            annotation_font=dict(color="rgba(255,255,255,0.4)", size=9),
        )

    fig.update_layout(
        title=dict(
            text="90-Day Inventory Backlog Projection",
            font=dict(color="white", size=16),
            x=0,
        ),
        xaxis=dict(
            title="Day",
            color="rgba(255,255,255,0.6)",
            gridcolor="rgba(255,255,255,0.08)",
            tickfont=dict(color="rgba(255,255,255,0.6)"),
        ),
        yaxis=dict(
            title="Units in Backlog",
            color="rgba(255,255,255,0.6)",
            gridcolor="rgba(255,255,255,0.08)",
            tickfont=dict(color="rgba(255,255,255,0.6)"),
        ),
        legend=dict(
            font=dict(color="white"),
            bgcolor="rgba(0,0,0,0)",
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(26,26,46,0.6)",
        margin=dict(l=10, r=10, t=60, b=10),
        hovermode="x unified",
    )

    return fig


def build_score_gauge(score: float, band: str) -> go.Figure:
    """
    Builds a gauge chart for the risk score.

    Parameters:
        score : float 0-100
        band  : 'Low Risk' | 'Monitor' | 'Action Required'

    Returns:
        Plotly Figure object
    """

    band_colours = {
        "Low Risk":         "#00C49A",
        "Monitor":          "#FF8C42",
        "Action Required":  "#E94560",
    }
    needle_colour = band_colours.get(band, "#E94560")

    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=score,
            number=dict(
                font=dict(color="white", size=48),
                suffix="/100",
            ),
            gauge=dict(
                axis=dict(
                    range=[0, 100],
                    tickwidth=1,
                    tickcolor="rgba(255,255,255,0.3)",
                    tickfont=dict(color="rgba(255,255,255,0.5)", size=10),
                ),
                bar=dict(color=needle_colour, thickness=0.25),
                bgcolor="rgba(0,0,0,0)",
                borderwidth=0,
                steps=[
                    dict(range=[0, 30],   color="rgba(0,196,154,0.15)"),
                    dict(range=[30, 60],  color="rgba(255,140,66,0.15)"),
                    dict(range=[60, 100], color="rgba(233,69,96,0.15)"),
                ],
                threshold=dict(
                    line=dict(color=needle_colour, width=3),
                    thickness=0.75,
                    value=score,
                ),
            ),
        )
    )

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white"),
        margin=dict(l=20, r=20, t=30, b=10),
        height=220,
    )

    return fig