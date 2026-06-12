"""
streamlit_app.py – House Transaction Forecast · Home
"""

import mlflow
import streamlit as st

st.set_page_config(
    page_title="House Forecast",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS ──────────────────────────────────────────────────────────────────────
st.markdown(
    """
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

  html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

  /* Sidebar */
  section[data-testid="stSidebar"] {
    background: #0f172a;
    border-right: 1px solid #1e293b;
  }
  section[data-testid="stSidebar"] * { color: #94a3b8 !important; }
  section[data-testid="stSidebar"] h1,
  section[data-testid="stSidebar"] h2,
  section[data-testid="stSidebar"] h3 { color: #f1f5f9 !important; }

  /* Metric cards */
  .metric-card {
    background: #f8fafc; border: 1px solid #e2e8f0;
    border-radius: 12px; padding: 18px 20px;
    text-align: center;
  }
  .metric-card .val  { font-size: 28px; font-weight: 700; color: #0f172a; font-family: 'JetBrains Mono'; }
  .metric-card .lbl  { font-size: 12px; color: #64748b; margin-top: 4px; text-transform: uppercase; letter-spacing: .05em; }
  .metric-card.good  .val { color: #16a34a; }
  .metric-card.warn  .val { color: #d97706; }
  .metric-card.bad   .val { color: #dc2626; }

  /* Upload zone */
  .upload-hint {
    background: #eff6ff; border: 2px dashed #93c5fd;
    border-radius: 10px; padding: 14px 18px;
    font-size: 13px; color: #1d4ed8; margin-bottom: 8px;
  }

  /* Section header */
  .section-header {
    font-size: 11px; font-weight: 600; letter-spacing: .08em;
    text-transform: uppercase; color: #94a3b8;
    margin: 24px 0 10px; padding-bottom: 6px;
    border-bottom: 1px solid #1e293b;
  }

  /* Tag badge */
  .badge {
    display: inline-block; padding: 2px 10px;
    border-radius: 999px; font-size: 11px; font-weight: 600;
  }
  .badge-blue  { background:#dbeafe; color:#1d4ed8; }
  .badge-green { background:#dcfce7; color:#16a34a; }
  .badge-amber { background:#fef3c7; color:#d97706; }

  div[data-testid="stFileUploader"] label { font-size: 13px !important; }
  .stButton > button {
    border-radius: 8px !important; font-weight: 600 !important;
    font-size: 14px !important;
  }
  .stButton > button[kind="primary"] {
    background: #1d4ed8 !important; border: none !important;
  }
</style>
""",
    unsafe_allow_html=True,
)


# ── Helper: MLflow baseline metrics ───────────────────────────────────────────
def _show_mlflow_sidebar():
    """Show baseline metrics from MLflow run recently."""
    try:
        client = mlflow.tracking.MlflowClient()
        exp = client.get_experiment_by_name("catboost_timeseries")
        if exp is None:
            st.caption("Chưa có MLflow run nào.")
            return
        runs = client.search_runs(
            experiment_ids=[exp.experiment_id],
            filter_string="tags.mlflow.runName = 'pipeline_run'",
            order_by=["start_time DESC"],
            max_results=1,
        )
        if not runs:
            st.caption("Chưa có pipeline run.")
            return
        run = runs[0]
        m = run.data.metrics

        def _fmt(key, default="–"):
            v = m.get(key)
            return f"{v:.4f}" if v is not None else default

        items = [
            ("Competition Score", "holdout_competition_score"),
            ("MAE", "holdout_mae"),
            ("RMSE", "holdout_rmse"),
            ("MAPE", "holdout_mape"),
            ("R²", "holdout_r2"),
            ("Bad Rate", "holdout_bad_rate"),
        ]
        for lbl, key in items:
            val = _fmt(key)
            st.markdown(
                f"<div style='display:flex;justify-content:space-between;"
                f"font-size:13px;padding:4px 0;border-bottom:1px solid #1e293b'>"
                f"<span style='color:#64748b'>{lbl}</span>"
                f"<span style='color:#f1f5f9;font-family:JetBrains Mono'>{val}</span>"
                f"</div>",
                unsafe_allow_html=True,
            )
        st.markdown(
            f"<div style='font-size:11px;color:#475569;margin-top:8px'>"
            f"Run: <code style='color:#7c3aed'>{run.info.run_id[:8]}…</code></div>",
            unsafe_allow_html=True,
        )
    except Exception:
        st.caption("MLflow is disable.")


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🏠 House Forecast")
    st.markdown(
        "<div style='font-size:12px;color:#475569;margin-bottom:20px'>"
        "Real-estate transaction forecasting</div>",
        unsafe_allow_html=True,
    )

    st.markdown("<div class='section-header'>Baseline Metrics</div>", unsafe_allow_html=True)
    _show_mlflow_sidebar()

# ── Home content ──────────────────────────────────────────────────────────────
st.title("🏠 House Transaction Forecast")
st.markdown(
    """
Welcome! Use the sidebar menu to navigate:

- **📤 Upload & Predict** – upload new data and view predictions  
- **📈 Sector Forecast** – view forecasts by sector  
- **📊 Monitoring** – track model drift & performance  
"""
)
