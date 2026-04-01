import streamlit as st

PRIMARY = "#23467F"
PRIMARY_DARK = "#1B3765"
ACCENT = "#3F8AD8"
ACCENT_LIGHT = "#DCEBFA"
BG = "#F5F7FA"
CARD = "#FFFFFF"
BORDER = "#D6DEE8"

TEXT = "#1F2937"

SUCCESS = "#2E7D32"
WARNING = "#B28704"
RISK = "#C76A00"
DANGER = "#B00020"


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

        /* --- Base layout --- */
        .stApp {{
            background-color: {BG};
            color: {TEXT};
        }}

        .block-container {{
            padding-top: 0.5rem;
            padding-bottom: 2rem;
        }}

        /* --- Force readable text everywhere --- */
        html, body, [class*="css"] {{
            color: {TEXT} !important;
        }}

        p, span, div {{
            color: {TEXT};
        }}

        h1, h2, h3, h4, h5 {{
            color: {PRIMARY};
        }}

        /* --- Sidebar --- */
        section[data-testid="stSidebar"] {{
            background-color: {ACCENT_LIGHT};
        }}

        section[data-testid="stSidebar"] * {{
            color: {TEXT} !important;
        }}

        /* --- Buttons --- */
        div.stButton > button {{
            background-color: {PRIMARY};
            color: white;
            border: none;
            border-radius: 10px;
            font-weight: 600;
            padding: 0.5rem 1rem;
        }}

        div.stButton > button:hover {{
            background-color: {PRIMARY_DARK};
            color: white;
        }}

        /* --- Metrics / cards --- */
        div[data-testid="stMetric"] {{
            background: {CARD};
            border: 1px solid {BORDER};
            padding: 12px;
            border-radius: 12px;
            color: {TEXT};
        }}

        /* --- Inputs --- */
        input, textarea, select {{
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
            color: {PRIMARY};
        }}

        .rc-title-accent {{
            color: {ACCENT};
        }}

        </style>
        """,
        unsafe_allow_html=True,
    )
