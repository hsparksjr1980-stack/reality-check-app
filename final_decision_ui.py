import streamlit as st
from recommendation_engine import get_master_decision
from shared_ui import render_next_actions, render_do_not_do

def render_final_decision():
    decision = get_master_decision()
    franchise_name = st.session_state.get("franchise_name", "this opportunity")

    st.header("Final Decision")
    st.write(
        f"This is where the app should stop feeling like a set of tools and start feeling like a decision product for {franchise_name}."
    )

    if not decision["has_any_results"]:
        st.info(
            "Complete the earlier sections first. This page is meant to synthesize evidence, not guess without inputs."
        )
        return

    st.markdown(
        f"""
        <div class="rc-card">
            <div class="rc-kicker">Overall Recommendation</div>
            <div class="rc-big">{decision["master_verdict"]}</div>
            <div class="rc-muted">{decision["short_positioning"]}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### Decision Path")
    if decision["reality_check_verdict"]:
        st.write(f"- **Reality Check:** {decision['reality_check_verdict']}")
    if decision["concept_verdict"]:
        st.write(f"- **Concept Validation:** {decision['concept_verdict']}")
    if decision["post_discovery_verdict"]:
        st.write(f"- **Post-Discovery Review:** {decision['post_discovery_verdict']}")
    if decision["financial_verdict"]:
        st.write(f"- **Financial Model:** {decision['financial_verdict']}")

    st.markdown("### Why This Is The Current Recommendation")
    st.write(f"- {decision['top_risk']}")
    st.write(f"- {decision['top_risk_explainer']}")

    if decision["secondary_risk"]:
        st.write(f"- {decision['secondary_risk']}")

    st.markdown("### What Must Be True For This Deal To Work")
    for item in decision["must_be_true"]:
        st.write(f"- {item}")

    render_next_actions(decision["next_actions"])
    render_do_not_do(decision["do_not_do"])

    st.markdown("### What This Recommendation Means")
    if decision["master_verdict"] == "Do Not Proceed":
        st.error(
            "This means the deal should stop unless new facts materially change the case."
        )
    elif decision["master_verdict"] == "Proceed Only If Fixed":
        st.warning(
            "This means there may be a path forward, but not without correcting the weaknesses already identified."
        )
    elif decision["master_verdict"] == "Proceed Carefully":
        st.warning(
            "This means the deal is still alive, but only under tighter assumptions and stronger discipline."
        )
    elif decision["master_verdict"] == "Proceed to Negotiation / Financing":
        st.success(
            "This means the opportunity has survived enough pressure to justify the next stage, but not blind commitment."
        )
    else:
        st.info(
            "Complete the earlier sections so the app can give you a real recommendation."
        )

    st.markdown("### What This Page Should Eventually Become")
    st.write("- A downloadable investment memo")
    st.write("- A lender-ready summary")
    st.write("- A negotiation prep document")
    st.write("- A premium action plan")
