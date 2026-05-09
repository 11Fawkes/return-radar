# 📦 Return Radar

**Return risk & inventory impact simulator for Zalando partner brands.**

Built in response to Zalando's 2025 policy change cutting the return window 
from 100 days to 30 days — a shift that created significant operational 
uncertainty for seller partners with no independent data tools.

🔴 **[Try the live tool →](YOUR_STREAMLIT_URL)**

---

## What it does

Input 5 numbers about your product. Get back:

- **Return Risk Score** — benchmarked against your category average 
  and Zalando's estimated penalty threshold
- **90-Day Inventory Simulation** — three scenarios: current, 
  optimised, worst case
- **3 Prioritised Actions** — specific to your category, 
  price point, and return situation

No data science background needed. Written entirely in plain English 
for brand operators.

---

## Why I built this

Zalando processes 125 million returns annually with machine learning 
models, fit prediction AI, and computer vision tools. Their seller 
partners have a spreadsheet.

That information asymmetry bothered me. Return Radar is a small step 
toward rebalancing it.

---

## Tech stack

- Python 3.12
- Streamlit
- Pandas + NumPy
- Plotly

---

## Run locally

```bash
pip install streamlit pandas numpy plotly
streamlit run app.py
```

---

## Author

**Dhruv Kumar** — Business Analysis | Berlin, 2026

[LinkedIn](https://linkedin.com/in/dhruv-kumar-a54a2916b) · 
[Portfolio](https://11fawkes.github.io/Portfolio)

---

*Benchmarks based on published academic and industry data. 
Not affiliated with Zalando SE.*