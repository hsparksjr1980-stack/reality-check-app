import streamlit as st


GUARDRAIL_LABELS = {
    "max_rent_pct": "Rent threshold",
    "max_buildout": "Buildout cap",
    "min_liquidity": "Liquidity floor",
    "min_revenue": "Revenue floor",
}



def get_required_guardrails() -> dict:
    return st.session_state.get("required_guardrails", {})



def save_required_guardrails(guardrails: dict) -> None:
    st.session_state["required_guardrails"] = guardrails



def evaluate_guardrails(actuals: dict) -> dict:
    required = get_required_guardrails()
    status = {}

    for key, threshold in required.items():
        actual = actuals.get(key)
        if actual is None or threshold in (None, ""):
            status[key] = "unknown"
            continue

        if key in {"max_rent_pct", "max_buildout"}:
            status[key] = "pass" if actual <= threshold else "fail"
        else:
            status[key] = "pass" if actual >= threshold else "fail"

    st.session_state["guardrail_status"] = status
    return status



def summarize_guardrail_status() -> dict:
    status = st.session_state.get("guardrail_status", {})
    return {
        "pass_count": sum(1 for v in status.values() if v == "pass"),
        "fail_count": sum(1 for v in status.values() if v == "fail"),
        "unknown_count": sum(1 for v in status.values() if v == "unknown"),
    }
