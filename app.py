import streamlit as st
from pathlib import Path
from overview_ui import render_overview
from shared_ui import render_brand_header, render_reality_profile
from phase0_ui import render_phase_0
from phase1_ui import render_phase_1
from theme import apply_theme

st.set_page_config(page_title="Reality Check", layout="wide")

apply_theme()

render_brand_header("Reality Check", "A blunt roadmap for deciding whether franchising makes sense before you commit real money and personal risk.")

st.sidebar.title("Reality Check Roadmap")
if st.sidebar.button("Reset Assessment"):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

page = st.sidebar.radio(
    "Go to section:",
    [
        "Overview",
        "Reality Check",
        "Concept Validation",
        "Financial Model",
    ]
)

render_reality_profile()
st.markdown("---")

if page == "Overview":
    render_overview()
elif page == "Reality Check":
    render_phase_0()
elif page == "Concept Validation":
    render_phase_1()
elif page == "Financial Model":
    model_path = Path(__file__).parent / "financial_model_ui.py"
    if not model_path.exists():
        st.error("financial_model_ui.py was not found in this folder.")
    else:
        code = model_path.read_text(encoding="utf-8")
        exec_globals = {"__name__": "__main__"}
        exec(code, exec_globals)
