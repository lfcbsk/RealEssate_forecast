import os
import pandas as pd
import requests
import streamlit as st

API_BASE_URL = os.environ.get("API_BASE_URL", "http://localhost:8000/api/v1")

st.set_page_config(page_title="Upload & Predict", page_icon="📤", layout="wide")

st.title("📤 Upload & Predict")
st.markdown(
    "Upload a CSV/Excel file with the required feature columns to get "
    "batch predictions from the production model."
)

st.markdown(
    "<div class='upload-hint'>"
    "📄 File must contain the engineered feature columns the model expects "
    "(plus optional <code>sector</code> / <code>date</code> columns for "
    "reference). Missing values are filled with 0."
    "</div>",
    unsafe_allow_html=True,
)

uploaded_file = st.file_uploader("Choose a CSV or Excel file", type=["csv", "xlsx", "xls"])

if uploaded_file is not None:
    st.markdown(f"**Selected file:** `{uploaded_file.name}`")

    # Preview
    try:
        if uploaded_file.name.endswith(".csv"):
            preview_df = pd.read_csv(uploaded_file)
        else:
            preview_df = pd.read_excel(uploaded_file)
        st.markdown("<div class='section-header'>Preview</div>", unsafe_allow_html=True)
        st.dataframe(preview_df.head(10), use_container_width=True)
        uploaded_file.seek(0)
    except Exception as e:
        st.error(f"Could not read file for preview: {e}")
        preview_df = None

    if st.button("🚀 Run Prediction", type="primary", use_container_width=True):
        with st.spinner("Sending file to the prediction service..."):
            try:
                files = {
                    "file": (
                        uploaded_file.name,
                        uploaded_file.getvalue(),
                        uploaded_file.type,
                    )
                }
                resp = requests.post(f"{API_BASE_URL}/upload", files=files, timeout=120)

                if resp.status_code == 200:
                    data = resp.json()
                    st.success(data.get("message", "Done"))

                    result_df = pd.DataFrame(data["predictions"])

                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.markdown(
                            f"<div class='metric-card'><div class='val'>{data['rows_processed']}</div>"
                            f"<div class='lbl'>Rows Processed</div></div>",
                            unsafe_allow_html=True,
                        )
                    with col2:
                        if "predicted_amount" in result_df.columns:
                            avg_pred = result_df["predicted_amount"].mean()
                            st.markdown(
                                f"<div class='metric-card good'><div class='val'>{avg_pred:,.0f}</div>"
                                f"<div class='lbl'>Avg Predicted Amount</div></div>",
                                unsafe_allow_html=True,
                            )
                    with col3:
                        st.markdown(
                            f"<div class='metric-card'><div class='val'>{data['status'].upper()}</div>"
                            f"<div class='lbl'>Status</div></div>",
                            unsafe_allow_html=True,
                        )

                    st.markdown(
                        "<div class='section-header'>Predictions</div>",
                        unsafe_allow_html=True,
                    )
                    st.dataframe(result_df, use_container_width=True)

                    csv_bytes = result_df.to_csv(index=False).encode("utf-8")
                    st.download_button(
                        "⬇️ Download predictions as CSV",
                        data=csv_bytes,
                        file_name=f"predictions_{uploaded_file.name.rsplit('.', 1)[0]}.csv",
                        mime="text/csv",
                        use_container_width=True,
                    )
                else:
                    detail = resp.json().get("detail", resp.text)
                    st.error(f"Prediction failed ({resp.status_code}): {detail}")

            except requests.exceptions.ConnectionError:
                st.error(
                    "Could not reach the prediction API. Make sure the "
                    f"backend is running at `{API_BASE_URL}`."
                )
            except Exception as e:
                st.error(f"Unexpected error: {e}")

st.divider()

with st.expander("🔧 Single prediction (advanced)"):
    st.markdown(
        "Make a one-off prediction by manually entering feature values "
        "as JSON."
    )
    default_payload = (
        '{\n'
        '  "lag_1": 500,\n'
        '  "lag_2": 480,\n'
        '  "nearby_sectors": 5,\n'
        '  "pre_owned": 100\n'
        '}'
    )
    features_json = st.text_area("Feature dictionary (JSON)", value=default_payload, height=150)

    if st.button("Predict single row"):
        try:
            import json

            features = json.loads(features_json)
            resp = requests.post(
                f"{API_BASE_URL}/predict",
                json={"features": features},
                timeout=30,
            )
            if resp.status_code == 200:
                data = resp.json()
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(
                        f"<div class='metric-card good'><div class='val'>{data['predicted_amount']:,}</div>"
                        f"<div class='lbl'>Predicted Amount</div></div>",
                        unsafe_allow_html=True,
                    )
                with col2:
                    st.markdown(
                        f"<div class='metric-card'><div class='val'>{data['predicted_value']:.4f}</div>"
                        f"<div class='lbl'>Raw (log) Prediction</div></div>",
                        unsafe_allow_html=True,
                    )
            else:
                detail = resp.json().get("detail", resp.text)
                st.error(f"Prediction failed ({resp.status_code}): {detail}")
        except json.JSONDecodeError as e:
            st.error(f"Invalid JSON: {e}")
        except requests.exceptions.ConnectionError:
            st.error(
                "Could not reach the prediction API. Make sure the "
                f"backend is running at `{API_BASE_URL}`."
            )
        except Exception as e:
            st.error(f"Unexpected error: {e}")