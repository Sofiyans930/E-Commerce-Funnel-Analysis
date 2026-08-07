<div align="center">

# 🛒 E-Commerce Funnel Analysis Dashboard

**An End-to-End Data Analytics Project built with Python, Pandas, Plotly and Streamlit.**

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-150458?logo=pandas&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-Interactive%20Charts-3F4F75?logo=plotly&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?logo=streamlit&logoColor=white)
![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-F37626?logo=jupyter&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green.svg)

[Overview](#-project-overview) •
[Business Problem](#-business-problem) •
[Workflow](#-project-workflow) •
[Technologies](#-technologies-used) •
[Skills](#-skills-demonstrated) •
[Features](#-dashboard-features) •
[Insights](#-key-business-insights) •
[Live Demo](#-live-dashboard) •
[Roadmap](#-future-improvements)

</div>

---

## 📌 Project Overview

Every e-commerce business runs on a simple truth: traffic is only valuable if it converts. This project analyzes how 10,000 customer sessions move through a 4-stage purchase funnel — **Browse → Add to Cart → Checkout → Purchase** — to answer the question every growth and product team asks: *where is revenue being lost, and what should we do about it?*

The project covers the full analytics lifecycle — data cleaning, feature engineering, session-level rollup, funnel and revenue analysis, and segment performance across channel, device, region, and product category — delivered as both a documented Jupyter notebook and a live, filterable Streamlit dashboard that turns raw event data into decisions.

## 🎯 Business Problem

Most e-commerce businesses lose the majority of their traffic before checkout, but rarely know exactly **where** or **why**. Without stage-by-stage visibility, teams tend to over-invest in top-of-funnel acquisition while the real leak sits further downstream, closer to the point of purchase.

This project — and the dashboard it produces — gives stakeholders a self-service way to:

- Identify the exact stage where the largest share of customers drop off
- Compare conversion performance across channels, devices, regions, and product categories to guide budget allocation
- Quantify the revenue at stake at each funnel stage and estimate the realistic upside from fixing the biggest leak
- Filter and explore the data live, without waiting on a static report

## 🔄 Project Workflow

```
┌─────────────────────┐     ┌──────────────────┐     ┌───────────────────────┐     ┌──────────────────┐
│   Data Generation    │ ──► │  Data Cleaning &  │ ──► │  Feature Engineering  │ ──► │  Session-Level    │
│  (10,000 sessions)   │     │  Verification     │     │                       │     │  Rollup           │
└─────────────────────┘     └──────────────────┘     └───────────────────────┘     └──────────────────┘
                                                                                              │
                                                                                              ▼
┌─────────────────────┐     ┌──────────────────┐     ┌───────────────────────┐     ┌──────────────────┐
│  Interactive         │ ◄── │  Business         │ ◄── │  Time-Based Analysis  │ ◄── │  Funnel, Revenue  │
│  Streamlit Dashboard │     │  Insights &       │     │                       │     │  & Segment        │
│                       │     │  Recommendations  │     │                       │     │  Analysis         │
└─────────────────────┘     └──────────────────┘     └───────────────────────┘     └──────────────────┘
```

1. **Data Generation** — 10,000 simulated sessions with realistic stage-drop probabilities, tagged by device, region, channel, and product category
2. **Data Cleaning & Verification** — type casting, null/duplicate checks, schema validation
3. **Feature Engineering** — date, hour, day, and month extraction from timestamps
4. **Session-Level Analysis** — one row per session, capturing full event sequence, session duration, and highest funnel stage reached
5. **Funnel & Revenue Analysis** — conversion and drop-off per stage, total revenue, average order value
6. **Segment Analysis** — conversion and revenue by channel, device, region, and product category
7. **Time-Based Analysis** — sessions and revenue trends by hour and day
8. **Business Insights & Recommendations** — findings translated into concrete, actionable steps
9. **Dashboard** — every calculation above, reproduced exactly, in a live filterable Streamlit application

## 🛠️ Technologies Used

| Category | Tools |
|---|---|
| **Programming Language** | Python 3.10+ |
| **Data Analysis** | Pandas, NumPy |
| **Visualization** | Matplotlib, Seaborn, Plotly |
| **Dashboard** | Streamlit |
| **Development Tools** | Jupyter Notebook, Faker (data simulation) |
| **Version Control** | Git, GitHub |

## 🧠 Skills Demonstrated

- Data Cleaning
- Feature Engineering
- Exploratory Data Analysis (EDA)
- KPI Reporting
- Funnel Analysis
- Customer Journey Analytics
- Business Intelligence
- Interactive Dashboard Development
- Data Visualization
- Business Problem Solving

## 📁 Project Structure

```
E-Commerce-Funnel-Analysis/
│
├── .devcontainer/                        # Dev container configuration
├── Ecommerce_Funnel_Analysis.ipynb       # Full analysis notebook
├── app.py                                # Streamlit dashboard
├── funnel_dataset.csv                    # Generated dataset
├── requirements.txt                      # Project dependencies
├── assets/
│   └── screenshots/                      # Dashboard screenshots
├── .gitignore
├── LICENSE
└── README.md
```

## ⚙️ Installation

```bash
git clone https://github.com/Sofiyans930/E-Commerce-Funnel-Analysis.git
cd E-Commerce-Funnel-Analysis
pip install -r requirements.txt
```

## ▶️ How to Run

**Notebook (full analysis):**
```bash
jupyter notebook Ecommerce_Funnel_Analysis.ipynb
```

**Dashboard (interactive):**
```bash
streamlit run app.py
```
Opens at `http://localhost:8501`. `funnel_dataset.csv` is read directly from the project root, so no path changes are needed.

## 📊 Dashboard Features

- Executive KPI cards — Total Sessions, Total Orders, Total Revenue, Conversion Rate, Average Order Value, Purchase Rate
- Interactive funnel chart with stage-by-stage drop-off
- Revenue by funnel stage and average session duration by stage
- Channel, device, region, and product category performance — charts, breakdown tables, and top-performer KPIs
- Business insights and strategic recommendations sections
- Suggested improvements, kept separate from the core analysis
- Sidebar filters for channel, device, region, and product category
- CSV download of filtered data
- Hover tooltips, responsive layout, and a consistent corporate color palette

## 💡 Key Business Insights

| Metric | Value |
|---|---|
| Total Sessions | 10,000 |
| Overall Conversion Rate | 10.58% |
| Total Revenue | $1,129,865.17 |
| Average Order Value | $1,067.93 |
| Biggest Drop-off | Checkout → Purchase — only 29.97% of Checkout sessions convert |
| Best Channel | Google Ads (11.80% conversion) |
| Best Device | Desktop (10.87% conversion) |
| Best Region | South (11.39% conversion) |
| Best Product Category | Fashion (11.09% conversion) |

**Top recommendation:** Checkout is the single largest leak in the funnel. Simplifying it — guest checkout, fewer form fields, upfront shipping costs — carries more revenue upside than acquiring additional top-of-funnel traffic.

## 🌐 Live Dashboard

**Live Demo:**
https://e-commerce-funnel-analysis-ze4ngh33vheqkgexljpoa6.streamlit.app/

**GitHub Repository:**
https://github.com/Sofiyans930/E-Commerce-Funnel-Analysis

## 📸 Dashboard Screenshots

### Executive Dashboard

![Executive Dashboard](assets/screenshots/dashboard_overview.png)

---

### Funnel Analysis

![Funnel Analysis](assets/screenshots/funnel_analysis.png)

---

### Channel Performance

![Channel Performance](assets/screenshots/channel_performance.png)

---

### Device Performance

![Device Performance](assets/screenshots/device_performance.png)

---

### Region Performance

![Region Performance](assets/screenshots/region_performance.png)

---

### Product Category Performance

![Product Category Performance](assets/screenshots/product_category_performance.png)

---

### Business Insights

![Business Insights](assets/screenshots/business_insights.png)

 |

## 🤝 AI Assistance

Parts of this project were built with AI-assisted development:

**ChatGPT** assisted with:
- Debugging
- Code explanation
- Documentation
- Code optimization
- README improvements

**Claude AI** assisted with:
- Streamlit frontend development
- UI improvements
- Layout improvements
- Documentation formatting

All analytical decisions, KPI calculations, business insights, dashboard validation, and final implementation were completed and reviewed by the project author. This includes exploratory data analysis (EDA), funnel analysis, revenue analysis, channel/device/region/category analysis, business insights, strategic recommendations, and testing and validation of results.

## 🚀 Future Improvements

- Customer Segmentation
- Predictive Analytics
- Machine Learning Models
- Database Integration
- Real-Time Data Pipeline

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

Copyright (c) 2026 Sofiyan Shaikh

---

<div align="center">

⭐ If you found this project helpful, please consider giving it a Star.

</div>
