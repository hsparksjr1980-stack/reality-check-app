import streamlit as st

PRIMARY = "#23467F"
PRIMARY_DARK = "#1B3765"
ACCENT = "#3F8AD8"
ACCENT_LIGHT = "#DCEBFA"
BG = "#F5F7FA"
CARD = "#FFFFFF"
BORDER = "#D6DEE8"

TEXT = "#1F2937"


def apply_theme():
    st.markdown(
        f"""
        <style>

        /* --- Remove Streamlit chrome --- */
        [data-testid="stToolbar"] {{
            display: none !important;
        }}

        [data-testid="stDecoration"] {{
            display: none !important;
        }}

        [data-testid="stStatusWidget"] {{
            display: none !important;
        }}

        [data-testid="stAppHeader"] {{
            display: none !important;
        }}

        header {{
            display: none !important;
        }}

        footer {{
            display: none !important;
        }}

        /* --- Base app --- */
        .stApp {{
            background-color: {BG};
            color: {TEXT};
        }}

        .block-container {{
            padding-top: 0.5rem;
            padding-bottom: 2rem;
        }}

        /* --- Global text --- */
        html, body, p, li, label, div, span {{
            color: {TEXT} !important;
        }}

        h1, h2, h3, h4, h5, h6 {{
            color: {PRIMARY} !important;
        }}

        /* --- Sidebar --- */
        section[data-testid="stSidebar"] {{
            background-color: {ACCENT_LIGHT};
        }}

        section[data-testid="stSidebar"] * {{
            color: {TEXT} !important;
        }}

        /* Sidebar radio group label */
        section[data-testid="stSidebar"] [data-testid="stRadio"] label {{
            color: {PRIMARY} !important;
            font-weight: 600 !important;
        }}

        /* Sidebar radio option text */
        section[data-testid="stSidebar"] [data-testid="stRadio"] div[role="radiogroup"] label p {{
            color: {PRIMARY} !important;
            font-weight: 600 !important;
        }}

        section[data-testid="stSidebar"] [data-testid="stRadio"] div[role="radiogroup"] label span {{
            color: {PRIMARY} !important;
        }}

        /* --- Buttons --- */
        div.stButton > button {{
            background-color: {PRIMARY} !important;
            color: #FFFFFF !important;
            border: none !important;
            border-radius: 10px !important;
            font-weight: 600 !important;
            padding: 0.5rem 1rem !important;
        }}

        div.stButton > button:hover {{
            background-color: {PRIMARY_DARK} !important;
            color: #FFFFFF !important;
        }}

        /* --- Metrics --- */
        div[data-testid="stMetric"] {{
            background: {CARD};
            border: 1px solid {BORDER};
            padding: 12px;
            border-radius: 12px;
            color: {TEXT} !important;
        }}

        /* --- Inputs --- */
        input, textarea, select {{
            color: {TEXT} !important;
        }}

        /* --- Expander headers (this is your section title issue) --- */
        details summary {{
            color: {PRIMARY} !important;
        }}

        details summary p {{
            color: {PRIMARY} !important;
            font-weight: 700 !important;
        }}

        /* Streamlit expander button text */
        [data-testid="stExpander"] summary {{
            color: {PRIMARY} !important;
        }}

        [data-testid="stExpander"] summary p {{
            color: {PRIMARY} !important;
            font-weight: 700 !important;
        }}

        [data-testid="stExpander"] details summary span {{
            color: {PRIMARY} !important;
        }}

        /* --- Radio labels in main content --- */
        [data-testid="stRadio"] label p {{
            color: {TEXT} !important;
        }}

        /* --- Selectbox labels --- */
        [data-testid="stSelectbox"] label p {{
            color: {TEXT} !important;
        }}

        /* --- Divider --- */
        hr {{
            border-top: 1px solid {BORDER};
        }}

        /* --- Custom cards --- */
        .rc-card {{
            background: {CARD};
            border: 1px solid {BORDER};
            border-radius: 14px;
            padding: 18px;
        }}

        .rc-card-soft {{
            background: {ACCENT_LIGHT};
            border: 1px solid {BORDER};
            border-radius: 14px;
            padding: 18px;
        }}

        .rc-title-dark {{
            color: {PRIMARY} !important;
        }}

        .rc-title-accent {{
            color: {ACCENT} !important;
        }}

        </style>
        """,
        unsafe_allow_html=True,
    )
