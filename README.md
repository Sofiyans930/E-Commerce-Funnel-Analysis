<div align="center">

E-Commerce-Funnel-Analysis
### End-to-end funnel analytics — from raw event data to an interactive executive dashboard

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-150458?logo=pandas&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-Interactive%20Charts-3F4F75?logo=plotly&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?logo=streamlit&logoColor=white)
![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-F37626?logo=jupyter&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green.svg)

[Overview](#-project-overview) •
[Business Problem](#-business-problem) •
[Workflow](#-project-workflow) •
[Features](#-dashboard-features) •
[Install](#-installation) •
[Insights](#-key-business-insights) •
[Roadmap](#-future-improvements)

</div>

---

## 📌 Project Overview

This project analyzes how customers move through a 4-stage e-commerce
purchase funnel — **Browse → Add to Cart → Checkout → Purchase** — using
10,000 simulated customer sessions. It covers the full analytics
lifecycle: data cleaning, feature engineering, session-level rollup,
funnel and revenue analysis, and segment performance across channel,
device, region, and product category — delivered as both a documented
Jupyter notebook and a live, filterable Streamlit dashboard.

## 🎯 Business Problem

E-commerce businesses lose the majority of their traffic before checkout,
but rarely know **exactly where** or **why**. Without stage-by-stage
visibility, teams over-invest in top-of-funnel traffic acquisition while
the real leak sits further downstream. This project answers three
questions a growth or product team actually needs answered:

1. **Where** in the funnel are customers dropping off?
2. **Which** channels, devices, regions, and product categories convert
   best — and where should budget move?
3. **What** revenue is at stake at each stage, and what's the realistic
   lift from fixing the biggest leak?

## 🔄 Project Workflow

```
Data Generation → Data Cleaning → Feature Engineering → Session Rollup
       ↓
Funnel Analysis → Revenue Analysis → Segment Analysis (Channel/Device/Region/Category)
       ↓
Time-Based Analysis → Business Insights → Strategic Recommendations
       ↓
Interactive Streamlit Dashboard
```

1. **Data Generation** — 10,000 simulated sessions with realistic
   stage-drop probabilities, tagged with device, region, channel, and
   product category.
2. **Data Cleaning & Verification** — type casting, null/duplicate checks,
   schema validation.
3. **Feature Engineering** — date/hour/day/month extraction from
   timestamps.
4. **Session-Level Analysis** — one row per session: full event sequence,
   session duration, and highest funnel stage reached.
5. **Funnel & Revenue Analysis** — conversion and drop-off per stage,
   total revenue, average order value.
6. **Segment Analysis** — conversion and revenue by channel, device,
   region, and product category.
7. **Time-Based Analysis** — sessions and revenue by hour/day.
8. **Business Insights & Recommendations** — translated into concrete
   action items.
9. **Dashboard** — every calculation above, reproduced exactly, in a
   live filterable Streamlit app.

## 🛠️ Technologies Used

| Category | Tools |
|---|---|
| Language | Python 3.10+ |
| Data Analysis | Pandas, NumPy |
| Static Visualization | Matplotlib, Seaborn |
| Interactive Visualization | Plotly |
| Dashboard | Streamlit |
| Notebook | Jupyter |
| Data Simulation | Faker |

## 📁 Project Structure

```
ecommerce-funnel-analysis/
│
├── notebook/
│   └── Ecommerce_Funnel_Analysis.ipynb   # Full analysis notebook
│
├── dashboard/
│   ├── app.py                            # Streamlit dashboard
│   └── requirements.txt                  # Dashboard dependencies
│
├── data/
│   └── funnel_dataset.csv                # Generated dataset
│
├── reports/
│   ├── REPORT.md                         # Written analysis summary
│   └── Funnel_Analysis_Report.pptx       # Presentation deck
│
├── assets/
│   └── screenshots/                      # Dashboard screenshots (below)
│
├── .gitignore
├── LICENSE
└── README.md
```

## ⚙️ Installation

```bash
git clone https://github.com/<your-username>/ecommerce-funnel-analysis.git
cd ecommerce-funnel-analysis
pip install -r dashboard/requirements.txt
```

## ▶️ How to Run

**Notebook (full analysis):**
```bash
jupyter notebook notebook/Ecommerce_Funnel_Analysis.ipynb
```

**Dashboard (interactive):**
```bash
cd dashboard
streamlit run app.py
```
Opens at `http://localhost:8501`. Make sure `funnel_dataset.csv` is
accessible from the dashboard folder (update the path in `app.py` if you
move `data/`).

## 📊 Dashboard Features

- **Executive KPI cards** — Total Sessions, Total Orders, Total Revenue,
  Conversion Rate, Average Order Value, Purchase Rate
- **Interactive Funnel Chart** with stage-by-stage drop-off
- **Revenue by Funnel Stage** and **Average Session Duration by Stage**
- **Channel / Device / Region / Product Category performance** — chart,
  breakdown table, and top-performer KPIs for each
- **Business Insights** and **Strategic Recommendations** sections
- **Suggested Improvements** — code/logic observations, kept separate
  from the analysis itself
- **Sidebar filters** — Channel, Device, Region, Product Category
- **Download filtered data as CSV**
- Hover tooltips, responsive layout, consistent corporate color palette

## 💡 Key Business Insights

| Metric | Value |
|---|---|
| Total Sessions | 10,000 |
| Overall Conversion Rate | 10.58% |
| Total Revenue | $1,129,865.17 |
| Average Order Value | $1,067.93 |
| **Biggest Drop-off** | Checkout → Purchase — only 29.97% of Checkout sessions convert |
| **Best Channel** | Google Ads (11.80% conversion) |
| **Best Device** | Desktop (10.87% conversion) |
| **Best Region** | South (11.39% conversion) |
| **Best Product Category** | Fashion (11.09% conversion) |

**Top recommendation:** checkout is the single largest leak in the funnel
— simplifying it (guest checkout, fewer form fields, upfront shipping
costs) has more revenue upside than acquiring more top-of-funnel traffic.

## 📸 Dashboard Screenshots

> Add screenshots after running the dashboard locally: `Print Screen` →
> save into `assets/screenshots/` → reference them below.

| Executive KPIs | Funnel Analysis |
|---|---|
| ![KPIs](<img width="1022" height="107" alt="image" src="https://github.com/user-attachments/assets/a8ebe301-4c23-4b82-baed-c52d70d07a60" />
) | ![Funnel](<img width="1786" height="790" alt="newplot (1)" src="https://github.com/user-attachments/assets/7533eb7d-567f-46d1-9157-4254a55e18bb" />
) |

| Channel Performance | Business Insights |
|---|---|
| ![Channel](assets/screenshots/channel.png) | ![Insights](assets/screenshots/insights.png) |

## 🚀 Future Improvements

- [ ] Replace simulated data with real clickstream/analytics data
- [ ] Add a random seed to the data-generation step for reproducibility
- [ ] Add cohort and retention analysis (do purchasers return?)
- [ ] A/B test the checkout simplification and measure actual lift
- [ ] Add automated tests for the core calculation functions
- [ ] Deploy the dashboard to Streamlit Community Cloud with a public URL
- [ ] Add date-range filtering to the dashboard sidebar
- [ ] Containerize with Docker for one-command setup

## 🤝 AI Assistance

Parts of this project were built with AI-assisted development:

- **ChatGPT** assisted with: Python debugging, code optimization, code
  explanation, error fixing, and README drafting.
- **Claude AI** assisted with: Streamlit frontend development, dashboard
  UI improvements, code organization, and documentation improvements.

**All core analytical work is original**, including: exploratory data
analysis (EDA), KPI calculations, funnel analysis, revenue analysis,
channel analysis, device analysis, region analysis, product category
analysis, business insights, strategic recommendations, and testing/
validation of results.

## 📄 License

MIT License

Copyright (c) 2026 [Sofiyan Shaikh]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.


---

<div align="center">

If you found this project useful, consider giving it a ⭐

</div>
