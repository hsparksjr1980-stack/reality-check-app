import streamlit as st
from recommendation_engine import get_master_decision
from shared_ui import render_next_actions, render_do_not_do


def money(x):
    return f"${x:,.0f}"


def pct(x):
    return f"{x*100:,.1f}%"


def render_final_decision():
    decision = get_master_decision()
    franchise_name = st.session_state.get("franchise_name", "this opportunity")

    st.header("Final Decision")

    if not decision["has_any_results"]:
        st.info("Complete earlier sections first.")
        return

    # Pull financial outputs
    roi = st.session_state.get("deal_model_roi", None)
    dscr = st.session_state.get("deal_model_dscr", None)
    lowest_cash = st.session_state.get("deal_model_lowest_cash", None)
    gap = st.session_state.get("su_gap", 0.0)
    payback = st.session_state.get("deal_model_payback", None)

    # Notes
    notes_df = st.session_state.get("workspace_notes")

    # -------------------------------
    # Overall Recommendation
    # -------------------------------
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

    # -------------------------------
    # Key Financial Snapshot
    # -------------------------------
    st.markdown("### Financial Snapshot")

    c1, c2, c3, c4 = st.columns(4)
    if roi is not None:
        c1.metric("ROI", pct(roi))
    if dscr is not None:
        c2.metric("DSCR", f"{dscr:.2f}x")
    if lowest_cash is not None:
        c3.metric("Lowest Cash", money(lowest_cash))
    c4.metric("Funding Gap", money(gap))

    # -------------------------------
    # Decision Path
    # -------------------------------
    st.markdown("### Decision Path")

    if decision["reality_check_verdict"]:
        st.write(f"- **Reality Check:** {decision['reality_check_verdict']}")
    if decision["concept_verdict"]:
        st.write(f"- **Concept Validation:** {decision['concept_verdict']}")
    if decision["post_discovery_verdict"]:
        st.write(f"- **Post-Discovery Review:** {decision['post_discovery_verdict']}")
    if decision["financial_verdict"]:
        st.write(f"- **Financial Model:** {decision['financial_verdict']}")

    # -------------------------------
    # Why (Enhanced with real data)
    # -------------------------------
    st.markdown("### Why This Recommendation")

    if gap > 0:
        st.write(f"- You are underfunded by {money(gap)}")

    if lowest_cash is not None and lowest_cash < 0:
        st.write("- Cash goes negative before stabilization")

    if dscr is not None and dscr < 1.25:
        st.write("- Debt service coverage is weak")

    if roi is not None and roi < 0.15:
        st.write("- Return on equity is below target")

    # fallback to recommendation engine
    st.write(f"- {decision['top_risk']}")
    st.write(f"- {decision['top_risk_explainer']}")

    if decision["secondary_risk"]:
        st.write(f"- {decision['secondary_risk']}")

    # -------------------------------
    # Notes / Open Risks
    # -------------------------------
    if notes_df is not None and not notes_df.empty:
        open_notes = notes_df[
            notes_df["Status"].astype(str).str.lower().isin(
                ["open", "todo", "follow up", "in progress"]
            )
        ]

        if not open_notes.empty:
            st.markdown("### Open Items You Still Need to Resolve")

            for _, row in open_notes.head(5).iterrows():
                st.write(f"- {row['Note / Follow-Up']}")

    # -------------------------------
    # What Must Be True
    # -------------------------------
    st.markdown("### What Must Be True For This Deal To Work")

    for item in decision["must_be_true"]:
        st.write(f"- {item}")

    # -------------------------------
    # Next Actions
    # -------------------------------
    render_next_actions(decision["next_actions"])
    render_do_not_do(decision["do_not_do"])

    # -------------------------------
    # Meaning
    # -------------------------------
    st.markdown("### What This Recommendation Means")

    verdict = decision["master_verdict"]

    if verdict == "Do Not Proceed":
        st.error("Stop unless something materially changes.")
    elif verdict == "Proceed Only If Fixed":
        st.warning("Fix key issues before moving forward.")
    elif verdict == "Proceed Carefully":
        st.warning("Proceed, but under tighter assumptions.")
    elif verdict == "Proceed to Negotiation / Financing":
        st.success("Move forward into structuring and financing.")
    else:
        st.info("Complete earlier sections.")

    # -------------------------------
    # Forward Path
    # -------------------------------
    if verdict in ["Proceed Carefully", "Proceed to Negotiation / Financing"]:
        if st.button("➡️ Proceed to Deal Workspace"):
            st.session_state["page"] = "Deal Workspace (Pro)"
            st.rerun()
