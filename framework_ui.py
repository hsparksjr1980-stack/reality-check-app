import streamlit as st

def render_framework(title, look_at, common, ask, pressure):
    st.markdown(f"### {title}")

    with st.expander("What to Look At"):
        for item in look_at:
            st.write(f"- {item}")

    with st.expander("What’s Common in the Industry"):
        for item in common:
            st.write(f"- {item}")

    with st.expander("What to Ask"):
        for item in ask:
            st.write(f"- {item}")

    with st.expander("Pressure Test"):
        for item in pressure:
            st.write(f"- {item}")
