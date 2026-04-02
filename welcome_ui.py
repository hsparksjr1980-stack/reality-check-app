import streamlit as st

def render_welcome():
    st.header("Welcome")
    st.write(
        "This app is built to tell someone whether a franchise opportunity is worth pursuing, validating, and financing before they commit real money and personal risk."
    )

    st.markdown("### Get Started")
    st.write(
        "For now, this is a prototype flow. The account and login experience below is a front-end shell so the product feels like a real platform. A secure account system can be added later."
    )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            '''
            <div class="rc-card">
                <div class="rc-kicker">New User</div>
                <div style="font-size:22px; font-weight:700;">Create Account</div>
                <div class="rc-muted">Start a new assessment and set up your profile.</div>
            </div>
            ''',
            unsafe_allow_html=True,
        )
        if st.button("Create Account", key="create_account_button"):
            st.session_state["account_mode"] = "create"
            st.session_state["auth_complete"] = True
            st.rerun()

    with col2:
        st.markdown(
            '''
            <div class="rc-card">
                <div class="rc-kicker">Returning User</div>
                <div style="font-size:22px; font-weight:700;">Log In</div>
                <div class="rc-muted">Resume your assessment and continue from where you left off.</div>
            </div>
            ''',
            unsafe_allow_html=True,
        )
        if st.button("Log In", key="login_button"):
            st.session_state["account_mode"] = "login"
            st.session_state["auth_complete"] = True
            st.rerun()
