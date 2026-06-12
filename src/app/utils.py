"""Streamlit UI helpers — re-exports pipeline data_store + CSS."""

from src.pipeline.data_store import (  # noqa: F401
    RAW_FILE_SPECS,
    append_raw_to_csv,
    get_raw_csv_paths,
    get_train_dir,
    load_merged_training_data,
    load_production_model,
    predict_on_uploaded_months,
    process_raw_upload,
    read_upload_bytes,
    read_uploaded_csv,
    save_uploaded_raw_files,
)

APP_CSS = """
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
  html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
  section[data-testid="stSidebar"] {
    background: #0f172a; border-right: 1px solid #1e293b;
  }
  section[data-testid="stSidebar"] * { color: #94a3b8 !important; }
  section[data-testid="stSidebar"] h1,
  section[data-testid="stSidebar"] h2,
  section[data-testid="stSidebar"] h3 { color: #f1f5f9 !important; }
  .metric-card {
    background: #f8fafc; border: 1px solid #e2e8f0;
    border-radius: 12px; padding: 18px 20px; text-align: center;
  }
  .metric-card .val { font-size: 28px; font-weight: 700; color: #0f172a; font-family: 'JetBrains Mono'; }
  .metric-card .lbl { font-size: 12px; color: #64748b; margin-top: 4px; text-transform: uppercase; letter-spacing: .05em; }
  .metric-card.good .val { color: #16a34a; }
  .metric-card.warn .val { color: #d97706; }
  .metric-card.bad  .val { color: #dc2626; }
  .upload-hint {
    background: #eff6ff; border: 2px dashed #93c5fd;
    border-radius: 10px; padding: 14px 18px;
    font-size: 13px; color: #1d4ed8; margin-bottom: 8px;
  }
  .section-header {
    font-size: 11px; font-weight: 600; letter-spacing: .08em;
    text-transform: uppercase; color: #94a3b8;
    margin: 24px 0 10px; padding-bottom: 6px;
    border-bottom: 1px solid #1e293b;
  }
  .badge {
    display: inline-block; padding: 2px 10px;
    border-radius: 999px; font-size: 11px; font-weight: 600;
  }
  .badge-blue  { background:#dbeafe; color:#1d4ed8; }
  .badge-green { background:#dcfce7; color:#16a34a; }
  .badge-amber { background:#fef3c7; color:#d97706; }
  .badge-red   { background:#fee2e2; color:#dc2626; }
  div[data-testid="stFileUploader"] label { font-size: 13px !important; }
  .stButton > button {
    border-radius: 8px !important; font-weight: 600 !important; font-size: 14px !important;
  }
  .stButton > button[kind="primary"] {
    background: #1d4ed8 !important; border: none !important;
  }
</style>
"""
