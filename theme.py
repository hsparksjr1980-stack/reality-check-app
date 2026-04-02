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
        f'''
        <style>
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

        .stApp {{
            background-color: {BG};
            color: {TEXT};
        }}

        .block-container {{
            padding-top: 0.5rem;
            padding-bottom: 2rem;
        }}

        h1, h2, h3, h4, h5, h6 {{
            color: {PRIMARY} !important;
            letter-spacing: -0.02em;
        }}

        p, li, label {{
            color: {TEXT};
        }}

        section[data-testid="stSidebar"] {{
            background-color: {ACCENT_LIGHT};
        }}

        section[data-testid="stSidebar"] [data-testid="stRadio"] div[role="radiogroup"] label p {{
            color: {ACCENT} !important;
            font-weight: 600 !important;
        }}

        section[data-testid="stSidebar"] [data-testid="stRadio"] div[role="radiogroup"] label span {{
            color: {ACCENT} !important;
        }}

        [data-testid="stRadio"] label p {{
            color: {ACCENT} !important;
            font-weight: 500 !important;
        }}

        div.stButton > button {{
            background-color: {PRIMARY} !important;
            color: #FFFFFF !important;
            border: none !important;
            border-radius: 10px !important;
            font-weight: 600 !important;
            padding: 0.55rem 1rem !important;
        }}

        div.stButton > button:hover {{
            background-color: {PRIMARY_DARK} !important;
            color: #FFFFFF !important;
        }}

        div.stButton > button * {{
            color: #FFFFFF !important;
            fill: #FFFFFF !important;
        }}

        div.stButton > button p {{
            color: #FFFFFF !important;
        }}

        div[data-testid="stMetric"] {{
            background: {CARD};
            border: 1px solid {BORDER};
            border-radius: 14px;
            padding: 12px;
        }}

        [data-testid="stExpander"] {{
            border: 1px solid {BORDER};
            border-radius: 14px;
            background: {CARD};
        }}

        [data-testid="stExpander"] summary p {{
            color: {PRIMARY} !important;
            font-weight: 700 !important;
        }}

        hr {{
            border-top: 1px solid {BORDER};
        }}

        .rc-card {{
            background: {CARD};
            border: 1px solid {BORDER};
            border-radius: 16px;
            padding: 18px;
        }}

        .rc-card-soft {{
            background: {ACCENT_LIGHT};
            border: 1px solid {BORDER};
            border-radius: 16px;
            padding: 18px;
        }}

        .rc-kicker {{
            font-size: 12px;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            color: #5B6B7C;
            margin-bottom: 6px;
        }}

        .rc-big {{
            font-size: 32px;
            font-weight: 700;
            line-height: 1.05;
            color: {PRIMARY};
        }}

        .rc-muted {{
            color: #5B6B7C;
            font-size: 14px;
        }}

        .rc-badge {{
            display: inline-block;
            padding: 6px 10px;
            border-radius: 999px;
            font-size: 12px;
            font-weight: 700;
            border: 1px solid {BORDER};
            background: {CARD};
            margin-right: 8px;
            margin-bottom: 8px;
        }}
        </style>
        ''',
        unsafe_allow_html=True,
    )
