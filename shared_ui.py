import streamlit as st
from pathlib import Path
import base64

PRIMARY = "#23467F"
ACCENT = "#3F8AD8"
BORDER = "#D6DEE8"
CARD = "#FFFFFF"
SOFT = "#DCEBFA"


# --- LOGO HANDLING ---
def _get_logo_base64():
    logo_path = Path(__file__).parent / "logo.png"
    if not logo_path.exists():
        return None
    return base64.b64encode(logo_path.read_bytes()).decode("utf-8")


# --- HEADER ---
def render_brand_header(title: str, subtitle: str = ""):
    logo_b64 = _get_logo_base64()

    if logo_b64:
        st.markdown(
            f"""
            <div style="
                display:flex;
                align-items:center;
                gap:18px;
                margin:0 0 8px 0;
                padding:0 0 10px 0;
                border-bottom:1px solid #D6DEE8;
            ">
                <img src="data:image/png;base64,{logo_b64}" style="height:72px; display:block;" />
                <div style="line-height:1.1;">
                    <div style="font-size:32px; font-weight:700; color:#23467F; margin:0;">
                        {title}
                    </div>
                    <div style="font-size:14px; color:#5B6B7C; margin-top:6px;">
                        {subtitle}
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.title(title)
        if subtitle:
            st.caption(subtitle)


# --- PROFILE STATE ---
def get_reality_profile():
    return {
        "phase_0_score": st.session_state.get("phase_0_score"),
        "phase_0_verdict": st.session_state.get("phase_0_verdict"),
        "phase_0_category_scores": st.session_state.get("phase_0_category_scores"),
        "phase_1_score": st.session_state.get("phase_1_score"),
        "phase_1_verdict": st.session_state.get("phase_1_verdict"),
        "phase_1_category_scores": st.session_state.get("phase_1_category_scores"),
    }


# --- PROFILE UI ---
def render_reality_profile():
    profile = get_reality_profile()

    if profile["phase_0_score"] is None and profile["phase_1_score"] is None:
        return

    st.markdown("### Your Profile")

    col1, col2 = st.columns(2)

    with col1:
        if profile["phase_0_score"] is not None:
            st.markdown(
                f"""
                <div style="background:{CARD}; border:1px solid {BORDER}; padding:16px; border-radius:12px;">
                    <div style="font-size:12px; color:#6B7280;">Reality Check</div>
                    <div style="font-size:22px; font-weight:700; color:{PRIMARY};">
                        {profile['phase_0_verdict']}
                    </div>
                    <div style="font-size:15px;">Score: {profile['phase_0_score']} / 100</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    with col2:
        if profile["phase_1_score"] is not None:
            st.markdown(
                f"""
                <div style="background:{CARD}; border:1px solid {BORDER}; padding:16px; border-radius:12px;">
                    <div style="font-size:12px; color:#6B7280;">Concept Validation</div>
                    <div style="font-size:22px; font-weight:700; color:{PRIMARY};">
                        {profile['phase_1_verdict']}
                    </div>
                    <div style="font-size:15px;">Score: {profile['phase_1_score']} / 100</div>
                </div>
                """,
                unsafe_allow_html=True,
            )


# --- CARRY FORWARD WARNINGS ---
def render_carry_forward_warning():
    phase_0_verdict = st.session_state.get("phase_0_verdict")
    phase_1_verdict = st.session_state.get("phase_1_verdict")
    phase_0_scores = st.session_state.get("phase_0_category_scores", {})
    phase_1_scores = st.session_state.get("phase_1_category_scores", {})

    messages = []

    if phase_0_verdict in ["High Risk", "Do Not Proceed"]:
        messages.append(
            "Your Reality Check shows structural ownership risk. A better concept does not fix weak capital, limited time, or operator mismatch."
        )

    if phase_1_verdict in ["High Concept Risk", "Do Not Proceed"]:
        messages.append(
            "Your concept does not currently hold up. Strong personal readiness does not fix a weak concept."
        )

    if phase_0_scores:
        financial = phase_0_scores.get("financial", {}).get("weighted_score", 999)
        if financial <= 15:
            messages.append(
                "Your financial readiness is weak. Treat any projections conservatively."
            )

        operator = phase_0_scores.get("operator", {}).get("weighted_score", 999)
        if operator <= 10:
            messages.append(
                "Your operator fit is weak. Any operator-heavy model increases execution risk."
            )

    if phase_1_scores:
        economics = phase_1_scores.get("economics", {}).get("weighted_score", 999)
        if economics <= 12:
            messages.append(
                "Your concept economics are not fully validated. Do not treat projected performance as proven."
            )

    if messages:
        st.markdown(
            f"""
            <div style="background:{SOFT}; border:1px solid {BORDER}; padding:16px; border-radius:12px;">
                <div style="font-weight:700; color:{PRIMARY}; margin-bottom:8px;">Carry-Forward Reality</div>
                {"".join([f"<div style='margin-bottom:6px;'>• {m}</div>" for m in messages])}
            </div>
            """,
            unsafe_allow_html=True,
        )
