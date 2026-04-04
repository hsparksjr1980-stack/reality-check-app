
import streamlit as st


def _inject_styles() -> None:
    st.markdown(
        """
        <style>
        .pf-hero {
            border: 1px solid rgba(120,120,120,.25);
            border-radius: 20px;
            padding: 1.3rem 1.3rem 1rem 1.3rem;
            margin-bottom: 1rem;
            background: rgba(255,255,255,.02);
        }
        .pf-kicker {
            font-size: 0.82rem;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            opacity: 0.72;
            margin-bottom: 0.4rem;
        }
        .pf-title {
            font-size: 1.8rem;
            font-weight: 700;
            line-height: 1.15;
            margin-bottom: 0.45rem;
        }
        .pf-subtitle {
            font-size: 1rem;
            opacity: 0.92;
        }
        .pf-card {
            border: 1px solid rgba(120,120,120,.22);
            border-radius: 18px;
            padding: 1rem;
            background: rgba(255,255,255,.02);
            margin-bottom: 1rem;
        }
        .pf-card-title {
            font-size: 1.08rem;
            font-weight: 700;
            margin-bottom: 0.25rem;
        }
        .pf-muted {
            opacity: 0.84;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_profile_setup() -> None:
    _inject_styles()

    st.title("Profile Setup")

    st.markdown(
        """
        <div class="pf-hero">
            <div class="pf-kicker">Getting Started</div>
            <div class="pf-title">Set up your profile before starting the evaluation.</div>
            <div class="pf-subtitle">
                This creates the basic context for the assessment so the app can guide the decision flow more cleanly.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="pf-card">
            <div class="pf-card-title">Basic Information</div>
            <div class="pf-muted">
                Keep this simple for now. You can expand it later.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)

    with col1:
        st.text_input(
            "Full Name",
            value=st.session_state.get("full_name", ""),
            key="full_name",
        )
        st.text_input(
            "Email",
            value=st.session_state.get("email", ""),
            key="email",
        )
        st.text_input(
            "City / State",
            value=st.session_state.get("city_state", ""),
            key="city_state",
        )

    with col2:
        st.text_input(
            "Franchise or Concept Name",
            value=st.session_state.get("franchise_name", ""),
            key="franchise_name",
        )
        st.selectbox(
            "Units Considered",
            ["1", "2-3", "4+"],
            index=["1", "2-3", "4+"].index(st.session_state.get("units_considered", "1"))
            if st.session_state.get("units_considered", "1") in ["1", "2-3", "4+"]
            else 0,
            key="units_considered",
        )
        st.selectbox(
            "Ownership Style",
            ["Owner-Operator", "Manager-Led", "Investor / Semi-Absentee"],
            index=["Owner-Operator", "Manager-Led", "Investor / Semi-Absentee"].index(
                st.session_state.get("ownership_style", "Owner-Operator")
            )
            if st.session_state.get("ownership_style", "Owner-Operator") in [
                "Owner-Operator",
                "Manager-Led",
                "Investor / Semi-Absentee",
            ]
            else 0,
            key="ownership_style",
        )

    st.checkbox(
        "I have already signed something or materially committed in the process",
        value=bool(st.session_state.get("signed_anything", False)),
        key="signed_anything",
    )

    if st.button("Continue", key="profile_setup_continue", use_container_width=True):
        st.session_state["profile_complete"] = True
        st.session_state["current_page"] = "Overview"
        st.rerun()
