import streamlit as st

ROADMAP = [
    ("Reality Check", "Tests whether you are personally, financially, and operationally suited for franchising."),
    ("Concept Validation", "Tests whether the concept itself holds up before you waste time on financing or site work."),
    ("Capital & Bank Readiness", "Tests whether the deal is financeable and whether your capital plan is realistic."),
    ("Financial Model", "Pressures the numbers: startup capital, debt, revenue assumptions, break-even, and cash risk."),
    ("Site & Lease", "Tests whether the location and lease terms create avoidable long-term risk."),
    ("Buildout", "Covers contractor selection, budget control, contingencies, and timeline risk."),
    ("Pre-Open Hiring", "Covers HR setup, hiring timing, onboarding, and labor planning."),
    ("Opening Execution", "Covers training, soft open, grand opening, and first-30-day targets."),
    ("Operating the Business", "Covers KPIs, marketing, labor, inventory, cash discipline, and ongoing review."),
    ("Turnaround", "Used when results are weak and you need to decide whether to fix, fund, or stop."),
    ("Exit", "Covers shutdown, transfer, landlord/franchisor issues, and personal risk cleanup."),
]

def _status_line(score_key, verdict_key):
    score = st.session_state.get(score_key)
    verdict = st.session_state.get(verdict_key)

    if score is None or verdict is None:
        return "Not started"

    return f"Completed — {verdict} ({score}/100)"

def render_overview():
    st.header("Overview")

    st.write(
        "This is a decision system, not a learning tool. Each section either moves you forward or stops you."
    )

    st.markdown("### Current Status")
    st.write(f"- Reality Check: {_status_line('phase_0_score', 'phase_0_verdict')}")
    st.write(f"- Concept Validation: {_status_line('phase_1_score', 'phase_1_verdict')}")
    st.write("- Financial Model: Use after Reality Check and Concept Validation are directionally acceptable.")

    st.markdown("### Recommended Next Step")

    phase_0 = st.session_state.get("phase_0_verdict")
    phase_1 = st.session_state.get("phase_1_verdict")

    if phase_0 in ["High Risk", "Do Not Proceed"]:
        st.warning(
            "Your Reality Check shows structural risk. Do not move forward until this is corrected."
        )
    elif phase_1 in ["High Concept Risk", "Do Not Proceed"]:
        st.warning(
            "Your concept does not currently hold up. Do not rely on the Financial Model to justify it."
        )
    elif phase_0 and phase_1:
        st.success(
            "Your next step is the Financial Model. This is where the deal either works or breaks."
        )
    else:
        st.info(
            "Start with Reality Check, then Concept Validation, then move into the Financial Model."
        )

    st.markdown("### Full Roadmap")

    for title, desc in ROADMAP:
        st.markdown(f"### {title}")
        st.write(desc)
        st.markdown("---")
        
