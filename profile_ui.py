import streamlit as st

def render_profile_setup():
    st.header("Set Up Your Assessment")
    st.write(
        "Before the app gives you a serious recommendation, it needs a basic profile for who you are, what concept you are considering, and how far along you are."
    )

    with st.form("profile_setup_form"):
        col1, col2 = st.columns(2)

        with col1:
            full_name = st.text_input("Full name", value=st.session_state.get("full_name", ""))
            email = st.text_input("Email", value=st.session_state.get("email", ""))
            city_state = st.text_input("City / State", value=st.session_state.get("city_state", ""))

        with col2:
            franchise_name = st.text_input("Franchise / concept name", value=st.session_state.get("franchise_name", ""))
            units_considered = st.number_input("How many units are you considering?", min_value=1, value=int(st.session_state.get("units_considered", 1)), step=1)
            ownership_style = st.selectbox(
                "How are you approaching this?",
                ["Owner-operator", "Investor", "Unsure"],
                index=["Owner-operator", "Investor", "Unsure"].index(st.session_state.get("ownership_style", "Owner-operator"))
            )

        signed_anything = st.selectbox(
            "Have you already signed anything or paid anything?",
            ["No", "Yes - exploratory", "Yes - financially committed"],
            index=["No", "Yes - exploratory", "Yes - financially committed"].index(st.session_state.get("signed_anything", "No"))
        )

        submitted = st.form_submit_button("Save and Continue", use_container_width=True)

        if submitted:
            st.session_state["full_name"] = full_name
            st.session_state["email"] = email
            st.session_state["city_state"] = city_state
            st.session_state["franchise_name"] = franchise_name
            st.session_state["units_considered"] = units_considered
            st.session_state["ownership_style"] = ownership_style
            st.session_state["signed_anything"] = signed_anything
            st.session_state["profile_complete"] = True
            st.session_state["current_page"] = "Overview"
            st.rerun()
