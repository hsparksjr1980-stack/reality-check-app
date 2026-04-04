import streamlit as st
from decision_engine import build_decision_packet, render_decision_summary


def render_final_decision():
    st.title("Final Decision")

    if st.button("Load Sample Decision Data"):
        st.session_state["readiness_score"] = 78
        st.session_state["concept_score"] = 74
        st.session_state["financial_score"] = 62
        st.session_state["post_discovery_score"] = 59
        st.session_state["pressure_test_score"] = 57

        st.session_state["flag_insufficient_liquidity"] = False
        st.session_state["flag_personal_guarantee_risk"] = True
        st.session_state["flag_buildout_too_high"] = True
        st.session_state["flag_rent_too_high"] = False
        st.session_state["flag_no_margin_for_error"] = True
        st.session_state["flag_unverified_unit_economics"] = True
        st.session_state["flag_major_unknowns_remaining"] = True

        st.session_state["required_guardrails"] = {
            "max_rent_percent": {"target": 10, "actual": 11.5, "operator": "<="},
            "max_buildout": {"target": 450000, "actual": 510000, "operator": "<="},
            "min_liquidity_remaining": {"target": 100000, "actual": 90000, "operator": ">="},
        }

    packet = build_decision_packet()
    decision = packet.get("recommendation", "Not available yet")

    st.markdown(f"## {decision}")

    render_decision_summary(packet)
