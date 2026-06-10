# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║     Retail Sales Forecasting Dashboard - Streamlit App                     ║
║     Proyek Machine Learning - Damar Syarafi Ramadhan                       ║
║     Dataset: Retail Sales Data with Seasonal Trends and Marketing (v1)     ║
╚══════════════════════════════════════════════════════════════════════════════╝

Cara Menjalankan:
    1. Install dependencies:
       pip install streamlit pandas numpy plotly seaborn matplotlib scikit-learn xgboost

    2. Jalankan aplikasi dari terminal di folder proyek:
       streamlit run app.py

    3. Browser akan otomatis terbuka di http://localhost:8501
"""

# ── Imports ──────────────────────────────────────────────────────────────────
import os
import warnings
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib
matplotlib.use("Agg")           # Non-interactive backend (required for Streamlit)
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import mean_squared_error, r2_score
from xgboost import XGBRegressor

warnings.filterwarnings("ignore")

# ── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Retail Sales Forecasting Dashboard",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    /* ─── Global Reset ─── */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* ─── App Background ─── */
    .stApp {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        min-height: 100vh;
    }

    /* ─── Main Container ─── */
    .main .block-container {
        padding: 2rem 3rem 3rem;
        max-width: 1400px;
    }

    /* ─── Header Banner ─── */
    .dashboard-header {
        background: linear-gradient(135deg, rgba(99,102,241,0.3), rgba(168,85,247,0.3));
        border: 1px solid rgba(99,102,241,0.4);
        border-radius: 20px;
        padding: 2.5rem 3rem;
        margin-bottom: 2rem;
        text-align: center;
        backdrop-filter: blur(10px);
    }
    .dashboard-header h1 {
        font-size: 2.6rem;
        font-weight: 700;
        background: linear-gradient(135deg, #a78bfa, #60a5fa, #34d399);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0 0 0.5rem;
    }
    .dashboard-header p {
        color: rgba(255,255,255,0.65);
        font-size: 1rem;
        margin: 0;
    }

    /* ─── Metric Cards ─── */
    [data-testid="stMetric"] {
        background: rgba(255,255,255,0.06);
        border: 1px solid rgba(255,255,255,0.12);
        border-radius: 16px;
        padding: 1.2rem 1.5rem;
        backdrop-filter: blur(8px);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    [data-testid="stMetric"]:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(99,102,241,0.3);
    }
    [data-testid="stMetricLabel"] p {
        color: rgba(255,255,255,0.6) !important;
        font-size: 0.82rem !important;
        font-weight: 500 !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    [data-testid="stMetricValue"] {
        color: #a78bfa !important;
        font-weight: 700 !important;
        font-size: 1.8rem !important;
    }

    /* ─── Section Headers ─── */
    .section-header {
        color: rgba(255,255,255,0.9);
        font-size: 1.15rem;
        font-weight: 600;
        margin: 1.8rem 0 1rem;
        padding-left: 0.75rem;
        border-left: 3px solid #a78bfa;
    }

    /* ─── Tabs ─── */
    [data-testid="stTabs"] [role="tablist"] {
        background: rgba(255,255,255,0.05);
        border-radius: 12px;
        padding: 0.3rem;
        gap: 0.3rem;
    }
    [data-testid="stTabs"] [role="tab"] {
        border-radius: 9px !important;
        font-weight: 500 !important;
        font-size: 0.92rem !important;
        color: rgba(255,255,255,0.55) !important;
        transition: all 0.2s ease !important;
    }
    [data-testid="stTabs"] [role="tab"][aria-selected="true"] {
        background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
        color: white !important;
        box-shadow: 0 4px 12px rgba(99,102,241,0.4) !important;
    }

    /* ─── Insight Boxes ─── */
    .insight-box {
        background: rgba(99,102,241,0.12);
        border: 1px solid rgba(99,102,241,0.3);
        border-radius: 12px;
        padding: 1.2rem 1.5rem;
        margin-top: 1rem;
        color: rgba(255,255,255,0.8);
        font-size: 0.92rem;
        line-height: 1.7;
    }
    .insight-box strong { color: #a78bfa; }

    /* ─── Prediction Result Card ─── */
    .prediction-card {
        background: linear-gradient(135deg, rgba(52,211,153,0.15), rgba(99,102,241,0.15));
        border: 1px solid rgba(52,211,153,0.4);
        border-radius: 16px;
        padding: 2rem;
        text-align: center;
        margin-top: 1.5rem;
    }
    .prediction-card h2 {
        font-size: 2.8rem;
        font-weight: 700;
        color: #34d399;
        margin: 0;
    }
    .prediction-card p {
        color: rgba(255,255,255,0.6);
        margin: 0.3rem 0 0;
        font-size: 0.9rem;
    }

    /* ─── Performance Cards ─── */
    .perf-card {
        background: rgba(255,255,255,0.06);
        border: 1px solid rgba(255,255,255,0.12);
        border-radius: 14px;
        padding: 1.5rem;
        text-align: center;
        backdrop-filter: blur(8px);
    }
    .perf-card .perf-label {
        color: rgba(255,255,255,0.55);
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        font-weight: 500;
    }
    .perf-card .perf-value {
        font-size: 2.2rem;
        font-weight: 700;
        margin-top: 0.4rem;
    }
    .perf-card .perf-r2 { color: #60a5fa; }
    .perf-card .perf-rmse { color: #f59e0b; }

    /* ─── Sidebar ─── */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e1b4b 0%, #2d2650 100%);
        border-right: 1px solid rgba(99,102,241,0.25);
    }
    [data-testid="stSidebar"] .stMarkdown h2 {
        color: #a78bfa;
        font-size: 1rem;
        font-weight: 600;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid rgba(99,102,241,0.3);
    }

    /* ─── Plotly Chart Container ─── */
    .stPlotlyChart {
        border-radius: 14px;
        overflow: hidden;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║                       DATA & MODEL CACHING LAYER                           ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

PLOTLY_TEMPLATE = "plotly_dark"
PLOTLY_PAPER_BG = "rgba(0,0,0,0)"
PLOTLY_PLOT_BG = "rgba(255,255,255,0.03)"
ACCENT_COLORS = px.colors.qualitative.Vivid


def _get_csv_path() -> str:
    """Resolve path to Retail_sales.csv relative to this script."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    candidates = [
        os.path.join(script_dir, "Retail_sales.csv"),
        os.path.join(script_dir, "data", "Retail_sales.csv"),
    ]
    for p in candidates:
        if os.path.exists(p):
            return p
    raise FileNotFoundError(
        "Retail_sales.csv tidak ditemukan. Pastikan file berada di folder yang sama "
        "dengan app.py atau di subfolder 'data/'."
    )


@st.cache_data(show_spinner="⏳ Memuat dan memproses dataset...")
def load_and_prepare_data() -> tuple[pd.DataFrame, pd.DataFrame, dict, StandardScaler]:
    """
    Memuat Retail_sales.csv, melakukan seluruh Data Preparation
    (rename, datetime, LabelEncoder, StandardScaler, IQR clipping, lag-1),
    dan mengembalikan:
        raw_df    : DataFrame sebelum encoding (untuk EDA visual)
        clean_df  : DataFrame setelah semua preprocessing (untuk model)
        encoders  : dict {col: fitted LabelEncoder}
        scaler    : fitted StandardScaler untuk numerical cols
    """
    csv_path = _get_csv_path()
    df = pd.read_csv(csv_path)

    # ── Rename columns ───────────────────────────────────────────────────────
    df.rename(
        columns={
            "Store ID": "store_ID",
            "Product ID": "product_ID",
            "Store Name": "store_name",
            "Date": "date",
            "Units Sold": "units_sold",
            "Sales Revenue (USD)": "sales_revenue",
            "Discount Percentage": "discount_percentage",
            "Marketing Spend (USD)": "marketing_spend",
            "Store Location": "store_location",
            "Product Category": "product_category",
            "Holiday Effect": "Holiday",
            "Day of the Week": "Weekdays",
        },
        inplace=True,
    )

    # ── Date features ────────────────────────────────────────────────────────
    df["date"] = pd.to_datetime(df["date"])
    df["Month"] = df["date"].dt.month
    df["Day"] = df["date"].dt.day
    df["Year"] = df["date"].dt.year

    # ── Drop unused ID columns ───────────────────────────────────────────────
    df.drop(columns=["store_ID", "product_ID"], inplace=True, errors="ignore")

    # Keep a raw copy for EDA BEFORE encoding/scaling
    raw_df = df.copy()

    # ── Label Encoding ───────────────────────────────────────────────────────
    categorical_cols = ["store_location", "product_category", "Weekdays", "Holiday"]
    encoders: dict[str, LabelEncoder] = {}
    clean_df = df.copy()

    for col in categorical_cols:
        le = LabelEncoder()
        clean_df[col] = le.fit_transform(clean_df[col].astype(str))
        encoders[col] = le

    # ── Standard Scaling ─────────────────────────────────────────────────────
    numerical_cols = ["units_sold", "discount_percentage", "marketing_spend"]
    scaler = StandardScaler()
    clean_df[numerical_cols] = scaler.fit_transform(clean_df[numerical_cols])

    # ── IQR Outlier Clipping ─────────────────────────────────────────────────
    numeric_cols_df = clean_df.select_dtypes(include=[np.number]).columns.tolist()
    # Exclude target so we clip it separately after lag creation
    for col in numeric_cols_df:
        q1 = clean_df[col].quantile(0.25)
        q3 = clean_df[col].quantile(0.75)
        iqr = q3 - q1
        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr
        clean_df[col] = np.clip(clean_df[col], lower, upper)

    # ── Lag Feature ──────────────────────────────────────────────────────────
    clean_df["sales_revenue_lag_1"] = clean_df["sales_revenue"].shift(1)
    clean_df.dropna(inplace=True)

    return raw_df, clean_df, encoders, scaler


@st.cache_resource(show_spinner="🤖 Melatih model XGBoost...")
def train_model(
    _clean_df: pd.DataFrame,
) -> tuple[XGBRegressor, pd.DataFrame, pd.Series, np.ndarray, float, float]:
    """
    Melatih XGBRegressor dengan Time Series Split (80/20).
    Mengembalikan: (model, X_test, y_test, y_pred, r2, rmse)

    Catatan: _clean_df diawali underscore agar Streamlit tidak mencoba hash DataFrame
    (caching by reference via @st.cache_resource).
    """
    features = [
        "units_sold", "Day", "Month", "Year",
        "discount_percentage", "marketing_spend",
        "store_location", "product_category", "Weekdays", "Holiday",
        "sales_revenue_lag_1",
    ]
    target = "sales_revenue"

    split_idx = int(len(_clean_df) * 0.8)
    split_date = _clean_df["date"].iloc[split_idx]

    X_train = _clean_df[_clean_df["date"] < split_date][features]
    y_train = _clean_df[_clean_df["date"] < split_date][target]
    X_test = _clean_df[_clean_df["date"] >= split_date][features]
    y_test = _clean_df[_clean_df["date"] >= split_date][target]

    model = XGBRegressor(
        n_estimators=300,
        learning_rate=0.05,
        max_depth=6,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42,
        verbosity=0,
    )
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    r2 = r2_score(y_test, y_pred)
    rmse = float(np.sqrt(mean_squared_error(y_test, y_pred)))

    return model, X_test, y_test, y_pred, r2, rmse


# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║                          LOAD DATA & MODEL                                 ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

try:
    raw_df, clean_df, encoders, scaler = load_and_prepare_data()
    model, X_test_ts, y_test_ts, y_pred_ts, test_r2, test_rmse = train_model(clean_df)
    data_loaded = True
except FileNotFoundError as e:
    data_loaded = False
    load_error = str(e)

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║                              SIDEBAR                                       ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

with st.sidebar:
    st.markdown(
        """
        <div style='text-align:center; padding: 1rem 0 1.5rem;'>
            <div style='font-size:3rem'>🛒</div>
            <div style='color:#a78bfa; font-size:1.1rem; font-weight:700; margin-top:0.5rem;'>
                RetailForecast AI
            </div>
            <div style='color:rgba(255,255,255,0.45); font-size:0.78rem; margin-top:0.2rem;'>
                Powered by XGBoost
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.divider()

    st.markdown("## 🗓️ Filter Tanggal (Tab 1)")
    if data_loaded:
        min_date = raw_df["date"].min().date()
        max_date = raw_df["date"].max().date()
        date_range = st.date_input(
            "Rentang Tanggal",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date,
            label_visibility="collapsed",
        )
        if len(date_range) == 2:
            start_date, end_date = date_range
        else:
            start_date, end_date = min_date, max_date
    else:
        st.info("Data belum dimuat.")

    st.divider()
    st.markdown("## 🔮 Prediksi Custom (Tab 3)")

    if data_loaded:
        cats = sorted(raw_df["product_category"].dropna().unique().tolist())
        locs = sorted(raw_df["store_location"].dropna().unique().tolist())
        days_map = {
            "Monday": 0, "Tuesday": 1, "Wednesday": 2, "Thursday": 3,
            "Friday": 4, "Saturday": 5, "Sunday": 6,
        }
        unique_weekdays = sorted(raw_df["Weekdays"].dropna().unique().tolist())

        sb_units_sold = st.number_input(
            "Units Sold", min_value=1, max_value=1000, value=50, step=5
        )
        sb_marketing = st.number_input(
            "Marketing Spend (USD)", min_value=0.0, max_value=50000.0,
            value=5000.0, step=100.0
        )
        sb_discount = st.slider(
            "Discount Percentage (%)", min_value=0.0, max_value=50.0,
            value=10.0, step=0.5
        )
        sb_category = st.selectbox("Product Category", options=cats)
        sb_location = st.selectbox("Store Location", options=locs)
        sb_weekday = st.selectbox("Day of the Week", options=unique_weekdays)
        sb_holiday = st.selectbox("Holiday Effect", options=["No", "Yes"])
        sb_day = st.number_input("Day (tanggal)", min_value=1, max_value=31, value=15)
        sb_month = st.number_input("Month", min_value=1, max_value=12, value=6)
        sb_year = st.number_input("Year", min_value=2020, max_value=2030, value=2024)
        sb_lag1 = st.number_input(
            "Prev-Day Revenue (lag_1, USD)", min_value=0.0,
            max_value=500000.0, value=10000.0, step=100.0
        )

        predict_btn = st.button("🚀 Prediksi Sekarang!", use_container_width=True)
    else:
        predict_btn = False

    st.divider()
    st.markdown(
        "<div style='color:rgba(255,255,255,0.3);font-size:0.75rem;text-align:center;'>"
        "Dataset: Retail Sales Data v1<br>Model: XGBoost Regressor<br>"
        "Split: 80% Train / 20% Test</div>",
        unsafe_allow_html=True,
    )

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║                          HANDLE LOAD ERROR                                 ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

if not data_loaded:
    st.error(f"❌ **Error memuat data:** {load_error}")
    st.stop()

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║                          DASHBOARD HEADER                                  ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

st.markdown(
    """
    <div class="dashboard-header">
        <h1>🛒 Retail Sales Forecasting Dashboard</h1>
        <p>Proyek Machine Learning — Damar Syarafi Ramadhan &nbsp;|&nbsp;
           Dataset: Retail Sales Data with Seasonal Trends & Marketing</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ── Filter data by date range ─────────────────────────────────────────────────
mask = (raw_df["date"].dt.date >= start_date) & (raw_df["date"].dt.date <= end_date)
filtered_raw = raw_df[mask]

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║                              TABS                                          ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

tab1, tab2, tab3 = st.tabs([
    "📊 Overview & EDA",
    "🔥 Distribusi & Korelasi",
    "🤖 Forecasting (XGBoost)",
])

# ════════════════════════════════════════════════════════════════════════════════
# TAB 1 — OVERVIEW & EDA
# ════════════════════════════════════════════════════════════════════════════════

with tab1:
    # ── KPI Metrics ──────────────────────────────────────────────────────────
    st.markdown('<p class="section-header">📈 Key Performance Indicators</p>', unsafe_allow_html=True)

    total_revenue = filtered_raw["sales_revenue"].sum()
    total_units = int(filtered_raw["units_sold"].sum())
    avg_marketing = filtered_raw["marketing_spend"].mean()
    avg_discount = filtered_raw["discount_percentage"].mean()

    k1, k2, k3, k4 = st.columns(4)
    k1.metric(
        "💰 Total Revenue",
        f"${total_revenue:,.0f}",
        delta=f"{len(filtered_raw):,} transaksi",
    )
    k2.metric(
        "📦 Total Units Sold",
        f"{total_units:,}",
        delta=f"Avg {total_units / max(len(filtered_raw), 1):.1f} / hari",
    )
    k3.metric(
        "📣 Avg Marketing Spend",
        f"${avg_marketing:,.0f}",
        delta="per transaksi",
    )
    k4.metric(
        "🏷️ Avg Discount",
        f"{avg_discount:.1f}%",
        delta="rata-rata diskon",
    )

    st.divider()

    # ── Sales Revenue Over Time ───────────────────────────────────────────────
    st.markdown('<p class="section-header">📉 Tren Sales Revenue Harian</p>', unsafe_allow_html=True)

    freq_col, _ = st.columns([1, 3])
    with freq_col:
        freq = st.radio(
            "Agregasi",
            ["Harian", "Mingguan", "Bulanan"],
            horizontal=True,
            label_visibility="collapsed",
        )

    freq_map = {"Harian": "D", "Mingguan": "W", "Bulanan": "ME"}
    ts_sales = (
        filtered_raw.set_index("date")["sales_revenue"]
        .resample(freq_map[freq])
        .sum()
        .reset_index()
    )

    fig_ts = go.Figure()
    fig_ts.add_trace(
        go.Scatter(
            x=ts_sales["date"],
            y=ts_sales["sales_revenue"],
            mode="lines+markers",
            name="Sales Revenue",
            line=dict(color="#6366f1", width=2.5),
            marker=dict(size=5, color="#a78bfa"),
            fill="tozeroy",
            fillcolor="rgba(99,102,241,0.1)",
            hovertemplate="<b>%{x|%d %b %Y}</b><br>Revenue: $%{y:,.0f}<extra></extra>",
        )
    )
    fig_ts.update_layout(
        template=PLOTLY_TEMPLATE,
        paper_bgcolor=PLOTLY_PAPER_BG,
        plot_bgcolor=PLOTLY_PLOT_BG,
        height=380,
        margin=dict(l=10, r=10, t=20, b=10),
        xaxis=dict(showgrid=False, title=""),
        yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.06)", title="Revenue (USD)"),
        hovermode="x unified",
        showlegend=False,
    )
    st.plotly_chart(fig_ts, use_container_width=True)

    st.divider()

    # ── Marketing Spend per Category & Product Sales per Month ───────────────
    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown('<p class="section-header">📣 Avg Marketing Spend per Kategori</p>', unsafe_allow_html=True)
        mkt_cat = (
            filtered_raw.groupby("product_category")["marketing_spend"]
            .mean()
            .reset_index()
            .sort_values("marketing_spend", ascending=True)
        )
        fig_mkt = px.bar(
            mkt_cat,
            x="marketing_spend",
            y="product_category",
            orientation="h",
            color="product_category",
            color_discrete_sequence=ACCENT_COLORS,
            labels={"marketing_spend": "Avg Marketing Spend (USD)", "product_category": ""},
        )
        fig_mkt.update_layout(
            template=PLOTLY_TEMPLATE,
            paper_bgcolor=PLOTLY_PAPER_BG,
            plot_bgcolor=PLOTLY_PLOT_BG,
            height=340,
            margin=dict(l=10, r=10, t=10, b=10),
            showlegend=False,
            yaxis=dict(showgrid=False),
            xaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.06)"),
        )
        fig_mkt.update_traces(
            hovertemplate="<b>%{y}</b><br>Avg Spend: $%{x:,.0f}<extra></extra>"
        )
        st.plotly_chart(fig_mkt, use_container_width=True)

    with col_right:
        st.markdown('<p class="section-header">📆 Sales Revenue vs Units Sold per Bulan</p>', unsafe_allow_html=True)
        metric_toggle = st.radio(
            "Tampilkan",
            ["Sales Revenue", "Units Sold"],
            horizontal=True,
            label_visibility="collapsed",
            key="metric_toggle_tab1",
        )
        prod_month = (
            filtered_raw.groupby(["Month", "product_category"])[
                ["sales_revenue", "units_sold"]
            ]
            .sum()
            .reset_index()
        )
        y_col = "sales_revenue" if metric_toggle == "Sales Revenue" else "units_sold"
        y_label = "Sales Revenue (USD)" if metric_toggle == "Sales Revenue" else "Units Sold"

        fig_prod = px.line(
            prod_month,
            x="Month",
            y=y_col,
            color="product_category",
            markers=True,
            color_discrete_sequence=ACCENT_COLORS,
            labels={y_col: y_label, "product_category": "Kategori"},
        )
        fig_prod.update_layout(
            template=PLOTLY_TEMPLATE,
            paper_bgcolor=PLOTLY_PAPER_BG,
            plot_bgcolor=PLOTLY_PLOT_BG,
            height=340,
            margin=dict(l=10, r=10, t=10, b=10),
            xaxis=dict(
                showgrid=False, title="Bulan",
                tickvals=list(range(1, 13)),
                ticktext=["Jan","Feb","Mar","Apr","May","Jun",
                          "Jul","Aug","Sep","Oct","Nov","Dec"],
            ),
            yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.06)"),
            legend=dict(orientation="h", y=-0.25),
        )
        st.plotly_chart(fig_prod, use_container_width=True)

    # ── Insight Box ──────────────────────────────────────────────────────────
    st.markdown(
        """
        <div class="insight-box">
            💡 <strong>Insight:</strong>
            Terdapat lonjakan penjualan yang signifikan pada <strong>November–Desember</strong>
            yang kemungkinan disebabkan oleh promo akhir tahun. Kategori
            <strong>Electronics</strong> dan <strong>Furniture</strong> mengalami kenaikan drastis saat
            musim peak, sementara <strong>Groceries</strong> cenderung stabil sepanjang tahun karena
            permintaan yang konsisten.
        </div>
        """,
        unsafe_allow_html=True,
    )

# ════════════════════════════════════════════════════════════════════════════════
# TAB 2 — DATA DISTRIBUTION & CORRELATION
# ════════════════════════════════════════════════════════════════════════════════

with tab2:
    st.markdown('<p class="section-header">🔥 Heatmap Korelasi Fitur Numerik</p>', unsafe_allow_html=True)

    numeric_cols_corr = raw_df.select_dtypes(include=[np.number]).drop(
        columns=["Month", "Day", "Year"], errors="ignore"
    )

    fig_heat, ax_heat = plt.subplots(figsize=(10, 7))
    fig_heat.patch.set_facecolor("#1a1a2e")
    ax_heat.set_facecolor("#1a1a2e")

    corr_matrix = numeric_cols_corr.corr()
    mask = np.triu(np.ones_like(corr_matrix, dtype=bool), k=1)  # upper triangle only

    sns.heatmap(
        corr_matrix,
        ax=ax_heat,
        annot=True,
        fmt=".2f",
        cmap="coolwarm",
        center=0,
        vmin=-1, vmax=1,
        linewidths=0.5,
        linecolor="#2d3178",
        annot_kws={"size": 10, "color": "white"},
        cbar_kws={"shrink": 0.8},
    )
    ax_heat.set_title("Correlation Heatmap — Fitur Numerik", color="white", pad=15, fontsize=13)
    ax_heat.tick_params(colors="white", labelsize=9)
    plt.xticks(rotation=30, ha="right", color="white")
    plt.yticks(rotation=0, color="white")

    cbar = ax_heat.collections[0].colorbar
    cbar.ax.yaxis.set_tick_params(color="white")
    plt.setp(cbar.ax.yaxis.get_ticklabels(), color="white")
    fig_heat.tight_layout()

    st.pyplot(fig_heat, use_container_width=True)
    plt.close(fig_heat)

    st.divider()

    # ── Scatter Matrix (Plotly) ───────────────────────────────────────────────
    st.markdown('<p class="section-header">🔵 Scatter Matrix: Marketing, Discount & Revenue</p>', unsafe_allow_html=True)

    fig_scatter = px.scatter_matrix(
        raw_df.sample(min(2000, len(raw_df)), random_state=42),
        dimensions=["marketing_spend", "discount_percentage", "sales_revenue"],
        color="product_category",
        color_discrete_sequence=ACCENT_COLORS,
        labels={
            "marketing_spend": "Mktg Spend",
            "discount_percentage": "Discount %",
            "sales_revenue": "Sales Rev",
            "product_category": "Kategori",
        },
        opacity=0.55,
    )
    fig_scatter.update_layout(
        template=PLOTLY_TEMPLATE,
        paper_bgcolor=PLOTLY_PAPER_BG,
        plot_bgcolor=PLOTLY_PLOT_BG,
        height=520,
        margin=dict(l=10, r=10, t=20, b=10),
        legend=dict(orientation="h", y=-0.12),
    )
    fig_scatter.update_traces(marker=dict(size=4))
    st.plotly_chart(fig_scatter, use_container_width=True)

    st.divider()

    # ── Distribution Histogram ────────────────────────────────────────────────
    st.markdown('<p class="section-header">📊 Distribusi Fitur Numerik</p>', unsafe_allow_html=True)

    dist_col = st.selectbox(
        "Pilih fitur untuk melihat distribusi:",
        ["sales_revenue", "units_sold", "marketing_spend", "discount_percentage"],
    )

    fig_dist = px.histogram(
        raw_df,
        x=dist_col,
        color="product_category",
        barmode="overlay",
        nbins=50,
        color_discrete_sequence=ACCENT_COLORS,
        opacity=0.7,
        labels={dist_col: dist_col.replace("_", " ").title(), "product_category": "Kategori"},
    )
    fig_dist.update_layout(
        template=PLOTLY_TEMPLATE,
        paper_bgcolor=PLOTLY_PAPER_BG,
        plot_bgcolor=PLOTLY_PLOT_BG,
        height=380,
        margin=dict(l=10, r=10, t=20, b=10),
        legend=dict(orientation="h", y=-0.2),
    )
    st.plotly_chart(fig_dist, use_container_width=True)

    # ── Insight Correlation ───────────────────────────────────────────────────
    st.markdown(
        """
        <div class="insight-box">
            💡 <strong>Insight Korelasi:</strong><br><br>
            📈 <strong>Marketing Spend → Sales Revenue:</strong>
            Korelasi positif yang jelas — anggaran marketing yang lebih tinggi berkorelasi dengan
            peningkatan pendapatan penjualan. Investasi promosi secara langsung menarik lebih banyak
            pelanggan dan meningkatkan volume transaksi.<br><br>
            🏷️ <strong>Discount Percentage → Sales Revenue:</strong>
            Korelasi cenderung negatif atau lemah — diskon bertujuan menghabiskan stok
            (inventory clearance) sehingga berpotensi mengurangi margin pendapatan per unit meski
            volume terjual bisa meningkat. Perlu dipertimbangkan trade-off antara volume vs. margin.
        </div>
        """,
        unsafe_allow_html=True,
    )

# ════════════════════════════════════════════════════════════════════════════════
# TAB 3 — FORECASTING MODEL (XGBOOST)
# ════════════════════════════════════════════════════════════════════════════════

with tab3:
    # ── Model Performance ─────────────────────────────────────────────────────
    st.markdown('<p class="section-header">🏆 Performa Model XGBoost (Time Series Split)</p>', unsafe_allow_html=True)

    p1, p2, p3, p4 = st.columns(4)
    with p1:
        st.markdown(
            f"""<div class="perf-card">
                <div class="perf-label">Test R² Score</div>
                <div class="perf-value perf-r2">{test_r2:.4f}</div>
            </div>""",
            unsafe_allow_html=True,
        )
    with p2:
        st.markdown(
            f"""<div class="perf-card">
                <div class="perf-label">Test RMSE</div>
                <div class="perf-value perf-rmse">${test_rmse:,.2f}</div>
            </div>""",
            unsafe_allow_html=True,
        )
    with p3:
        train_size = int(len(clean_df) * 0.8)
        st.markdown(
            f"""<div class="perf-card">
                <div class="perf-label">Train Samples</div>
                <div class="perf-value" style="color:#34d399">{train_size:,}</div>
            </div>""",
            unsafe_allow_html=True,
        )
    with p4:
        test_size = len(clean_df) - train_size
        st.markdown(
            f"""<div class="perf-card">
                <div class="perf-label">Test Samples</div>
                <div class="perf-value" style="color:#f472b6">{test_size:,}</div>
            </div>""",
            unsafe_allow_html=True,
        )

    st.divider()

    # ── Actual vs Predicted Chart ─────────────────────────────────────────────
    st.markdown('<p class="section-header">📉 Actual vs Predicted Sales Revenue (Test Set)</p>', unsafe_allow_html=True)

    # Build plot_df
    test_dates = clean_df.loc[X_test_ts.index, "date"]
    plot_df = pd.DataFrame(
        {
            "date": test_dates.values,
            "Actual Sales Revenue": y_test_ts.values,
            "Predicted Sales Revenue": y_pred_ts,
        }
    )
    plotting = (
        plot_df.groupby("date")
        .agg({"Actual Sales Revenue": "sum", "Predicted Sales Revenue": "sum"})
        .reset_index()
    )

    fig_pred = go.Figure()
    fig_pred.add_trace(
        go.Scatter(
            x=plotting["date"],
            y=plotting["Actual Sales Revenue"],
            mode="lines",
            name="Actual",
            line=dict(color="#60a5fa", width=2.5),
            hovertemplate="<b>%{x|%d %b %Y}</b><br>Actual: $%{y:,.0f}<extra></extra>",
        )
    )
    fig_pred.add_trace(
        go.Scatter(
            x=plotting["date"],
            y=plotting["Predicted Sales Revenue"],
            mode="lines",
            name="Predicted",
            line=dict(color="#f59e0b", width=2.5, dash="dash"),
            hovertemplate="<b>%{x|%d %b %Y}</b><br>Predicted: $%{y:,.0f}<extra></extra>",
        )
    )
    fig_pred.update_layout(
        template=PLOTLY_TEMPLATE,
        paper_bgcolor=PLOTLY_PAPER_BG,
        plot_bgcolor=PLOTLY_PLOT_BG,
        height=420,
        margin=dict(l=10, r=10, t=20, b=10),
        xaxis=dict(showgrid=False, title=""),
        yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.06)", title="Sales Revenue (USD)"),
        hovermode="x unified",
        legend=dict(orientation="h", y=1.08, x=0.5, xanchor="center"),
    )
    st.plotly_chart(fig_pred, use_container_width=True)

    st.divider()

    # ── Feature Importance ────────────────────────────────────────────────────
    st.markdown('<p class="section-header">🔑 Feature Importance (XGBoost)</p>', unsafe_allow_html=True)

    feature_names = [
        "units_sold", "Day", "Month", "Year",
        "discount_percentage", "marketing_spend",
        "store_location", "product_category", "Weekdays", "Holiday",
        "sales_revenue_lag_1",
    ]
    importances = model.feature_importances_
    fi_df = (
        pd.DataFrame({"Feature": feature_names, "Importance": importances})
        .sort_values("Importance", ascending=True)
    )

    fig_fi = px.bar(
        fi_df,
        x="Importance",
        y="Feature",
        orientation="h",
        color="Importance",
        color_continuous_scale="Viridis",
        labels={"Importance": "Importance Score", "Feature": ""},
    )
    fig_fi.update_layout(
        template=PLOTLY_TEMPLATE,
        paper_bgcolor=PLOTLY_PAPER_BG,
        plot_bgcolor=PLOTLY_PLOT_BG,
        height=380,
        margin=dict(l=10, r=10, t=10, b=10),
        coloraxis_showscale=False,
    )
    st.plotly_chart(fig_fi, use_container_width=True)

    st.divider()

    # ── Interactive Prediction Form ───────────────────────────────────────────
    st.markdown('<p class="section-header">🔮 Prediksi Sales Revenue Custom</p>', unsafe_allow_html=True)
    st.markdown(
        "<p style='color:rgba(255,255,255,0.5);font-size:0.88rem;margin-top:-0.5rem;'>"
        "Isi parameter di <b>Sidebar kiri</b>, lalu tekan tombol <b>Prediksi Sekarang!</b></p>",
        unsafe_allow_html=True,
    )

    if predict_btn:
        try:
            # ── Encode categorical inputs ─────────────────────────────────────
            def safe_encode(le: LabelEncoder, value: str) -> int:
                """Encode a value; fall back to 0 if unseen."""
                classes = list(le.classes_)
                return le.transform([value])[0] if value in classes else 0

            enc_category = safe_encode(encoders["product_category"], sb_category)
            enc_location = safe_encode(encoders["store_location"], sb_location)
            enc_weekday = safe_encode(encoders["Weekdays"], sb_weekday)
            enc_holiday = safe_encode(encoders["Holiday"], sb_holiday)

            # ── Scale numerical inputs (same scaler fitted on training data) ──
            # scaler was fitted on [units_sold, discount_percentage, marketing_spend]
            raw_numerical = np.array([[sb_units_sold, sb_discount, sb_marketing]])
            scaled_numerical = scaler.transform(raw_numerical)[0]
            s_units_sold, s_discount, s_marketing = scaled_numerical

            # ── Build feature vector ──────────────────────────────────────────
            input_row = np.array([[
                s_units_sold,       # units_sold
                sb_day,             # Day
                sb_month,           # Month
                sb_year,            # Year
                s_discount,         # discount_percentage
                s_marketing,        # marketing_spend
                enc_location,       # store_location
                enc_category,       # product_category
                enc_weekday,        # Weekdays
                enc_holiday,        # Holiday
                sb_lag1,            # sales_revenue_lag_1 (raw USD, same as target)
            ]])

            prediction = float(model.predict(input_row)[0])

            st.markdown(
                f"""
                <div class="prediction-card">
                    <p>Estimasi Sales Revenue</p>
                    <h2>${prediction:,.2f}</h2>
                    <p style="margin-top:0.8rem">
                        🏷️ {sb_category} &nbsp;|&nbsp; 📍 {sb_location}
                        &nbsp;|&nbsp; 📅 {sb_day}/{sb_month}/{sb_year}
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )

            # ── Detail breakdown ──────────────────────────────────────────────
            with st.expander("🔍 Detail Input yang Digunakan Model"):
                detail = {
                    "Fitur": feature_names,
                    "Nilai Raw": [
                        sb_units_sold, sb_day, sb_month, sb_year,
                        sb_discount, sb_marketing,
                        sb_location, sb_category, sb_weekday, sb_holiday, sb_lag1,
                    ],
                    "Nilai ke Model": list(input_row[0]),
                }
                st.dataframe(pd.DataFrame(detail), use_container_width=True, hide_index=True)

        except Exception as e:
            st.error(f"❌ Gagal melakukan prediksi: {e}")

    elif not predict_btn:
        st.markdown(
            """
            <div style="background:rgba(255,255,255,0.04);border:1px dashed rgba(255,255,255,0.15);
                        border-radius:14px;padding:2rem;text-align:center;margin-top:0.5rem;">
                <div style="font-size:2.5rem">🔮</div>
                <p style="color:rgba(255,255,255,0.45);margin:0.5rem 0 0;font-size:0.92rem;">
                    Atur parameter di sidebar lalu klik <strong style="color:#a78bfa">Prediksi Sekarang!</strong>
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown(
    """
    <hr style="border:none;border-top:1px solid rgba(255,255,255,0.08);margin:3rem 0 1rem;">
    <div style="text-align:center;color:rgba(255,255,255,0.25);font-size:0.78rem;padding-bottom:1rem;">
        Retail Sales Forecasting Dashboard &nbsp;·&nbsp;
        Damar Syarafi Ramadhan &nbsp;·&nbsp;
        XGBoost Time Series Forecasting
    </div>
    """,
    unsafe_allow_html=True,
)

# ════════════════════════════════════════════════════════════════════════════════
# HOW TO RUN
# ════════════════════════════════════════════════════════════════════════════════
# 1. Install dependencies (satu kali saja):
#    pip install streamlit pandas numpy plotly seaborn matplotlib scikit-learn xgboost
#
# 2. Pastikan file Retail_sales.csv berada di folder yang sama dengan app.py
#
# 3. Jalankan di terminal:
#    streamlit run app.py
#
# 4. Browser akan otomatis membuka http://localhost:8501
# ════════════════════════════════════════════════════════════════════════════════
