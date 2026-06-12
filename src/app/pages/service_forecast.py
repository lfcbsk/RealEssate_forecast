import os
import pandas as pd
import plotly.express as px
import requests
import streamlit as st

API_BASE_URL = os.environ.get("API_BASE_URL", "http://localhost:8000/api/v1")

st.set_page_config(page_title="Sector Forecast", page_icon="📈", layout="wide")

st.title("📈 Sector Forecast")
st.markdown(
    "Generate a recursive multi-month forecast and explore predicted "
    "transaction amounts by sector."
)


@st.cache_data(ttl=300, show_spinner=False)
def _fetch_sectors():
    resp = requests.get(f"{API_BASE_URL}/sectors", timeout=30)
    resp.raise_for_status()
    return resp.json()


@st.cache_data(ttl=120, show_spinner=False)
def _fetch_forecast(n_months, sectors):
    payload = {"n_months": n_months}
    if sectors:
        payload["sectors"] = sectors
    resp = requests.post(f"{API_BASE_URL}/forecast", json=payload, timeout=120)
    resp.raise_for_status()
    return resp.json()


# ── Controls ──────────────────────────────────────────────────────────────────
sectors_data = None
try:
    sectors_data = _fetch_sectors()
except requests.exceptions.ConnectionError:
    st.error(
        "Could not reach the forecast API. Make sure the backend is "
        f"running at `{API_BASE_URL}`."
    )
except Exception as e:
    st.warning(f"Could not load sector list: {e}")

col1, col2 = st.columns([1, 2])

with col1:
    n_months = st.slider("Number of months to forecast", min_value=1, max_value=36, value=12)

with col2:
    sector_options = []
    if sectors_data:
        sector_options = [s["sector_name"] for s in sectors_data["sectors"]]
    selected_sectors = st.multiselect(
        "Filter by sector (leave empty = all sectors)",
        options=sector_options,
    )

if sectors_data:
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(
            f"<div class='metric-card'><div class='val'>{sectors_data['total_sectors']}</div>"
            f"<div class='lbl'>Total Sectors</div></div>",
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            f"<div class='metric-card good'><div class='val'>{sectors_data['active_sectors_count']}</div>"
            f"<div class='lbl'>Active Sectors</div></div>",
            unsafe_allow_html=True,
        )
    with c3:
        st.markdown(
            f"<div class='metric-card warn'><div class='val'>{sectors_data['zero_sectors_count']}</div>"
            f"<div class='lbl'>Zero Sectors</div></div>",
            unsafe_allow_html=True,
        )

st.divider()

if st.button("📊 Generate Forecast", type="primary", use_container_width=True):
    with st.spinner("Running recursive forecast..."):
        try:
            data = _fetch_forecast(n_months, selected_sectors or None)
            df = pd.DataFrame(data["predictions"])
            df["date"] = pd.to_datetime(df["date"])

            st.success(
                f"Generated {data['total_predictions']} predictions "
                f"for {n_months} month(s)."
            )

            # ── Chart ─────────────────────────────────────────────────────
            st.markdown("<div class='section-header'>Forecast Chart</div>", unsafe_allow_html=True)

            if df["sector"].nunique() > 15:
                top_sectors = (
                    df.groupby("sector")["pred_amount"]
                    .sum()
                    .sort_values(ascending=False)
                    .head(15)
                    .index
                )
                chart_df = df[df["sector"].isin(top_sectors)]
                st.caption("Showing top 15 sectors by total predicted volume.")
            else:
                chart_df = df

            fig = px.line(
                chart_df.sort_values("date"),
                x="date",
                y="pred_amount",
                color="sector",
                markers=True,
                labels={"pred_amount": "Predicted Amount", "date": "Date", "sector": "Sector"},
            )
            fig.update_layout(
                template="plotly_white",
                legend_title_text="Sector",
                height=480,
            )
            st.plotly_chart(fig, use_container_width=True)

            # ── Aggregated view ───────────────────────────────────────────
            st.markdown(
                "<div class='section-header'>Total Predicted Volume by Month</div>",
                unsafe_allow_html=True,
            )
            monthly = df.groupby("date", as_index=False)["pred_amount"].sum()
            fig2 = px.bar(
                monthly,
                x="date",
                y="pred_amount",
                labels={"pred_amount": "Total Predicted Amount", "date": "Date"},
            )
            fig2.update_layout(template="plotly_white", height=380)
            st.plotly_chart(fig2, use_container_width=True)

            # ── Raw table ─────────────────────────────────────────────────
            st.markdown("<div class='section-header'>Forecast Data</div>", unsafe_allow_html=True)
            st.dataframe(
                df.sort_values(["sector", "date"]).reset_index(drop=True),
                use_container_width=True,
            )

            csv_bytes = df.to_csv(index=False).encode("utf-8")
            st.download_button(
                " Download forecast as CSV",
                data=csv_bytes,
                file_name=f"forecast_{n_months}m.csv",
                mime="text/csv",
                use_container_width=True,
            )

        except requests.exceptions.ConnectionError:
            st.error(
                "Could not reach the forecast API. Make sure the backend "
                f"is running at `{API_BASE_URL}`."
            )
        except requests.exceptions.HTTPError as e:
            try:
                detail = e.response.json().get("detail", str(e))
            except Exception:
                detail = str(e)
            st.error(f"Forecast failed: {detail}")
        except Exception as e:
            st.error(f"Unexpected error: {e}")
else:
    st.info("Configure the options above and click **Generate Forecast**.")