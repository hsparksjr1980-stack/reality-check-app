import base64
from pathlib import Path
import streamlit as st
from recommendation_engine import get_master_decision
from theme import PRIMARY, BORDER

def _get_logo_base64():
    logo_path = Path(__file__).parent / "logo.png"
    if not logo_path.exists():
        return None
    return base64.b64encode(logo_path.read_bytes()).decode("utf-8")


def render_brand_header(title: str, subtitle: str = ""):
    logo_b64 = _get_logo_base64()
    if logo_b64:
        st.markdown(
            f'''
            <div style="display:flex; align-items:center; gap:16px; margin-bottom:14px; padding-bottom:10px; border-bottom:1px solid {BORDER};">
                <img src="data:image/png;base64,{logo_b64}" style="height:58px; display:block;" />
                <div>
                    <div style="font-size:34px; font-weight:700; color:{PRIMARY}; line-height:1.05;">{title}</div>
                    <div style="font-size:14px; color:#5B6B7C;">{subtitle}</div>
                </div>
            </div>
            ''',
            unsafe_allow_html=True,
        )
    else:
        st.title(title)
        if subtitle:
            st.caption(subtitle)


def render_profile_strip():
    decision = get_master_decision()
    full_name = st.session_state.get("full_name")
    franchise_name = st.session_state.get("franchise_name")
    units = st.session_state.get("units_considered")
    ownership_style = st.session_state.get("ownership_style")

    if not any([decision["has_any_results"], full_name, franchise_name]):
        return

    st.markdown("### Your Profile")
    chips = []
    if full_name:
        chips.append(f"<span class='rc-badge'>{full_name}</span>")
    if franchise_name:
        chips.append(f"<span class='rc-badge'>{franchise_name}</span>")
    if units:
        chips.append(f"<span class='rc-badge'>{units} unit(s)</span>")
    if ownership_style:
        chips.append(f"<span class='rc-badge'>{ownership_style}</span>")

    if chips:
        st.markdown("".join(chips), unsafe_allow_html=True)

    cols = st.columns([1.2, 1.2, 1.2, 1.6])

    with cols[0]:
        if decision["reality_check_score"] is not None:
            st.markdown(
                f'''
                <div class="rc-card">
                    <div class="rc-kicker">Reality Check</div>
                    <div style="font-size:22px; font-weight:700; color:{PRIMARY};">{decision["reality_check_verdict"]}</div>
                    <div class="rc-muted">Score: {decision["reality_check_score"]}/100</div>
                </div>
                ''',
                unsafe_allow_html=True,
            )

    with cols[1]:
        if decision["concept_score"] is not None:
            st.markdown(
                f'''
                <div class="rc-card">
                    <div class="rc-kicker">Concept Validation</div>
                    <div style="font-size:22px; font-weight:700; color:{PRIMARY};">{decision["concept_verdict"]}</div>
                    <div class="rc-muted">Score: {decision["concept_score"]}/100</div>
                </div>
                ''',
                unsafe_allow_html=True,
            )

    with cols[2]:
        st.markdown(
            f'''
            <div class="rc-card">
                <div class="rc-kicker">Decision Status</div>
                <div style="font-size:22px; font-weight:700; color:{PRIMARY};">{decision["master_verdict"]}</div>
                <div class="rc-muted">{decision["short_positioning"]}</div>
            </div>
            ''',
            unsafe_allow_html=True,
        )

    with cols[3]:
        if decision["top_risk"]:
            st.markdown(
                f'''
                <div class="rc-card-soft">
                    <div class="rc-kicker">Top Risk</div>
                    <div style="font-size:18px; font-weight:700; color:{PRIMARY};">{decision["top_risk"]}</div>
                    <div class="rc-muted">{decision["top_risk_explainer"]}</div>
                </div>
                ''',
                unsafe_allow_html=True,
            )


def render_carry_forward_warning():
    decision = get_master_decision()
    messages = []

    if decision["reality_check_verdict"] in ["High Risk", "Do Not Proceed"]:
        messages.append(
            "Your earlier Reality Check showed structural ownership risk. A better concept does not fix weak capital, limited time, or operator mismatch."
        )

    if decision["concept_verdict"] in ["High Concept Risk", "Do Not Proceed"]:
        messages.append(
            "Your earlier Concept Validation showed concept risk. Strong personal readiness does not fix a weak concept."
        )

    if decision["top_risk"]:
        messages.append(f"Current top risk: {decision['top_risk']}")

    if messages:
        st.markdown(
            f'''
            <div class="rc-card-soft" style="margin-bottom:16px;">
                <div class="rc-kicker">Carry-Forward Reality</div>
                {"".join([f"<div style='margin-bottom:6px; color:#1F2937;'>• {m}</div>" for m in messages])}
            </div>
            ''',
            unsafe_allow_html=True,
        )


def render_section_intro(title: str, body: str):
    st.header(title)
    st.write(body)


def render_next_actions(actions):
    st.markdown("### What To Do Next")
    for action in actions:
        st.write(f"- {action}")


def render_do_not_do(do_not_do):
    st.markdown("### What Not To Do")
    for item in do_not_do:
        st.write(f"- {item}")
