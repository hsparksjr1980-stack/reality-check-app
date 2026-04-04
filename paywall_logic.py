import streamlit as st


def has_premium_access() -> bool:
    return bool(st.session_state.get("premium_access", False))



def can_access_pro() -> bool:
    return bool(st.session_state.get("move_forward", False) and has_premium_access())



def dev_unlock_pro() -> None:
    st.session_state["premium_access"] = True



def lock_decision(action: str) -> None:
    st.session_state["decision_locked"] = True
    st.session_state["final_decision_action"] = action
    st.session_state["move_forward"] = action == "Move Forward"
    st.session_state["walk_away"] = action == "Walk Away"
