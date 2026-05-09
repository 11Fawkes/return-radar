# ============================================================
# app.py
# Return Radar — Main Streamlit Application
# Built by Dhruv Kumar | Berlin 2025
# ============================================================

import streamlit as st
from modules.benchmarks import CATEGORY_BENCHMARKS
from modules.scoring import calculate_risk_score
from modules.simulation import simulate_inventory, get_financial_table
from modules.recommendations import get_recommendations
from modules.charts import build_inventory_chart, build_score_gauge

# ── Page config ──────────────────────────────────────────────
st.set_page_config(
    page_title="Return Radar",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ───────────────────────────────────────────────
st.markdown("""
<style>
    /* Main background */
    .stApp { background-color: #0F0F1A; }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #1A1A2E;
        border-right: 1px solid #2a2a4a;
    }

    /* Headers */
    h1, h2, h3 { color: #FFFFFF !important; }

    /* Risk band cards */
    .risk-card {
        padding: 20px 24px;
        border-radius: 8px;
        margin-bottom: 16px;
    }
    .risk-low      { background: rgba(0,196,154,0.12); border-left: 4px solid #00C49A; }
    .risk-monitor  { background: rgba(255,140,66,0.12); border-left: 4px solid #FF8C42; }
    .risk-action   { background: rgba(233,69,96,0.12);  border-left: 4px solid #E94560; }

    /* Recommendation cards */
    .rec-card {
        background: #1A1A2E;
        border: 1px solid #2a2a4a;
        border-radius: 8px;
        padding: 20px;
        margin-bottom: 12px;
    }
    .rec-high   { border-top: 3px solid #E94560; }
    .rec-medium { border-top: 3px solid #FF8C42; }
    .rec-low    { border-top: 3px solid #00C49A; }

    /* Impact badge */
    .badge {
        display: inline-block;
        padding: 2px 10px;
        border-radius: 12px;
        font-size: 11px;
        font-weight: 600;
        margin-bottom: 8px;
    }
    .badge-high   { background: rgba(233,69,96,0.2);  color: #E94560; }
    .badge-medium { background: rgba(255,140,66,0.2); color: #FF8C42; }
    .badge-low    { background: rgba(0,196,154,0.2);  color: #00C49A; }

    /* Metric boxes */
    [data-testid="stMetric"] {
        background: #1A1A2E;
        border: 1px solid #2a2a4a;
        border-radius: 8px;
        padding: 16px;
    }
    [data-testid="stMetricLabel"] { color: rgba(255,255,255,0.6) !important; }
    [data-testid="stMetricValue"] { color: #FFFFFF !important; }

    /* Divider */
    hr { border-color: #2a2a4a; }

    /* Table */
    .stDataFrame { background: #1A1A2E; }

    /* Button */
    .stButton > button {
        background: #E94560;
        color: white;
        border: none;
        border-radius: 6px;
        padding: 10px 24px;
        font-weight: 600;
        width: 100%;
        font-size: 15px;
    }
    .stButton > button:hover {
        background: #c73652;
        color: white;
    }

    /* Info box */
    .info-box {
        background: rgba(233,69,96,0.08);
        border: 1px solid rgba(233,69,96,0.3);
        border-radius: 8px;
        padding: 16px 20px;
        margin: 12px 0;
    }
</style>
""", unsafe_allow_html=True)


# ── Header ───────────────────────────────────────────────────
st.markdown("""
<div style='padding: 8px 0 24px 0;'>
    <h1 style='font-size:2.4rem; margin-bottom:4px;'>
        📦 Return Radar
    </h1>
    <p style='color:rgba(255,255,255,0.55); font-size:1.05rem; margin:0;'>
        Return risk & inventory impact simulator for Zalando partner brands
    </p>
    <p style='color:rgba(233,69,96,0.8); font-size:0.85rem; margin-top:6px;'>
        Built in response to Zalando's January 2025 policy change —
        cutting the return window from 100 days to 30 days.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")


# ── Sidebar Inputs ───────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding-bottom:16px;'>
        <h2 style='font-size:1.2rem; margin-bottom:4px;'>Your Product Details</h2>
        <p style='color:rgba(255,255,255,0.45); font-size:0.82rem;'>
            Fill in 5 fields and press Analyse.
        </p>
    </div>
    """, unsafe_allow_html=True)

    category = st.selectbox(
        "Product Category",
        options=list(CATEGORY_BENCHMARKS.keys()),
        help="Select the category that best matches your product."
    )

    price = st.slider(
        "Price Point (€)",
        min_value=10,
        max_value=500,
        value=60,
        step=5,
        help="The retail price of this product on Zalando."
    )

    monthly_units = st.number_input(
        "Monthly Units Sold",
        min_value=1,
        max_value=10000,
        value=100,
        step=10,
        help="How many units of this product do you sell per month?"
    )

    return_rate_pct = st.slider(
        "Current Return Rate (%)",
        min_value=0,
        max_value=70,
        value=35,
        step=1,
        help="What percentage of sold items are returned? Use your best estimate."
    )

    current_stock = st.number_input(
        "Current Inventory Stock (units)",
        min_value=0,
        max_value=50000,
        value=200,
        step=10,
        help="How many units do you currently have in your warehouse?"
    )

    st.markdown("<br>", unsafe_allow_html=True)
    run = st.button("Run Analysis")

    st.markdown("""
    <div style='margin-top:32px; padding-top:16px;
                border-top:1px solid #2a2a4a;
                color:rgba(255,255,255,0.3); font-size:0.75rem;'>
        Benchmarks based on published academic and industry data.<br>
        Not affiliated with Zalando SE.
    </div>
    """, unsafe_allow_html=True)


# ── Default state: show instructions ─────────────────────────
if not run:
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class='rec-card rec-high'>
            <div style='font-size:1.5rem;'>⚠️</div>
            <h3 style='margin:8px 0 4px;'>Risk Score</h3>
            <p style='color:rgba(255,255,255,0.55); font-size:0.88rem;'>
                See exactly where your return rate sits relative to
                Zalando's penalty threshold and your category benchmark.
            </p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class='rec-card rec-medium'>
            <div style='font-size:1.5rem;'>📈</div>
            <h3 style='margin:8px 0 4px;'>90-Day Projection</h3>
            <p style='color:rgba(255,255,255,0.55); font-size:0.88rem;'>
                Model what your inventory backlog looks like over 3 months
                across 3 scenarios: current, optimised, and worst case.
            </p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class='rec-card rec-low'>
            <div style='font-size:1.5rem;'>✅</div>
            <h3 style='margin:8px 0 4px;'>Action Plan</h3>
            <p style='color:rgba(255,255,255,0.55); font-size:0.88rem;'>
                Get 3 prioritised recommendations specific to your
                category, price point, and return situation.
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class='info-box' style='margin-top:24px;'>
        <p style='color:rgba(255,255,255,0.7); margin:0; font-size:0.9rem;'>
            👈 <b>Fill in your product details in the sidebar and press Run Analysis</b>
            to generate your personalised return risk report.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.stop()


# ── Run all modules ───────────────────────────────────────────
return_rate = return_rate_pct / 100

risk      = calculate_risk_score(category, price, monthly_units, return_rate)
sim       = simulate_inventory(monthly_units, return_rate, current_stock, price)
fin_table = get_financial_table(sim["summary"])
recs      = get_recommendations(category, price, return_rate, risk["score"])


# ════════════════════════════════════════════════════════════
# OUTPUT BLOCK 1 — RISK SCORE
# ════════════════════════════════════════════════════════════
st.markdown("## 📊 Return Risk Score")

col_gauge, col_info = st.columns([1, 1.6])

with col_gauge:
    fig_gauge = build_score_gauge(risk["score"], risk["band"])
    st.plotly_chart(fig_gauge, use_container_width=True, config={"displayModeBar": False})

with col_info:
    band_class = {
        "Low Risk":        "risk-low",
        "Monitor":         "risk-monitor",
        "Action Required": "risk-action",
    }.get(risk["band"], "risk-monitor")

    band_emoji = {
        "Low Risk":        "🟢",
        "Monitor":         "🟡",
        "Action Required": "🔴",
    }.get(risk["band"], "🟡")

    st.markdown(f"""
    <div class='risk-card {band_class}'>
        <div style='font-size:1.1rem; font-weight:700; margin-bottom:8px;'>
            {band_emoji} {risk["band"]}
        </div>
        <p style='color:rgba(255,255,255,0.8); margin:0; line-height:1.6;'>
            {risk["interpretation"]}
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Sub-score breakdown
    st.markdown("<p style='color:rgba(255,255,255,0.4); font-size:0.78rem; margin:12px 0 6px;'>SCORE BREAKDOWN</p>", unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("vs Benchmark", f"{risk['benchmark_sub']}")
    c2.metric("vs Threshold", f"{risk['threshold_sub']}")
    c3.metric("Price Factor",  f"{risk['price_sub']}")
    c4.metric("Volume Factor", f"{risk['volume_sub']}")

st.markdown("---")


# ════════════════════════════════════════════════════════════
# OUTPUT BLOCK 2 — 90-DAY INVENTORY PROJECTION
# ════════════════════════════════════════════════════════════
st.markdown("## 📈 90-Day Inventory Impact")

fig_chart = build_inventory_chart(sim["df"])
st.plotly_chart(fig_chart, use_container_width=True, config={"displayModeBar": False})

st.markdown("<p style='color:rgba(255,255,255,0.4); font-size:0.78rem; margin:4px 0 10px;'>FINANCIAL IMPACT BY SCENARIO</p>", unsafe_allow_html=True)
st.dataframe(
    fin_table,
    use_container_width=True,
    hide_index=True,
)

st.markdown("---")


# ════════════════════════════════════════════════════════════
# OUTPUT BLOCK 3 — RECOMMENDATIONS
# ════════════════════════════════════════════════════════════
st.markdown("## ✅ Your Action Plan")
st.markdown(
    "<p style='color:rgba(255,255,255,0.55); margin-bottom:20px;'>"
    "3 prioritised actions based on your category, price point, and return situation."
    "</p>",
    unsafe_allow_html=True
)

for i, rec in enumerate(recs):
    impact_lower = rec["impact"].lower()
    rec_class    = f"rec-{impact_lower}"
    badge_class  = f"badge-{impact_lower}"

    st.markdown(f"""
    <div class='rec-card {rec_class}'>
        <span class='badge {badge_class}'>{rec["impact"]} Impact</span>
        <h3 style='margin:4px 0 8px; font-size:1rem;'>{i+1}. {rec["title"]}</h3>
        <p style='color:rgba(255,255,255,0.65); margin:0; font-size:0.9rem; line-height:1.6;'>
            {rec["explanation"]}
        </p>
    </div>
    """, unsafe_allow_html=True)


# ── Footer ────────────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style='text-align:center; color:rgba(255,255,255,0.25); font-size:0.8rem; padding:8px 0 16px;'>
    Built by <a href='https://linkedin.com/in/dhruv-kumar-a54a2916b'
    style='color:#E94560; text-decoration:none;'>Dhruv Kumar</a>
    &nbsp;·&nbsp;
    <a href='https://github.com/11fawkes' style='color:#E94560; text-decoration:none;'>GitHub</a>
    &nbsp;·&nbsp;
    <a href='https://11fawkes.github.io/Portfolio' style='color:#E94560; text-decoration:none;'>Portfolio</a>
    &nbsp;·&nbsp;
    Benchmarks based on published academic and industry data. Not affiliated with Zalando SE.
</div>
""", unsafe_allow_html=True)