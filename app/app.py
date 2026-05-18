import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# Safety check for Prophet installation
try:
    from prophet import Prophet
    prophet_available = True
except Exception:
    prophet_available = False

# Tightened Application Page Configuration
st.set_page_config(
    page_title="Enterprise Sales Intelligence",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Premium Global CSS Overhaul (Aggressive Typography Scale & Dynamic Density)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght=400;500;600;700&display=swap');
    
    /* GLOBAL TEXT SCALE & WHITESPACE MINIMIZATION */
    html, body, p, div, [data-testid="stWidgetLabel"], .stTabs button, .stButton button, label {
        font-family: 'Inter', sans-serif !important;
        font-size: 19px !important;
        font-weight: 500;
    }
    
    .block-container {
        padding-top: 1.2rem !important;
        padding-bottom: 1.2rem !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
    }
    
    div[data-testid="stVerticalBlock"] {
        gap: 0.75rem !important;
    }
    
    /* MAXIMIZED HEADER SYSTEM */
    .dashboard-header {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        padding: 26px 32px;
        border-radius: 12px;
        margin-bottom: 14px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    }
    .dashboard-title {
        font-size: 36px !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        margin: 0 0 6px 0 !important;
        letter-spacing: -1px;
    }
    .dashboard-subtitle {
        font-size: 18px !important;
        color: #94a3b8 !important;
        margin: 0 !important;
        font-weight: 400;
    }
    
    /* LAYOUT CONTAINERS WITH SOLID DEPTH */
    .content-block {
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 22px 26px;
        background-color: #ffffff;
        margin-bottom: 12px;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.03), 0 4px 6px -2px rgba(0, 0, 0, 0.02);
    }
    
    .chart-wrapper {
        border: 1px solid #f1f5f9;
        border-radius: 8px;
        padding: 12px;
        background-color: #f8fafc;
    }
    
    /* HIGH-CONTRAST ACCENTED METRIC CARDS */
    .kpi-card {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-top: 5px solid #2563eb;
        border-radius: 10px;
        padding: 20px 22px;
        display: flex;
        align-items: center;
        gap: 20px;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05), 0 4px 6px -2px rgba(0, 0, 0, 0.01);
        transition: transform 0.2s ease;
    }
    .kpi-card:hover {
        transform: translateY(-2px);
    }
    .kpi-icon {
        font-size: 30px;
        background: #eff6ff;
        color: #1d4ed8;
        width: 58px;
        height: 58px;
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
    }
    .kpi-content {
        display: flex;
        flex-direction: column;
    }
    .kpi-label {
        font-size: 14px !important;
        color: #64748b;
        text-transform: uppercase;
        font-weight: 700;
        letter-spacing: 0.8px;
        margin: 0;
    }
    .kpi-value {
        font-size: 34px !important;
        color: #0f172a;
        font-weight: 700;
        margin: 2px 0 0 0;
        letter-spacing: -0.5px;
    }
    
    /* HIGH-READABILITY STRATEGY BLOCKS */
    .insight-box {
        background-color: #f0fdf4;
        border-left: 6px solid #10b981;
        border-radius: 6px;
        padding: 18px 22px;
        margin: 12px 0;
        font-size: 18px !important;
        color: #14532d;
        font-weight: 500;
    }
    
    /* LARGE NAVIGATION TABS */
    .stTabs [data-baseweb="tab-list"] {
        gap: 14px;
        border-bottom: 2px solid #e2e8f0;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding-left: 24px;
        padding-right: 24px;
        font-size: 18px !important;
        font-weight: 700 !important;
        color: #64748b;
    }
    .stTabs [aria-selected="true"] {
        background-color: #eff6ff !important;
        color: #2563eb !important;
    }
    
    /* ENLARGED FORM INPUTS & SELECTORS */
    input, select, textarea, div[data-baseweb="select"] * {
        font-size: 18px !important;
    }
    
    /* SIDEBAR TYPOGRAPHY SCALING */
    .sidebar-section-title {
        font-size: 14px !important;
        font-weight: 700;
        color: #475569;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        margin-bottom: 8px;
        display: block;
    }
    
    .chat-response-wrapper {
        background-color: #ffffff; 
        border-radius: 8px; 
        padding: 22px; 
        margin: 16px 0; 
        border: 1px solid #e2e8f0; 
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.03);
    }
</style>
""", unsafe_allow_html=True)

# Data Infrastructure Layer
@st.cache_data
def load_data():
    BASE_DIR = Path(__file__).resolve().parent
    DATA_PATH = BASE_DIR.parent / "data" / "cleaned_sales_data.csv"

    df = pd.read_csv(DATA_PATH)
    df["Order_Date"] = pd.to_datetime(df["Order_Date"])
    return df
    
@st.cache_data
def load_customer_segments():
    BASE_DIR = Path(__file__).resolve().parent
    SEG_PATH = BASE_DIR.parent / "data" / "customer_segments.csv"

    seg = pd.read_csv(SEG_PATH)
    if "Last_Order_Date" in seg.columns:
        seg["Last_Order_Date"] = pd.to_datetime(seg["Last_Order_Date"])
    return seg

def money(value):
    return f"${value:,.0f}"

# High-Fidelity Plotly Style Engine (Scaled for Larger Layout Context)
def style_chart(fig, height=270, title=None):
    fig.update_layout(
        height=height,
        template="plotly_white",
        margin=dict(l=15, r=15, t=60 if title else 20, b=20),
        font=dict(family="Inter", size=15, color="#475569"),
        title=title,
        title_font=dict(size=18, color="#0f172a", weight="bold"),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        hovermode="x unified",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(size=14)
        )
    )
    fig.update_xaxes(showgrid=False, linecolor="#e2e8f0", linewidth=1, title_font=dict(size=15, weight="bold"), tickfont=dict(size=13))
    fig.update_yaxes(showgrid=True, gridcolor="#f1f5f9", zeroline=False, linecolor="#e2e8f0", linewidth=1, title_font=dict(size=15, weight="bold"), tickfont=dict(size=13))
    return fig

def render_kpi(col, icon, label, value):
    col.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-icon">{icon}</div>
        <div class="kpi-content">
            <span class="kpi-label">{label}</span>
            <span class="kpi-value">{value}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

def relabel_customer_segments(seg):
    seg = seg.copy()
    if not {"Customer_Segment", "Total_Sales"}.issubset(seg.columns):
        return seg
    freq_col = "Frequency" if "Frequency" in seg.columns else ("Total_Orders" if "Total_Orders" in seg.columns else None)
    rec_col = "Recency" if "Recency" in seg.columns else None
    
    profile = seg.groupby("Customer_Segment").agg(Total_Sales=("Total_Sales", "mean"))
    if freq_col:
        profile["Frequency"] = seg.groupby("Customer_Segment")[freq_col].mean()
    else:
        profile["Frequency"] = 1
        
    if rec_col:
        profile["Recency"] = seg.groupby("Customer_Segment")[rec_col].mean()
        profile["Score"] = profile["Total_Sales"].rank() + profile["Frequency"].rank() + profile["Recency"].rank(ascending=False)
    else:
        profile["Score"] = profile["Total_Sales"].rank() + profile["Frequency"].rank()
        
    ordered = profile.sort_values("Score", ascending=False).index.tolist()
    names = ["VIP Customers", "Loyal Customers", "Occasional Customers", "Low Activity Customers"]
    mapping = {old: names[i] if i < len(names) else f"Customer Group {i+1}" for i, old in enumerate(ordered)}
    seg["Customer_Segment"] = seg["Customer_Segment"].map(mapping).fillna(seg["Customer_Segment"])
    return seg

def ai_answer(question, data, seg_data):
    q = question.lower().strip()
    if not q:
        return "👋 **Welcome to Sales Intelligence Assist.** Enter a query above or click a suggestion below to probe your current operational metrics slice."
    
    sales = data["Sales"].sum()
    profit = data["Profit"].sum() if "Profit" in data.columns else 0
    margin = (profit / sales * 100) if sales else 0
    
    if any(k in q for k in ["region", "territory", "place", "where"]):
        r_sales = data.groupby("Region")["Sales"].sum()
        r_best = r_sales.idxmax()
        r_worst = r_sales.idxmin()
        if any(k in q for k in ["worst", "lowest", "least", "bottom"]):
            return f"📉 The lowest performing market territory is <b>{r_worst}</b> with total processing revenues of {money(r_sales[r_worst])}."
        return f"🌍 The dominant performing market region is <b>{r_best}</b> with total processing revenues of <b>{money(r_sales[r_best])}</b>."
        
    if any(k in q for k in ["category", "department", "stock class"]):
        c_sales = data.groupby("Category")["Sales"].sum()
        c_best = c_sales.idxmax()
        if any(k in q for k in ["worst", "lowest", "least", "bottom"]):
            c_worst = c_sales.idxmin()
            return f"📦 The lowest velocity inventory department category is <b>{c_worst}</b> generating {money(c_sales[c_worst])}."
        return f"🏆 The primary volume product category path is <b>{c_best}</b>, bringing in <b>{money(c_sales[c_best])}</b>."
        
    if any(k in q for k in ["product", "item", "sku", "sell"]):
        p_sales = data.groupby("Product_Name")["Sales"].sum()
        p_best = p_sales.idxmax()
        return f"⭐ The single highest item conversion driver across this vector matrix slice is:<br><b>{p_best}</b> (Totaling <b>{money(p_sales[p_best])}</b>)."
        
    if any(k in q for k in ["margin", "profit", "earnings", "leakage", "loss"]):
        loss_df = data[data["Profit"] < 0]
        return f"📊 <b>Financial Health Parameters:</b> Net operating margins sit at <b>{margin:.2f}%</b> on absolute profits of <b>{money(profit)}</b>.<br>⚠️ There are currently <b>{loss_df.shape[0]}</b> transactional nodes functioning at an operating loss."
    
    return f"📌 <b>Data Slice Scan Summary:</b> under current filter structures, the matrix displays <b>{money(sales)}</b> in total gross revenue, spanning <b>{data['Order_ID'].nunique():,}</b> validated invoices, operating at an overall efficiency margin of <b>{margin:.2f}%</b>."

# Load Assets
df = load_data()
customer_segments = relabel_customer_segments(load_customer_segments())

if "Profit" not in df.columns:
    df["Profit"] = df["Sales"] * 0.12

# MAIN FRAME CONTROL BANNER
st.markdown("""
<div class="dashboard-header">
    <h1 class="dashboard-title">🛒 Sales Intelligence Console</h1>
    <p class="dashboard-subtitle">Enterprise Data Optimization Core • Predictive Models & Advanced Audience Clustering</p>
</div>
""", unsafe_allow_html=True)

# SIDEBAR CONTROL DECK
with st.sidebar:
    st.markdown("<h2 style='font-size: 24px; color: #0f172a; margin-bottom: 4px; font-weight:700;'>🎛️ Control Center</h2>", unsafe_allow_html=True)
    st.caption("Adjust dynamic operational filters")
    st.markdown("<hr style='margin: 14px 0; border-color: #cbd5e1;'>", unsafe_allow_html=True)

    min_date = df["Order_Date"].min().date()
    max_date = df["Order_Date"].max().date()

    with st.container():
        st.markdown('<span class="sidebar-section-title">📅 Temporal Boundaries</span>', unsafe_allow_html=True)
        date_range = st.date_input("Select Range", value=(min_date, max_date), min_value=min_date, max_value=max_date, label_visibility="collapsed")

    st.markdown("<div style='margin-top:16px;'></div>", unsafe_allow_html=True)

    with st.container():
        st.markdown('<span class="sidebar-section-title">🌍 Inventory & Logistics</span>', unsafe_allow_html=True)
        region_options = ["All Regions"] + sorted(df["Region"].dropna().unique().tolist())
        selected_region = st.selectbox("Market Target Region", options=region_options, label_visibility="collapsed")
        
        st.markdown("<div style='margin-top:10px;'></div>", unsafe_allow_html=True)
        category_options = ["All Categories"] + sorted(df["Category"].dropna().unique().tolist())
        selected_category = st.selectbox("Stock Core Category", options=category_options, label_visibility="collapsed")

    st.markdown("<div style='margin-top:16px;'></div>", unsafe_allow_html=True)

    with st.container():
        st.markdown('<span class="sidebar-section-title">👥 Consumer Demographics</span>', unsafe_allow_html=True)
        segment_options = ["All Customer Segments"] + sorted(df["Segment"].dropna().unique().tolist())
        selected_segment = st.selectbox("Consumer Cohort Target", options=segment_options, label_visibility="collapsed")

# Filter execution logic
start_date, end_date = date_range if isinstance(date_range, tuple) and len(date_range) == 2 else (min_date, max_date)
mask = (df["Order_Date"].dt.date >= start_date) & (df["Order_Date"].dt.date <= end_date)

if selected_region != "All Regions":
    mask &= (df["Region"] == selected_region)
if selected_category != "All Categories":
    mask &= (df["Category"] == selected_category)
if selected_segment != "All Customer Segments":
    mask &= (df["Segment"] == selected_segment)

filtered = df[mask].copy()

if filtered.empty:
    st.warning("No operational data matrix matched criteria.")
    st.stop()

# Calculations Pipeline
total_sales = filtered["Sales"].sum()
total_orders = filtered["Order_ID"].nunique()
total_customers = filtered["Customer_ID"].nunique()
total_profit = filtered["Profit"].sum()
avg_order_value = total_sales / total_orders if total_orders else 0
profit_margin = (total_profit / total_sales * 100) if total_sales else 0

# Presentation Tabs Layout
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📊 Executive Summary", "🤖 Stock Fulfillment", "💰 Profit Architecture", 
    "👥 Client Clusters", "🚨 Process Deviations", "💬 Data Assistant"
])

# TAB 1: EXECUTIVE SUMMARY
with tab1:
    st.markdown('<div class="content-block">', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    render_kpi(c1, "💰", "Revenue", money(total_sales))
    render_kpi(c2, "📦", "Invoices", f"{total_orders:,}")
    render_kpi(c3, "👥", "Clients", f"{total_customers:,}")
    render_kpi(c4, "📈", "Margin", f"{profit_margin:.2f}%")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="content-block">', unsafe_allow_html=True)
    monthly_sales = filtered.groupby(pd.Grouper(key="Order_Date", freq="ME"))["Sales"].sum().reset_index()
    monthly_sales.columns = ["ds", "y"]

    if prophet_available and len(monthly_sales) >= 12:
        model = Prophet(yearly_seasonality=True, weekly_seasonality=False, daily_seasonality=False)
        model.fit(monthly_sales)
        future = model.make_future_dataframe(periods=6, freq="ME")
        forecast = model.predict(future)
        future_forecast = forecast[forecast["ds"] > monthly_sales["ds"].max()]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=monthly_sales["ds"], y=monthly_sales["y"], mode="lines+markers", name="Actual Performance", line=dict(color="#0f172a", width=3, shape="spline")))
        fig.add_trace(go.Scatter(x=future_forecast["ds"], y=future_forecast["yhat"], mode="lines+markers", name="Predictive Forecast Stream", line=dict(color="#10b981", width=3, dash="dash", shape="spline")))
        
        st.markdown('<div class="chart-wrapper">', unsafe_allow_html=True)
        st.plotly_chart(style_chart(fig, 300, "6-Month Predictive Revenue Projection Pipeline Stream"), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.caption("Forecasting engine demands a minimum threshold of 12 continuous historical month intervals.")
    st.markdown('</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="content-block">', unsafe_allow_html=True)
        cat = filtered.groupby("Category")["Sales"].sum().reset_index().sort_values("Sales", ascending=False)
        fig = px.bar(cat, x="Category", y="Sales", text_auto=",.0f", color="Sales", color_continuous_scale=["#1e293b", "#3b82f6"])
        fig.update_coloraxes(showscale=False)
        fig.update_traces(opacity=0.95, width=0.35, textposition="outside")
        st.markdown('<div class="chart-wrapper">', unsafe_allow_html=True)
        st.plotly_chart(style_chart(fig, 260, "Revenue Breakdown Matrix by Operational Category"), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col2:
        st.markdown('<div class="content-block">', unsafe_allow_html=True)
        reg = filtered.groupby("Region")["Sales"].sum().reset_index()
        fig = px.pie(reg, values="Sales", names="Region", hole=0.6, color_discrete_sequence=["#0f172a", "#2563eb", "#475569", "#38bdf8"])
        fig.update_traces(textposition="inside", textinfo="percent+label", marker=dict(line=dict(color="#ffffff", width=2)))
        st.markdown('<div class="chart-wrapper">', unsafe_allow_html=True)
        st.plotly_chart(style_chart(fig, 260, "Territorial Market Share Allocation Matrix"), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# TAB 2: SMART PRODUCT RECOMMENDATIONS
with tab2:
    st.markdown('<div class="content-block">', unsafe_allow_html=True)
    st.markdown('<div class="chart-wrapper">', unsafe_allow_html=True)
    product_sales = filtered.groupby("Product_Name")["Sales"].sum().reset_index().sort_values("Sales", ascending=False).head(5)
    fig = px.bar(product_sales, x="Sales", y="Product_Name", orientation="h", text_auto=",.0f", color="Sales", color_continuous_scale=["#475569", "#0f172a"])
    fig.update_coloraxes(showscale=False)
    fig.update_traces(opacity=0.95, textposition="inside")
    st.plotly_chart(style_chart(fig, 290, "Inventory Asset Conversion Velocity Trends (Top Performers)"), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    best_product = product_sales.iloc[0]["Product_Name"]
    st.markdown(f'<div class="insight-box">✅ <b style="font-weight:700;">Strategic Supply Optimization Mandate:</b> Prioritize fulfillment channels for <b>{best_product}</b> to intercept compounding volume demands.</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# TAB 3: PROFIT ANALYTICS
with tab3:
    st.markdown('<div class="content-block">', unsafe_allow_html=True)
    p1, p2, p3, p4 = st.columns(4)
    render_kpi(p1, "💼", "Net Earnings", money(total_profit))
    render_kpi(p2, "📈", "Margin Index", f"{profit_margin:.2f}%")
    render_kpi(p3, "🛒", "System AOV", f"${avg_order_value:,.2f}")
    loss_count = filtered[filtered["Profit"] < 0].shape[0]
    render_kpi(p4, "🚨", "Leakage Nodes", f"{loss_count:,}")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="chart-wrapper">', unsafe_allow_html=True)
        pc = filtered.groupby("Category")["Profit"].sum().reset_index().sort_values("Profit", ascending=False)
        fig = px.bar(pc, x="Category", y="Profit", text_auto=",.0f", color="Profit", color_continuous_scale=["#0f172a", "#2563eb"])
        fig.update_coloraxes(showscale=False)
        fig.update_traces(opacity=0.95, width=0.35, textposition="outside")
        st.plotly_chart(style_chart(fig, 250, "Net Operating Yields mapped by Category Groupings"), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="chart-wrapper">', unsafe_allow_html=True)
        rm = filtered.groupby("Region").agg(Sales=("Sales", "sum"), Profit=("Profit", "sum")).reset_index()
        rm["Profit Margin"] = (rm["Profit"] / rm["Sales"] * 100).fillna(0)
        fig = px.bar(rm, x="Region", y="Profit Margin", text_auto=".2f", color="Profit Margin", color_continuous_scale=["#475569", "#0284c7"])
        fig.update_coloraxes(showscale=False)
        fig.update_traces(opacity=0.95, width=0.35, textposition="outside")
        st.plotly_chart(style_chart(fig, 250, "Net Structural Profit Margin Ratios by Territory %"), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# TAB 4: CUSTOMER SEGMENTATION
with tab4:
    st.markdown('<div class="content-block">', unsafe_allow_html=True)
    cs = customer_segments[customer_segments["Customer_ID"].isin(filtered["Customer_ID"].unique())].copy()
    if cs.empty: cs = customer_segments.copy()
        
    left, right = st.columns(2)
    with left:
        st.markdown('<div class="chart-wrapper">', unsafe_allow_html=True)
        count = cs["Customer_Segment"].value_counts().reset_index()
        count.columns = ["Customer Segment", "Customers"]
        fig = px.bar(count, x="Customer Segment", y="Customers", text_auto=True, color="Customers", color_continuous_scale=["#1e293b", "#3b82f6"])
        fig.update_coloraxes(showscale=False)
        fig.update_traces(opacity=0.95, width=0.35)
        st.plotly_chart(style_chart(fig, 250, "Dynamic Account Density Split by Cohort Classification"), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with right:
        st.markdown('<div class="chart-wrapper">', unsafe_allow_html=True)
        ss = cs.groupby("Customer_Segment")["Total_Sales"].sum().reset_index().sort_values("Total_Sales", ascending=False)
        fig = px.pie(ss, values="Total_Sales", names="Customer_Segment", hole=0.6, color_discrete_sequence=["#0f172a", "#1d4ed8", "#64748b", "#38bdf8"])
        fig.update_traces(textposition="inside", textinfo="percent+label", marker=dict(line=dict(color="#ffffff", width=2)))
        st.plotly_chart(style_chart(fig, 250, "Total Asset Equity Share Breakdown by Segment Class"), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# TAB 5: SALES ANOMALY DETECTION
with tab5:
    st.markdown('<div class="content-block">', unsafe_allow_html=True)
    ad = filtered.groupby(pd.Grouper(key="Order_Date", freq="ME"))["Sales"].sum().reset_index()
    ad.columns = ["Month", "Sales"]
    ad["Rolling_Avg"] = ad["Sales"].rolling(3).mean()
    ad["Rolling_Std"] = ad["Sales"].rolling(3).std()
    ad["Upper"] = ad["Rolling_Avg"] + 1.2 * ad["Rolling_Std"]
    ad["Lower"] = ad["Rolling_Avg"] - 1.2 * ad["Rolling_Std"]
    ad["Anomaly"] = ad.apply(lambda r: "Spike" if r["Sales"] > r["Upper"] else ("Drop" if r["Sales"] < r["Lower"] else "Normal"), axis=1)
    anomalies = ad[ad["Anomaly"] != "Normal"]
    
    st.markdown('<div class="chart-wrapper">', unsafe_allow_html=True)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=ad["Month"], y=ad["Sales"], mode="lines+markers", name="Observed Sales Track", line=dict(color="#0f172a", width=2.5, shape="spline")))
    fig.add_trace(go.Scatter(x=anomalies["Month"], y=ad.loc[anomalies.index, "Sales"], mode="markers", name="Outlier Threshold Deviation", marker=dict(size=12, color="#f43f5e", symbol="diamond")))
    st.plotly_chart(style_chart(fig, 310, "Volatility Vector Mapping Engine (Rolling Deviation Bounds)"), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# TAB 6: DIAGNOSTIC AI CO-PILOT ASSISTANT
with tab6:
    st.markdown('<div class="content-block">', unsafe_allow_html=True)
    st.markdown("<h3 style='font-size:22px; margin:0 0 16px 0; color:#0f172a; font-weight:700;'>💬 Automated Insights Processing Core</h3>", unsafe_allow_html=True)
    
    # Initialize necessary session state keys cleanly
    if "chat_query" not in st.session_state:
        st.session_state.chat_query = ""
    if "form_submitted" not in st.session_state:
        st.session_state.form_submitted = False

    # Professional Section Header for Quick Routes
    st.markdown("<p style='font-size:14px; font-weight:700; color:#475569; text-transform:uppercase; margin:10px 0 10px 0; letter-spacing:0.75px;'>🎯 Suggested Quick Diagnostics Pipeline Routes</p>", unsafe_allow_html=True)
    
    sq1, sq2, sq3, sq4 = st.columns(4)
    if sq1.button("🌍 What is the best region?", key="ai_btn_best_region"):
        st.session_state.chat_query = "best region"
        st.session_state.form_submitted = True
        st.rerun()
    if sq2.button("📉 Which region is worst?", key="ai_btn_worst_region"):
        st.session_state.chat_query = "worst region"
        st.session_state.form_submitted = True
        st.rerun()
    if sq3.button("📦 Top performance category", key="ai_btn_best_category"):
        st.session_state.chat_query = "best category"
        st.session_state.form_submitted = True
        st.rerun()
    if sq4.button("📊 Profit margin stats", key="ai_btn_profit_margin"):
        st.session_state.chat_query = "profit margin"
        st.session_state.form_submitted = True
        st.rerun()

    st.markdown("<div style='margin-top: 14px;'></div>", unsafe_allow_html=True)

    # Search Box Input Form
    with st.form(key="ai_chat_form", clear_on_submit=False):
        user_input = st.text_input(
            "Search Request:", 
            value=st.session_state.chat_query, 
            placeholder="Type your query (e.g., best region, overall profit margin)...", 
            label_visibility="collapsed"
        )
        submit_btn = st.form_submit_button(label="Submit")
        
        if submit_btn:
            st.session_state.chat_query = user_input
            st.session_state.form_submitted = True

    # Only parse data matrix and render response if an intentional execution action occurred
    if st.session_state.form_submitted and st.session_state.chat_query:
        answer = ai_answer(st.session_state.chat_query, filtered, customer_segments)
        
        st.markdown(f"""
        <div class="chat-response-wrapper">
            <p style="margin:0; font-size: 19px; color:#1e293b; line-height:1.6; font-weight:500;">{answer}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Reset the submission flag cleanly so typing doesn't prematurely trigger responses on next interaction lifecycle
        st.session_state.form_submitted = False
    else:
        # Default placeholder layout state before any button inputs or text strings are submitted
        st.markdown("""
        <div class="chat-response-wrapper" style="background-color: #f8fafc; border-style: dashed;">
            <p style="margin:0; font-size: 19px; color:#64748b; font-style: italic; font-weight:400; text-align: center;">
                👋 Core analytical processor ready. Choose a pipeline shortcut route or type a custom inquiry above and press Submit.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown('</div>', unsafe_allow_html=True)
