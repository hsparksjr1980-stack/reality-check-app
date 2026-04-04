import streamlit as st
from plans_support_content import ADD_ONS, APP_TIERS, CONSULTING_OPTIONS



def render_plans_support() -> None:
    st.header("Plans & Support")
    st.caption("Clear packaging for the app, consulting, and add-ons so users know what they get and what they should not expect.")

    st.subheader("App Tiers")
    tier_cols = st.columns(len(APP_TIERS))
    for col, tier in zip(tier_cols, APP_TIERS):
        with col:
            st.markdown(f"### {tier['name']}")
            st.markdown(f"**Price:** {tier['price']}")
            st.markdown("**Includes**")
            for item in tier["includes"]:
                st.write(f"- {item}")
            st.markdown("**Boundaries**")
            for item in tier["boundaries"]:
                st.write(f"- {item}")

    st.subheader("Consulting Options")
    for option in CONSULTING_OPTIONS:
        with st.container(border=True):
            st.markdown(f"### {option['name']}")
            st.write(f"**Price:** {option['price']}")
            st.write(f"**What you get:** {option['what_you_get']}")
            st.write(f"**Time expectation:** {option['time']}")
            st.write(f"**Boundaries:** {option['boundaries']}")

    st.subheader("Add-Ons")
    for name, price, description in ADD_ONS:
        with st.container(border=True):
            st.markdown(f"**{name}** — {price}")
            st.write(description)
