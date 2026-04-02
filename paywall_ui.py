import streamlit as st

def has_premium_access():
    return bool(st.session_state.get("premium_access", False))


def render_upgrade_card():
    franchise_name = st.session_state.get("franchise_name", "this opportunity")

    st.markdown(
        """
        <div class="rc-card-soft" style="margin-top:16px;">
            <div class="rc-kicker">Upgrade Required</div>
            <div style="font-size:28px; font-weight:700; color:#23467F; margin-bottom:8px;">
                Unlock Full Financial Analysis
            </div>
            <div class="rc-muted" style="margin-bottom:12px;">
                You’ve finished building the model. The full results are locked because this is the point where the app stops being a form and starts being a decision product.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write(f"To see whether **{franchise_name}** actually works, unlock:")
    st.write("- full results and recommendation")
    st.write("- break-even pressure points")
    st.write("- cash fragility and debt pressure")
    st.write("- risk interpretation, not just raw numbers")
    st.write("- what to fix before moving forward")

    col1, col2 = st.columns(2)

    with col1:
        st.button("Unlock Pro", key="unlock_pro_button", use_container_width=True)

    with col2:
        if st.button("Dev Unlock", key="dev_unlock_button", use_container_width=True):
            st.session_state["premium_access"] = True
            st.rerun()


def require_premium_or_stop():
    if not has_premium_access():
        render_upgrade_card()
        st.stop()
