"""
E-Commerce Funnel Analysis — Executive Dashboard
==================================================
This dashboard is a frontend ONLY. Every calculation below reproduces the
logic from `Ecommerce_Funnel_Analysis.ipynb` exactly (same groupby keys,
same funnel-stage cumulative-count method, same revenue/AOV formulas).
No business logic, KPI definition, or feature engineering was changed.

Run:      streamlit run app.py
Data:     funnel_dataset.csv must sit next to this file.
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# ----------------------------------------------------------------------
# PAGE CONFIG
# ----------------------------------------------------------------------
st.set_page_config(
    page_title="E-Commerce Funnel Analysis | Executive Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ----------------------------------------------------------------------
# THEME — corporate palette, applied consistently across every chart
# ----------------------------------------------------------------------
COLORS = {
    "primary": "#2563EB",     # blue   - conversion / primary metric
    "secondary": "#7C3AED",   # violet - secondary metric
    "success": "#16A34A",     # green  - revenue
    "warning": "#F59E0B",     # amber  - duration / neutral
    "danger": "#EF4444",      # red    - drop-off
    "dark": "#111827",
    "muted": "#6B7280",
    "bg_card": "#F9FAFB",
    "border": "#E5E7EB",
}
FUNNEL_COLORS = ["#2563EB", "#4F86F7", "#7CA8FA", "#A9CAFC"]

st.markdown(f"""
<style>
    .main {{ background-color: #FFFFFF; }}
    div[data-testid="stMetric"] {{
        background-color: {COLORS['bg_card']};
        border: 1px solid {COLORS['border']};
        border-radius: 10px;
        padding: 14px 16px 10px 16px;
    }}
    div[data-testid="stMetricLabel"] {{ color: {COLORS['muted']}; }}
    h1, h2, h3 {{ color: {COLORS['dark']}; font-family: 'Segoe UI', sans-serif; }}
    .section-divider {{ margin-top: 0.4rem; margin-bottom: 0.8rem; }}
</style>
""", unsafe_allow_html=True)

FUNNEL_STAGES = ["Browse", "Add to Cart", "Checkout", "Purchase"]


# ========================================================================
# DATA LAYER — every function here mirrors one notebook cell 1:1.
# The comment above each function names the source cell so you can
# cross-check it against Ecommerce_Funnel_Analysis.ipynb at any time.
# ========================================================================

@st.cache_data
def load_data(path: str = "funnel_dataset.csv") -> pd.DataFrame:
    """Mirrors notebook cells 8/16/24: load, parse Timestamp, extract
    Hour/Day features. No rows are dropped or modified."""
    df = pd.read_csv(path)
    df["Timestamp"] = pd.to_datetime(df["Timestamp"])
    df["Hour"] = df["Timestamp"].dt.hour
    df["Day"] = df["Timestamp"].dt.day_name()
    return df


@st.cache_data
def build_session_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Mirrors notebook cell 26 exactly: one row per Session_ID, event
    sequence preserved as a list, session duration in minutes, and the
    highest funnel stage each session reached."""
    session_summary = df.groupby("Session_ID").agg({
        "User_ID": "first",
        "Event": lambda x: list(x),
        "Timestamp": lambda x: list(x),
        "Device": "first",
        "Region": "first",
        "Channel": "first",
        "Product_Category": "first",
        "Revenue": "sum",
        "Bounce_Flag": "first",
    }).reset_index()

    session_summary.columns = [
        "Session_ID", "User_ID", "Event_Sequence", "Timestamp_Sequence",
        "Device", "Region", "Channel", "Product_Category", "Revenue", "Bounce_Flag",
    ]

    session_summary["Session_Duration_Min"] = session_summary["Timestamp_Sequence"].apply(
        lambda x: (max(x) - min(x)).total_seconds() / 60
    )

    def get_max_funnel_stage(events):
        stage_values = {stage: i for i, stage in enumerate(FUNNEL_STAGES)}
        max_stage_index = -1
        for event in events:
            if event in stage_values:
                max_stage_index = max(max_stage_index, stage_values[event])
        return FUNNEL_STAGES[max_stage_index] if max_stage_index != -1 else "Browse"

    session_summary["Max_Funnel_Stage"] = session_summary["Event_Sequence"].apply(get_max_funnel_stage)

    # notebook cell 28: lowercase all columns
    session_summary.columns = session_summary.columns.str.lower()
    return session_summary


def compute_funnel_df(session_summary: pd.DataFrame) -> pd.DataFrame:
    """Mirrors notebook cell 29 exactly (cumulative funnel counts,
    Conversion_Rate against Browse, Drop_Off_Rate stage-to-stage)."""
    funnel_metrics = []
    for i, stage in enumerate(FUNNEL_STAGES):
        if i == 0:
            count = len(session_summary)
        else:
            count = len(session_summary[session_summary["max_funnel_stage"].isin(FUNNEL_STAGES[i:])])
        funnel_metrics.append({"Stage": stage, "Sessions": count, "Stage_Order": i})

    funnel_df = pd.DataFrame(funnel_metrics)
    funnel_df["Conversion_Rate (%)"] = (funnel_df["Sessions"] / funnel_df["Sessions"].iloc[0] * 100).round(2)
    funnel_df["Drop_Off_Rate (%)"] = (funnel_df["Sessions"] / funnel_df["Sessions"].shift(1) * 100)
    funnel_df.loc[0, "Drop_Off_Rate (%)"] = 100
    funnel_df["Drop_Off_Rate (%)"] = funnel_df["Drop_Off_Rate (%)"].round(2)
    return funnel_df


def compute_revenue_analysis(session_summary: pd.DataFrame) -> dict:
    """Mirrors notebook cell 31 exactly."""
    revenue_analysis = session_summary[
        session_summary["max_funnel_stage"] == "Purchase"
    ].agg({"revenue": ["sum", "mean", "count"]})

    return {
        "total_revenue": revenue_analysis.loc["sum", "revenue"] if len(revenue_analysis) else 0,
        "average_order_value": revenue_analysis.loc["mean", "revenue"] if len(revenue_analysis) else 0,
        "total_orders": revenue_analysis.loc["count", "revenue"] if len(revenue_analysis) else 0,
    }


def compute_segment_df(session_summary: pd.DataFrame, group_col: str, label_col: str) -> pd.DataFrame:
    """Generalizes notebook cells 37 (channel), 41 (device), 45 (region),
    49 (category) — those four cells are structurally identical, so this
    one function reproduces all four without duplicating the logic four
    times. The math inside is untouched."""
    records = []
    for value in session_summary[group_col].unique():
        seg_session = session_summary[session_summary[group_col] == value]
        total_sessions = len(seg_session)
        if total_sessions == 0:
            continue

        metrics = {label_col: value, "Total_Sessions": total_sessions}

        for i, stage in enumerate(FUNNEL_STAGES):
            if i == 0:
                count = total_sessions
            else:
                count = len(seg_session[seg_session["max_funnel_stage"].isin(FUNNEL_STAGES[i:])])
            metrics[f"{stage}_Sessions"] = count
            metrics[f"{stage}_Rate"] = round((count / total_sessions) * 100, 2)

        purchased = seg_session[seg_session["max_funnel_stage"] == "Purchase"]
        metrics["Total_Revenue"] = purchased["revenue"].sum()
        metrics["AOV"] = purchased["revenue"].mean() if len(purchased) > 0 else 0
        metrics["Conversion_Rate"] = round((len(purchased) / total_sessions) * 100, 2)

        records.append(metrics)

    return pd.DataFrame(records).round(2)


def compute_revenue_by_stage(session_summary: pd.DataFrame) -> pd.DataFrame:
    """Mirrors the revenue-by-stage block inside notebook cell 33."""
    return session_summary.groupby("max_funnel_stage")["revenue"].sum().reset_index()


def compute_duration_by_stage(session_summary: pd.DataFrame) -> pd.DataFrame:
    """Mirrors the duration-by-stage block inside notebook cell 33."""
    return session_summary.groupby("max_funnel_stage")["session_duration_min"].mean().reset_index()


def compute_business_insights(session_summary, funnel_df, channel_df, device_df, region_df, category_df) -> dict:
    """Mirrors notebook cell 61 exactly (same idxmax/idxmin logic)."""
    purchase_sessions = len(session_summary[session_summary["max_funnel_stage"] == "Purchase"])
    conversion_rate = (purchase_sessions / len(session_summary)) * 100

    return {
        "total_sessions": len(session_summary),
        "total_purchases": purchase_sessions,
        "conversion_rate": conversion_rate,
        "total_revenue": session_summary["revenue"].sum(),
        "aov": session_summary[session_summary["max_funnel_stage"] == "Purchase"]["revenue"].mean(),
        "best_channel": channel_df.loc[channel_df["Conversion_Rate"].idxmax(), "Channel"] if len(channel_df) else "N/A",
        "best_device": device_df.loc[device_df["Conversion_Rate"].idxmax(), "Device"] if len(device_df) else "N/A",
        "best_region": region_df.loc[region_df["Conversion_Rate"].idxmax(), "Region"] if len(region_df) else "N/A",
        "best_category": category_df.loc[category_df["Conversion_Rate"].idxmax(), "Product_Category"] if len(category_df) else "N/A",
        "drop_stage": funnel_df.loc[funnel_df["Drop_Off_Rate (%)"].idxmin(), "Stage"] if len(funnel_df) else "N/A",
    }


# ========================================================================
# REUSABLE CHART BUILDERS — one function per chart type, called for every
# section (funnel, channel, device, region, category) instead of writing
# the same Plotly boilerplate five times.
# ========================================================================

def bar_chart(data: pd.DataFrame, x: str, y: str, color: str, title: str,
              y_suffix: str = "", horizontal: bool = False) -> go.Figure:
    fig = px.bar(
        data, x=x if not horizontal else y, y=y if not horizontal else x,
        orientation="h" if horizontal else "v",
        text=y if not horizontal else x,
        color_discrete_sequence=[color],
        title=title,
    )
    fig.update_traces(
        texttemplate=f"%{{text:.2f}}{y_suffix}", textposition="outside",
        hovertemplate=f"<b>%{{x}}</b><br>{y}: %{{y:.2f}}{y_suffix}<extra></extra>",
    )
    fig.update_layout(
        template="plotly_white", margin=dict(t=50, b=10, l=10, r=10),
        font=dict(family="Segoe UI, Arial", size=13, color=COLORS["dark"]),
        title_font_size=15, showlegend=False,
        xaxis_title="", yaxis_title="",
    )
    return fig


def funnel_chart(funnel_df: pd.DataFrame) -> go.Figure:
    fig = go.Figure(go.Funnel(
        y=funnel_df["Stage"],
        x=funnel_df["Sessions"],
        textinfo="value+percent initial",
        marker=dict(color=FUNNEL_COLORS, line=dict(color="white", width=2)),
        connector=dict(line=dict(color="#D1D5DB", width=2)),
        hovertemplate="<b>%{y}</b><br>Sessions: %{x}<br>%{percentInitial}<extra></extra>",
    ))
    fig.update_layout(
        template="plotly_white", margin=dict(t=20, b=10, l=10, r=10),
        font=dict(family="Segoe UI, Arial", size=13),
    )
    return fig


def pie_chart(data: pd.DataFrame, names: str, values: str, title: str) -> go.Figure:
    fig = px.pie(
        data, names=names, values=values, title=title, hole=0.45,
        color_discrete_sequence=px.colors.sequential.Blues_r,
    )
    fig.update_traces(textinfo="label+percent", hovertemplate="<b>%{label}</b><br>%{value:,.0f}<extra></extra>")
    fig.update_layout(
        template="plotly_white", margin=dict(t=50, b=10, l=10, r=10),
        font=dict(family="Segoe UI, Arial", size=13), title_font_size=15,
    )
    return fig


# ========================================================================
# LOAD DATA + SIDEBAR FILTERS
# ========================================================================
try:
    df_raw = load_data()
except FileNotFoundError:
    st.error("⚠️ `funnel_dataset.csv` not found. Place it in the same folder as app.py.")
    st.stop()

st.sidebar.title("📊 Funnel Dashboard")
st.sidebar.caption("Executive view — E-Commerce Customer Journey")
st.sidebar.markdown("---")
st.sidebar.header("🔎 Filters")

channel_sel = st.sidebar.multiselect("Channel", sorted(df_raw["Channel"].unique()), default=sorted(df_raw["Channel"].unique()))
device_sel = st.sidebar.multiselect("Device", sorted(df_raw["Device"].unique()), default=sorted(df_raw["Device"].unique()))
region_sel = st.sidebar.multiselect("Region", sorted(df_raw["Region"].unique()), default=sorted(df_raw["Region"].unique()))
category_sel = st.sidebar.multiselect("Product Category", sorted(df_raw["Product_Category"].unique()), default=sorted(df_raw["Product_Category"].unique()))

# Handle missing/empty filter selection gracefully instead of crashing
if not all([channel_sel, device_sel, region_sel, category_sel]):
    st.warning("Select at least one option in every sidebar filter to see data.")
    st.stop()

df = df_raw[
    df_raw["Channel"].isin(channel_sel)
    & df_raw["Device"].isin(device_sel)
    & df_raw["Region"].isin(region_sel)
    & df_raw["Product_Category"].isin(category_sel)
]

if df.empty:
    st.warning("No sessions match the selected filters. Try widening your selection.")
    st.stop()

st.sidebar.markdown("---")
st.sidebar.download_button(
    "⬇️ Download Filtered Data (CSV)",
    data=df.to_csv(index=False).encode("utf-8"),
    file_name="filtered_funnel_data.csv",
    mime="text/csv",
    use_container_width=True,
)

# ========================================================================
# RUN THE ANALYSIS PIPELINE (identical logic, filtered data)
# ========================================================================
session_summary = build_session_summary(df)
funnel_df = compute_funnel_df(session_summary)
revenue = compute_revenue_analysis(session_summary)
channel_df = compute_segment_df(session_summary, "channel", "Channel")
device_df = compute_segment_df(session_summary, "device", "Device")
region_df = compute_segment_df(session_summary, "region", "Region")
category_df = compute_segment_df(session_summary, "product_category", "Product_Category")
revenue_by_stage = compute_revenue_by_stage(session_summary)
duration_by_stage = compute_duration_by_stage(session_summary)
insights = compute_business_insights(session_summary, funnel_df, channel_df, device_df, region_df, category_df)


# ========================================================================
# HEADER + EXECUTIVE KPI CARDS
# ========================================================================
st.title("🛒 E-Commerce Customer Funnel Analysis")
st.caption("Executive Dashboard · Browse → Add to Cart → Checkout → Purchase")
st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)

purchase_rate = funnel_df.loc[funnel_df["Stage"] == "Purchase", "Drop_Off_Rate (%)"].values[0]

k1, k2, k3, k4, k5, k6 = st.columns(6)
k1.metric("Total Sessions", f"{insights['total_sessions']:,}")
k2.metric("Total Orders", f"{int(revenue['total_orders']):,}")
k3.metric("Total Revenue", f"${revenue['total_revenue']:,.0f}")
k4.metric("Conversion Rate", f"{insights['conversion_rate']:.2f}%")
k5.metric("Avg Order Value", f"${revenue['average_order_value']:,.2f}" if revenue['total_orders'] else "$0.00")
k6.metric("Purchase Rate", f"{purchase_rate:.2f}%", help="Checkout → Purchase efficiency")

st.markdown("---")

# ========================================================================
# FUNNEL ANALYSIS
# ========================================================================
st.header("📉 Funnel Analysis")
c1, c2 = st.columns(2)
with c1:
    st.plotly_chart(funnel_chart(funnel_df), use_container_width=True)
with c2:
    st.plotly_chart(
        bar_chart(funnel_df, "Stage", "Drop_Off_Rate (%)", COLORS["danger"], "Stage Drop-off Rate", "%"),
        use_container_width=True,
    )

c3, c4 = st.columns(2)
with c3:
    st.plotly_chart(
        bar_chart(revenue_by_stage, "max_funnel_stage", "revenue", COLORS["success"], "Revenue by Funnel Stage", ""),
        use_container_width=True,
    )
with c4:
    st.plotly_chart(
        bar_chart(duration_by_stage, "max_funnel_stage", "session_duration_min", COLORS["warning"],
                   "Average Session Duration", " min"),
        use_container_width=True,
    )

st.markdown("---")

# ========================================================================
# SEGMENT PERFORMANCE — one reusable renderer for channel/device/region/category
# ========================================================================
def render_segment_section(title: str, seg_df: pd.DataFrame, label_col: str):
    st.header(title)
    if seg_df.empty:
        st.info("No data for the current filter selection.")
        return

    top = seg_df.loc[seg_df["Conversion_Rate"].idxmax()]
    m1, m2, m3 = st.columns(3)
    m1.metric(f"Top {label_col.replace('_', ' ')}", top[label_col])
    m2.metric("Its Conversion Rate", f"{top['Conversion_Rate']:.2f}%")
    m3.metric("Its Revenue", f"${top['Total_Revenue']:,.0f}")

    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(
            bar_chart(seg_df, label_col, "Conversion_Rate", COLORS["primary"], "Conversion Rate", "%"),
            use_container_width=True,
        )
    with c2:
        st.plotly_chart(pie_chart(seg_df, label_col, "Total_Sessions", "Session Share"), use_container_width=True)

    st.dataframe(
        seg_df.style.format({
            "Total_Revenue": "${:,.2f}", "AOV": "${:,.2f}", "Conversion_Rate": "{:.2f}%",
            **{f"{s}_Rate": "{:.2f}%" for s in FUNNEL_STAGES},
        }),
        use_container_width=True, hide_index=True,
    )
    st.markdown("---")


render_segment_section("📢 Channel Performance", channel_df, "Channel")
render_segment_section("📱 Device Performance", device_df, "Device")
render_segment_section("🌍 Region Performance", region_df, "Region")
render_segment_section("🛍️ Product Category Performance", category_df, "Product_Category")

# ========================================================================
# BUSINESS INSIGHTS  (mirrors notebook cell 61)
# ========================================================================
st.header("💡 Business Insights")
i1, i2 = st.columns(2)
with i1:
    st.markdown(f"""
    - **Total Sessions:** {insights['total_sessions']:,}
    - **Total Purchases:** {insights['total_purchases']:,}
    - **Overall Conversion Rate:** {insights['conversion_rate']:.2f}%
    - **Total Revenue:** ${insights['total_revenue']:,.2f}
    - **Average Order Value:** ${insights['aov']:,.2f}
    """)
with i2:
    st.markdown(f"""
    - **Best Marketing Channel:** {insights['best_channel']}
    - **Best Performing Device:** {insights['best_device']}
    - **Best Performing Region:** {insights['best_region']}
    - **Best Product Category:** {insights['best_category']}
    - **Biggest Funnel Drop-off Stage:** {insights['drop_stage']}
    """)

st.markdown("---")

# ========================================================================
# STRATEGIC RECOMMENDATIONS  (mirrors notebook cell 63, unchanged content)
# ========================================================================
st.header("🎯 Strategic Business Recommendations")

recs = [
    ("1️⃣ Improve Checkout Experience",
     ["The largest customer drop-off occurs before the Purchase stage.",
      "Simplify the checkout process to reduce cart abandonment.",
      "Offer guest checkout and faster payment options."]),
    ("2️⃣ Invest in High-Performing Marketing Channels",
     [f"Increase marketing investment in {insights['best_channel']}.",
      "Analyze why this channel performs better and replicate the strategy."]),
    ("3️⃣ Optimize Device Experience",
     ["Focus on improving user experience across all devices, especially the lower-performing ones.",
      f"Continue optimizing {insights['best_device']}, as it currently delivers the highest conversion rate."]),
    ("4️⃣ Expand High-Performing Regions",
     [f"Increase promotional campaigns in {insights['best_region']}.",
      "Study customer behavior in this region to identify successful strategies."]),
    ("5️⃣ Promote Best-Selling Product Categories",
     [f"Increase visibility and promotions for {insights['best_category']}.",
      "Bundle popular products with complementary items to increase sales."]),
    ("6️⃣ Improve Customer Conversion",
     ["Reduce friction throughout the purchase journey.",
      "Improve website performance and page loading speed.",
      "Use personalized offers and remarketing campaigns to recover abandoned carts."]),
    ("7️⃣ Monitor Business KPIs Regularly",
     ["Track Conversion Rate, Revenue, AOV, Bounce Rate, and Funnel Performance.",
      "Review marketing performance regularly and optimize underperforming channels."]),
]

for title, points in recs:
    with st.expander(title, expanded=False):
        for p in points:
            st.markdown(f"- {p}")

st.markdown("---")

# ========================================================================
# SUGGESTED IMPROVEMENTS — observations only, notebook logic untouched
# ========================================================================
st.header("🛠️ Suggested Improvements")
st.caption("Observations on the notebook — nothing here was applied to your analysis.")
with st.expander("View suggestions"):
    st.markdown("""
1. **Column naming:** `Drop_Off_Rate (%)` at each row actually stores the
   *carry-forward rate* (sessions this stage ÷ sessions previous stage),
   not a drop-off. A true drop-off would be `100 - carry_forward_rate`.
   The Purchase-stage KPI card above is labeled "Purchase Rate" for this
   reason rather than reusing the ambiguous column name directly.
2. **No random seed** in the data-generation cell — re-running it produces
   different numbers each time, making results hard to reproduce or compare
   across sessions.
3. **`revenue_by_stage` / `duration_by_stage`** (inside the combined
   dashboard cell) aren't reindexed to the funnel stage order, so if a
   stage has zero sessions it can be silently missing from the chart
   instead of showing as zero.
4. **`df.to_csv("funnel_Analysis_Dataset", index=False)`** (early save cell)
   is missing the `.csv` extension.
5. Four analysis cells (channel, device, region, category) repeat the same
   ~25 lines of logic with only the group-by column changed — a good
   candidate to factor into one function, as done here in `compute_segment_df()`.

None of the above were changed in your notebook — they're listed here as
optional follow-ups.
""")

st.caption("Built with Streamlit · Plotly · Pandas — frontend only, analysis logic unchanged from the source notebook.")
