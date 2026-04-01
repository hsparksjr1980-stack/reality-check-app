
import streamlit as st

PRIMARY = "#23467F"
PRIMARY_DARK = "#1B3765"
ACCENT = "#3F8AD8"
ACCENT_LIGHT = "#DCEBFA"
BG = "#F5F7FA"
CARD = "#FFFFFF"
BORDER = "#D6DEE8"

SUCCESS = "#2E7D32"
WARNING = "#B28704"
RISK = "#C76A00"
DANGER = "#B00020"


def apply_theme():
    st.markdown(
        f"""
        <style>
        /* Hide Streamlit top chrome completely */
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
            height: 0 !important;
            max-height: 0 !important;
            min-height: 0 !important;
            visibility: hidden !important;
        }}

        header {{
            display: none !important;
            height: 0 !important;
        }}

        footer {{
            display: none !important;
        }}

        /* App background */
        .stApp {{
            background-color: {BG};
        }}

        /* Pull content up now that header is gone */
        .block-container {{
            padding-top: 0.25rem !important;
            padding-bottom: 2rem;
        }}

        section[data-testid="stSidebar"] {{
            background-color: {ACCENT_LIGHT};
        }}

        div[data-testid="stMetric"] {{
            background: {CARD};
            border: 1px solid {BORDER};
            padding: 12px;
            border-radius: 12px;
        }}

        div.stButton > button {{
            background-color: {PRIMARY};
            color: white;
            border: none;
            border-radius: 10px;
            font-weight: 600;
        }}

        div.stButton > button:hover {{
            background-color: {PRIMARY_DARK};
            color: white;
        }}

        hr {{
            border-top: 1px solid {BORDER};
        }}

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
