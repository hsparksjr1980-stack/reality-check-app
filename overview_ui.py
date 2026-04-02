import streamlit as st
from recommendation_engine import get_master_decision

ROADMAP = [
    ("Reality Check", "Tests whether the buyer is personally, financially, and operationally suited for franchising."),
    ("Concept Validation", "Tests whether the concept itself is worth deeper effort before the process gets more expensive."),
    ("Financial Model", "Tests whether the startup estimate, debt load, cash curve, and break-even assumptions survive pressure before Discovery becomes a bigger commitment."),
    ("Post-Discovery Review", "Tests whether Discovery added real clarity or simply increased momentum toward the deal."),
    ("Final Decision", "Combines the earlier results into one recommendation, with next actions and reasons to stop."),
]

def render_overview():
    decision = get_master_decision()
    full_name = st.session_state.get("full_name", "there")
    franchise_name = st.session_state.get("franchise_name", "this concept")

    st.header("Overview")
    st.write(
        f"{full_name}, this product is meant to tell you whether {franchise_name} is worth pursuing before the deal gets expensive."
    )

    col1, col2 = st.columns([1.3, 1.7])

    with col1:
        st.markdown("### Current Position")
        st.markdown(
            f"""
            <div class="rc-card">
                <div class="rc-kicker">Top-Level Verdict</div>
                <div class="rc-big">{decision["master_verdict"]}</div>
                <div class="rc-muted">{decision["short_positioning"]}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown("### What This Product Is For")
        st.write("- It should tell someone when they are not ready.")
        st.write("- It should tell someone when the concept is not proven.")
        st.write("- It should tell someone when the numbers are too fragile.")
        st.write("- It should tell someone when Discovery improved momentum more than clarity.")
        st.write("- It should not help someone talk themselves into a bad deal.")

    st.markdown("### Recommended Next Step")
    if decision["master_verdict"] == "Not Started":
        st.info("Start with Reality Check, then Concept Validation, then use the Financial Model before deeper commitment.")
    elif decision["master_verdict"] == "Do Not Proceed":
        st.error("Do not advance the deal. The issues found so far are serious enough to stop it.")
    elif decision["master_verdict"] == "Proceed Only If Fixed":
        st.warning("Do not move forward casually. Fix the weak points first, then pressure-test again.")
    elif decision["master_verdict"] == "Proceed Carefully":
        st.warning("You can keep moving, but only with conservative assumptions and tighter validation.")
    else:
        st.success("You are clear to keep pressure-testing. If the numbers or Discovery do not hold up, the deal dies.")

    st.markdown("### Decision Flow")
    st.write("1. **Reality Check** — should you even be doing this?")
    st.write("2. **Concept Validation** — is this concept worth deeper effort?")
    st.write("3. **Financial Model** — do the numbers justify continuing?")
    st.write("4. **Post-Discovery Review** — did Discovery validate the case or weaken it?")
    st.write("5. **Final Decision** — should you actually move forward with the deal?")

    st.markdown("### Roadmap")
    for title, desc in ROADMAP:
        st.markdown(f"#### {title}")
        st.write(desc)
        st.markdown("---")
