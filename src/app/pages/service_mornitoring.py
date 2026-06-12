"""
service_monitoring.py – Monitoring Dashboard
Track model performance, drift detection & data health.
Only uses existing API endpoints: /health, /metrics, /drift, /sectors
"""
from __future__ import annotations

import os
from datetime import datetime
from typing import Any, Dict, List, Optional

import pandas as pd
import plotly.graph_objects as go
import requests
import streamlit as st

try:
    import mlflow
except ImportError:
    mlflow = None

# ── Config ───────────────────────────────────────────────────────────────────
API_BASE_URL = os.environ.get("API_BASE_URL", "http://localhost:8000/api/v1")
st.set_page_config(page_title="Monitoring", page_icon="📊", layout="wide")

# ── CSS (đồng bộ với các page khác) ─────────────────────────────────────────
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

section[data-testid="stSidebar"] {
    background: #0f172a;
    border-right: 1px solid #1e293b;
}
section[data-testid="stSidebar"] * { color: #94a3b8 !important; }
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 { color: #f1f5f9 !important; }

.metric-card {
    background: #f8fafc; border: 1px solid #e2e8f0;
    border-radius: 12px; padding: 18px 20px;
    text-align: center;
}
.metric-card .val { font-size: 28px; font-weight: 700; color: #0f172a; font-family: 'JetBrains Mono'; }
.metric-card .lbl { font-size: 12px; color: #64748b; margin-top: 4px; text-transform: uppercase; letter-spacing: .05em; }
.metric-card.good .val { color: #16a34a; }
.metric-card.warn .val { color: #d97706; }
.metric-card.bad  .val { color: #dc2626; }

.section-header {
    font-size: 11px; font-weight: 600; letter-spacing: .08em;
    text-transform: uppercase; color: #94a3b8;
    margin: 24px 0 10px; padding-bottom: 6px;
    border-bottom: 1px solid #1e293b;
}

.badge {
    display: inline-block; padding: 4px 12px;
    border-radius: 999px; font-size: 12px; font-weight: 600;
}
.badge-blue   { background:#dbeafe; color:#1d4ed8; }
.badge-green  { background:#dcfce7; color:#16a34a; }
.badge-amber  { background:#fef3c7; color:#d97706; }
.badge-red    { background:#fee2e2; color:#dc2626; }
.badge-gray   { background:#f1f5f9; color:#475569; }

.status-pill {
    display: inline-flex; align-items: center; gap: 8px;
    padding: 6px 14px; border-radius: 999px;
    font-size: 13px; font-weight: 600;
}
.status-pill.ok       { background:#dcfce7; color:#166534; }
.status-pill.warning  { background:#fef3c7; color:#92400e; }
.status-pill.critical { background:#fee2e2; color:#991b1b; }
.status-pill .dot {
    width: 8px; height: 8px; border-radius: 50%;
}
.status-pill.ok .dot       { background:#16a34a; }
.status-pill.warning .dot  { background:#d97706; }
.status-pill.critical .dot { background:#dc2626; animation: pulse 1.5s infinite; }

@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.4; }
}
</style>
""",
    unsafe_allow_html=True,
)


# ── Helper: API calls ────────────────────────────────────────────────────────
@st.cache_data(ttl=60, show_spinner=False)
def _api_get(path: str, params: Optional[Dict] = None) -> Optional[Dict]:
    try:
        resp = requests.get(f"{API_BASE_URL}{path}", params=params, timeout=30)
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.ConnectionError:
        return None
    except Exception:
        return None


# ── Helper: MLflow direct access (for performance trend) ─────────────────────
@st.cache_data(ttl=120, show_spinner=False)
def _get_mlflow_runs(limit: int = 30) -> pd.DataFrame:
    """Fetch recent MLflow runs for trend analysis."""
    if mlflow is None:
        return pd.DataFrame()
    try:
        mlflow.set_tracking_uri("sqlite:///mlruns.db")
        client = mlflow.tracking.MlflowClient()
        exp = client.get_experiment_by_name("catboost_timeseries")
        if exp is None:
            return pd.DataFrame()
        runs = client.search_runs(
            experiment_ids=[exp.experiment_id],
            order_by=["start_time DESC"],
            max_results=limit,
        )
        rows = []
        for r in runs:
            row = {
                "run_id": r.info.run_id,
                "start_time": r.info.start_time,
                "run_name": r.info.run_name,
            }
            row.update(r.data.metrics)
            rows.append(row)
        df = pd.DataFrame(rows)
        if not df.empty and "start_time" in df.columns:
            df["start_time"] = pd.to_datetime(df["start_time"], unit="ms")
            df = df.sort_values("start_time")
        return df
    except Exception:
        return pd.DataFrame()


# ── Helper: Drift status ─────────────────────────────────────────────────────
def _drift_status(drift_report: Optional[Dict]) -> tuple[str, str]:
    """Return (status_class, label) based on drift severity."""
    if drift_report is None:
        return "gray", "Unknown"
    severity = drift_report.get("severity", "low").lower()
    if severity == "high":
        return "critical", "🔴 Drift Detected"
    if severity == "medium":
        return "warning", "🟡 Warning"
    return "ok", "🟢 OK"


def _render_status_pill(status: str, label: str) -> None:
    st.markdown(
        f'<span class="status-pill {status}"><span class="dot"></span>{label}</span>',
        unsafe_allow_html=True,
    )


# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 📊 Monitoring")
    st.markdown(
        "<div style='font-size:12px;color:#475569;margin-bottom:20px'>"
        "Model health & drift tracking</div>",
        unsafe_allow_html=True,
    )

    # API status
    st.markdown("<div class='section-header'>API Status</div>", unsafe_allow_html=True)
    health = _api_get("/health")
    if health:
        st.markdown(
            '<span class="badge badge-green">● Connected</span>',
            unsafe_allow_html=True,
        )
        st.caption(f"Version: {health.get('version', 'N/A')}")
    else:
        st.markdown(
            '<span class="badge badge-red">● Offline</span>',
            unsafe_allow_html=True,
        )

    # Latest metrics from /metrics endpoint
    st.markdown("<div class='section-header'>Latest Metrics</div>", unsafe_allow_html=True)
    metrics_resp = _api_get("/metrics")
    if metrics_resp and metrics_resp.get("status") == "success":
        metrics_dict = {m["name"]: m["value"] for m in metrics_resp.get("metrics", [])}
        items = [
            ("Competition Score", "holdout_competition_score", ".4f"),
            ("MAE", "holdout_mae", ".2f"),
            ("RMSE", "holdout_rmse", ".2f"),
            ("MAPE", "holdout_mape", ".2f"),
            ("R²", "holdout_r2", ".3f"),
        ]
        for lbl, key, fmt in items:
            val = metrics_dict.get(key)
            val_str = f"{val:{fmt}}" if val is not None else "–"
            st.markdown(
                f"<div style='display:flex;justify-content:space-between;"
                f"font-size:13px;padding:4px 0;border-bottom:1px solid #1e293b'>"
                f"<span style='color:#64748b'>{lbl}</span>"
                f"<span style='color:#f1f5f9;font-family:JetBrains Mono'>{val_str}</span>"
                f"</div>",
                unsafe_allow_html=True,
            )
        if metrics_resp.get("model_version"):
            st.caption(f"Run: {metrics_resp['model_version']}")
    else:
        st.caption("No metrics available")

    # Refresh
    st.markdown("<div class='section-header'>Refresh</div>", unsafe_allow_html=True)
    if st.button("🔄 Refresh now", use_container_width=True):
        st.cache_data.clear()
        st.rerun()


# ── Page Header ──────────────────────────────────────────────────────────────
st.title("📊 Monitoring Dashboard")
st.markdown(
    "Track model performance over time, detect data drift, and monitor data health."
)

# ── Fetch data ───────────────────────────────────────────────────────────────
drift_report = _api_get("/drift")
sectors_resp = _api_get("/sectors")
mlflow_df = _get_mlflow_runs(limit=30)


# ═══════════════════════════════════════════════════════════════════════════
# ROW 1: SYSTEM OVERVIEW
# ═══════════════════════════════════════════════════════════════════════════
st.markdown("<div class='section-header'>System Overview</div>", unsafe_allow_html=True)
c1, c2, c3, c4 = st.columns(4)

# API health
with c1:
    if health:
        st.markdown(
            "<div class='metric-card good'><div class='val'>●</div>"
            "<div class='lbl'>API Status</div></div>",
            unsafe_allow_html=True,
        )
        st.caption("Healthy")
    else:
        st.markdown(
            "<div class='metric-card bad'><div class='val'>●</div>"
            "<div class='lbl'>API Status</div></div>",
            unsafe_allow_html=True,
        )
        st.caption("Offline")

# Drift status
with c2:
    drift_status, drift_label = _drift_status(drift_report)
    drift_score = drift_report.get("drift_score", 0) if drift_report else 0
    cls = "bad" if drift_status == "critical" else ("warn" if drift_status == "warning" else "good")
    st.markdown(
        f"<div class='metric-card {cls}'><div class='val'>{drift_score:.1%}</div>"
        f"<div class='lbl'>Drift Score</div></div>",
        unsafe_allow_html=True,
    )
    _render_status_pill(drift_status, drift_label)

# Latest MAE
with c3:
    if metrics_resp and metrics_resp.get("status") == "success":
        metrics_dict = {m["name"]: m["value"] for m in metrics_resp.get("metrics", [])}
        mae = metrics_dict.get("holdout_mae")
        if mae is not None:
            st.markdown(
                f"<div class='metric-card'><div class='val'>{mae:,.0f}</div>"
                f"<div class='lbl'>Latest MAE</div></div>",
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                "<div class='metric-card'><div class='val'>–</div>"
                "<div class='lbl'>Latest MAE</div></div>",
                unsafe_allow_html=True,
            )
    else:
        st.markdown(
            "<div class='metric-card'><div class='val'>–</div>"
            "<div class='lbl'>Latest MAE</div></div>",
            unsafe_allow_html=True,
        )

# Latest R²
with c4:
    if metrics_resp and metrics_resp.get("status") == "success":
        r2 = metrics_dict.get("holdout_r2")
        if r2 is not None:
            cls = "good" if r2 >= 0.5 else ("warn" if r2 >= 0.2 else "bad")
            st.markdown(
                f"<div class='metric-card {cls}'><div class='val'>{r2:.3f}</div>"
                f"<div class='lbl'>Latest R²</div></div>",
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                "<div class='metric-card'><div class='val'>–</div>"
                "<div class='lbl'>Latest R²</div></div>",
                unsafe_allow_html=True,
            )
    else:
        st.markdown(
            "<div class='metric-card'><div class='val'>–</div>"
            "<div class='lbl'>Latest R²</div></div>",
            unsafe_allow_html=True,
        )


# ═══════════════════════════════════════════════════════════════════════════
# TABS
# ═══════════════════════════════════════════════════════════════════════════
tab_perf, tab_drift, tab_data = st.tabs(
    ["📈 Performance Trend", "🔬 Drift Detection", "🏘️ Data Overview"]
)


# ─────────────────────────────────────────────────────────────────────────────
# TAB 1: PERFORMANCE TREND (from MLflow runs)
# ─────────────────────────────────────────────────────────────────────────────
with tab_perf:
    st.markdown(
        "<div class='section-header'>Model Performance Over Time</div>",
        unsafe_allow_html=True,
    )

    if not mlflow_df.empty:
        # Summary cards
        pc1, pc2, pc3, pc4 = st.columns(4)
        metric_cols = [
            ("holdout_mae", pc1, "Latest MAE", ".2f"),
            ("holdout_rmse", pc2, "Latest RMSE", ".2f"),
            ("holdout_mape", pc3, "Latest MAPE", ".2f"),
            ("holdout_r2", pc4, "Latest R²", ".3f"),
        ]
        for col, card, label, fmt in metric_cols:
            with card:
                if col in mlflow_df.columns and not mlflow_df[col].dropna().empty:
                    latest = mlflow_df[col].dropna().iloc[-1]
                    prev = mlflow_df[col].dropna().iloc[-2] if len(mlflow_df[col].dropna()) > 1 else latest
                    delta = latest - prev
                    if col == "holdout_r2":
                        cls = "good" if delta >= 0 else "bad"
                        arrow = "▲" if delta >= 0 else "▼"
                    else:
                        cls = "good" if delta <= 0 else "bad"
                        arrow = "▼" if delta <= 0 else "▲"
                    st.markdown(
                        f"<div class='metric-card {cls}'>"
                        f"<div class='val'>{latest:{fmt}}</div>"
                        f"<div class='lbl'>{label} {arrow} {abs(delta):{fmt}}</div></div>",
                        unsafe_allow_html=True,
                    )
                else:
                    st.markdown(
                        f"<div class='metric-card'><div class='val'>–</div>"
                        f"<div class='lbl'>{label}</div></div>",
                        unsafe_allow_html=True,
                    )

        # Trend chart
        available_metrics = [c for c in ["holdout_mae", "holdout_rmse", "holdout_mape", "holdout_r2"] if c in mlflow_df.columns]
        selected_metrics = st.multiselect(
            "Select metrics to display",
            options=available_metrics,
            default=available_metrics[:2] if available_metrics else [],
        )

        if selected_metrics:
            fig = go.Figure()
            colors = {
                "holdout_mae": "#3b82f6",
                "holdout_rmse": "#ef4444",
                "holdout_mape": "#f59e0b",
                "holdout_r2": "#10b981",
            }
            for m in selected_metrics:
                fig.add_trace(go.Scatter(
                    x=mlflow_df["start_time"],
                    y=mlflow_df[m],
                    mode="lines+markers",
                    name=m.replace("holdout_", "").upper(),
                    line=dict(color=colors.get(m, "#64748b"), width=2),
                    marker=dict(size=6),
                ))
            fig.update_layout(
                template="plotly_white",
                height=400,
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                margin=dict(l=20, r=20, t=20, b=20),
            )
            fig.update_xaxes(title_text="Run Date")
            st.plotly_chart(fig, use_container_width=True)

        # Trend analysis
        st.markdown("##### 📋 Trend Analysis")
        if len(mlflow_df) >= 2:
            for m in ["holdout_mae", "holdout_rmse", "holdout_mape"]:
                if m in mlflow_df.columns:
                    vals = mlflow_df[m].dropna()
                    if len(vals) >= 2:
                        trend = vals.iloc[-1] - vals.iloc[0]
                        pct = (trend / vals.iloc[0] * 100) if vals.iloc[0] != 0 else 0
                        badge = "badge-red" if pct > 5 else ("badge-amber" if pct > 0 else "badge-green")
                        direction = "increasing" if trend > 0 else "decreasing"
                        st.markdown(
                            f"<span class='badge {badge}'>{m.replace('holdout_', '').upper()}</span> "
                            f"is <b>{direction}</b> by <b>{pct:+.2f}%</b> over last {len(vals)} runs",
                            unsafe_allow_html=True,
                        )
        else:
            st.info("Need at least 2 runs to analyze trend.")

        # Runs table
        st.markdown("##### 📜 Recent Runs")
        display_cols = ["start_time", "run_name"]
        for c in ["holdout_competition_score", "holdout_mae", "holdout_rmse", "holdout_r2"]:
            if c in mlflow_df.columns:
                display_cols.append(c)
        st.dataframe(
            mlflow_df[display_cols].sort_values("start_time", ascending=False).head(10),
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.warning(
            "⚠️ No MLflow runs found. "
            "Run the training pipeline to generate performance history."
        )


# ─────────────────────────────────────────────────────────────────────────────
# TAB 2: DRIFT DETECTION (from /drift endpoint)
# ─────────────────────────────────────────────────────────────────────────────
with tab_drift:
    st.markdown(
        "<div class='section-header'>Data & Concept Drift</div>",
        unsafe_allow_html=True,
    )

    if drift_report:
        # Overall status
        status, label = _drift_status(drift_report)
        st.markdown("### Overall Status")
        _render_status_pill(status, label)
        st.markdown(f"*{drift_report.get('recommendation', '')}*")

        # Summary cards
        dc1, dc2, dc3 = st.columns(3)
        with dc1:
            score = drift_report.get("drift_score", 0)
            cls = "good" if score < 0.2 else ("warn" if score < 0.5 else "bad")
            st.markdown(
                f"<div class='metric-card {cls}'><div class='val'>{score:.1%}</div>"
                f"<div class='lbl'>Drift Score</div></div>",
                unsafe_allow_html=True,
            )
        with dc2:
            detected = drift_report.get("drift_detected", False)
            st.markdown(
                f"<div class='metric-card {'bad' if detected else 'good'}'>"
                f"<div class='val'>{'YES' if detected else 'NO'}</div>"
                f"<div class='lbl'>Drift Detected</div></div>",
                unsafe_allow_html=True,
            )
        with dc3:
            severity = drift_report.get("severity", "low").upper()
            cls = "good" if severity == "LOW" else ("warn" if severity == "MEDIUM" else "bad")
            st.markdown(
                f"<div class='metric-card {cls}'><div class='val'>{severity}</div>"
                f"<div class='lbl'>Severity</div></div>",
                unsafe_allow_html=True,
            )

        # Affected features
        affected = drift_report.get("affected_features", [])
        if affected:
            st.markdown("##### ⚠️ Affected Features")
            for feat in affected:
                st.markdown(
                    f"<span class='badge badge-red'>{feat}</span>",
                    unsafe_allow_html=True,
                )
            st.caption(f"Total: {len(affected)} features with significant drift")
        else:
            st.success("✅ No features with significant drift detected")

        # Recommendation
        st.markdown("##### 💡 Recommendation")
        st.info(drift_report.get("recommendation", "Continue monitoring"))
    else:
        st.warning(
            "⚠️ Drift report unavailable. "
            "Make sure the backend API is running and `/drift` endpoint is accessible."
        )


# ─────────────────────────────────────────────────────────────────────────────
# TAB 3: DATA OVERVIEW (from /sectors endpoint)
# ─────────────────────────────────────────────────────────────────────────────
with tab_data:
    st.markdown(
        "<div class='section-header'>Data Health Overview</div>",
        unsafe_allow_html=True,
    )

    if sectors_resp:
        # Summary cards
        sc1, sc2, sc3, sc4 = st.columns(4)
        with sc1:
            st.markdown(
                f"<div class='metric-card'><div class='val'>{sectors_resp['total_sectors']}</div>"
                f"<div class='lbl'>Total Sectors</div></div>",
                unsafe_allow_html=True,
            )
        with sc2:
            st.markdown(
                f"<div class='metric-card good'><div class='val'>{sectors_resp['active_sectors_count']}</div>"
                f"<div class='lbl'>Active Sectors</div></div>",
                unsafe_allow_html=True,
            )
        with sc3:
            st.markdown(
                f"<div class='metric-card warn'><div class='val'>{sectors_resp['zero_sectors_count']}</div>"
                f"<div class='lbl'>Zero Sectors</div></div>",
                unsafe_allow_html=True,
            )
        with sc4:
            active_pct = (
                sectors_resp["active_sectors_count"] / sectors_resp["total_sectors"] * 100
                if sectors_resp["total_sectors"] > 0
                else 0
            )
            cls = "good" if active_pct >= 80 else ("warn" if active_pct >= 50 else "bad")
            st.markdown(
                f"<div class='metric-card {cls}'><div class='val'>{active_pct:.1f}%</div>"
                f"<div class='lbl'>Active Rate</div></div>",
                unsafe_allow_html=True,
            )

        # Sectors table
        st.markdown("##### 🏘️ Sectors Details")
        sectors_df = pd.DataFrame(sectors_resp.get("sectors", []))
        if not sectors_df.empty:
            # Rename columns for display
            sectors_df = sectors_df.rename(columns={
                "sector_name": "Sector",
                "is_zero_sector": "Zero Sector",
                "historical_avg": "Historical Avg",
            })
            # Format
            sectors_df["Zero Sector"] = sectors_df["Zero Sector"].apply(
                lambda x: "🔴 Yes" if x else "🟢 No"
            )
            sectors_df["Historical Avg"] = sectors_df["Historical Avg"].apply(
                lambda x: f"{x:,.0f}" if pd.notna(x) else "–"
            )
            st.dataframe(sectors_df, use_container_width=True, hide_index=True)
        else:
            st.info("No sectors data available")
    else:
        st.warning(
            "⚠️ Could not load sectors data. "
            "Make sure the backend API is running and `/sectors` endpoint is accessible."
        )


# ── Footer ───────────────────────────────────────────────────────────────────
st.divider()
st.caption(
    f"📊 Monitoring Dashboard · Last refreshed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} · "
    f"API: `{API_BASE_URL}`"
)