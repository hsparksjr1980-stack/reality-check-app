import streamlit as st

def _safe_weighted(scores, category_key, default=999):
    if not scores:
        return default
    return scores.get(category_key, {}).get("weighted_score", default)


def _pick_top_risk(
    rc_verdict,
    cv_verdict,
    pd_verdict,
    financial_verdict,
    rc_scores,
    cv_scores,
    pd_scores,
):
    if rc_verdict in ["High Risk", "Do Not Proceed"]:
        financial = _safe_weighted(rc_scores, "financial")
        operator = _safe_weighted(rc_scores, "operator")

        if financial <= operator:
            return (
                "Ownership readiness is weaker than the opportunity requires.",
                "The main problem is not the concept. It is whether the buyer has enough cushion, downside tolerance, and room to absorb a slow ramp.",
                "A different concept or cleaner math will not solve a weak ownership profile."
            )
        return (
            "The business may require stronger operator behavior than the buyer profile currently shows.",
            "A hands-on, people-heavy model becomes dangerous if the buyer wants something more passive or less operationally demanding.",
            "Execution weakness can break even a concept that looks fine on paper."
        )

    if cv_verdict in ["High Concept Risk", "Do Not Proceed"]:
        return (
            "The concept is not validated well enough to trust yet.",
            "Before money, Discovery, or deeper commitment go further, the concept itself needs stronger proof in the actual market.",
            "The current issue is not momentum. It is unresolved concept risk."
        )

    if pd_verdict in ["High Post-Discovery Risk", "Do Not Proceed"]:
        return (
            "Discovery appears to have weakened the case for the deal rather than strengthened it.",
            "What you learned after deeper engagement does not appear strong enough to justify smooth forward momentum.",
            "This is where many buyers keep going because they are committed, not because the evidence improved."
        )

    if financial_verdict in ["High Financial Risk", "Do Not Proceed"]:
        return (
            "The numbers do not appear strong enough to justify the deal.",
            "Even if the concept and Discovery process are workable, the startup estimate, cash curve, debt load, or break-even profile may still be too fragile.",
            "This is not a pitch problem. It is a math problem."
        )

    economics = _safe_weighted(cv_scores, "economics")
    signal_quality = _safe_weighted(pd_scores, "signal_quality")
    if economics <= 12:
        return (
            "The economics still need to survive more pressure than they have so far.",
            "The opportunity may still be too assumption-driven, especially around local costs, ramp timing, and margin resilience.",
            "A concept can feel convincing long before the numbers are actually dependable."
        )

    if signal_quality <= 12:
        return (
            "Discovery may have added more momentum than clarity.",
            "The process appears to have moved forward, but the signal may still be weaker than the commitment level.",
            "That creates a real risk of continuing because the process advanced, not because the deal improved."
        )

    return (
        "The next question is whether the deal holds up under conservative pressure.",
        "The profile, concept, and process may be directionally workable, but they still need disciplined financial review and clean decision-making.",
        "The opportunity is alive, but not entitled to survive."
    )


def _get_financial_verdict():
    """
    Pulls from session_state if your financial model later starts writing summary outputs.
    For now, this stays optional and won't break anything if those keys don't exist.
    """
    return st.session_state.get("financial_verdict")


def get_master_decision():
    rc_score = st.session_state.get("phase_0_score")
    rc_verdict = st.session_state.get("phase_0_verdict")
    rc_scores = st.session_state.get("phase_0_category_scores", {})

    cv_score = st.session_state.get("phase_1_score")
    cv_verdict = st.session_state.get("phase_1_verdict")
    cv_scores = st.session_state.get("phase_1_category_scores", {})

    pd_score = st.session_state.get("post_discovery_score")
    pd_verdict = st.session_state.get("post_discovery_verdict")
    pd_scores = st.session_state.get("post_discovery_category_scores", {})

    financial_verdict = _get_financial_verdict()

    has_any_results = any(
        v is not None for v in [rc_score, cv_score, pd_score, financial_verdict]
    )

    # Master verdict logic
    if (
        rc_verdict == "Do Not Proceed"
        or cv_verdict == "Do Not Proceed"
        or pd_verdict == "Do Not Proceed"
        or financial_verdict == "Do Not Proceed"
    ):
        master_verdict = "Do Not Proceed"
        short_positioning = "This should stop the deal, not just slow it down."

    elif (
        rc_verdict == "High Risk"
        or cv_verdict == "High Concept Risk"
        or pd_verdict == "High Post-Discovery Risk"
        or financial_verdict == "High Financial Risk"
    ):
        master_verdict = "Proceed Only If Fixed"
        short_positioning = "There may be a path forward, but only after core weaknesses are corrected."

    elif (
        rc_verdict == "Proceed with Caution"
        or cv_verdict == "Needs More Validation"
        or pd_verdict == "Proceed with Caution"
        or financial_verdict == "Proceed with Caution"
    ):
        master_verdict = "Proceed Carefully"
        short_positioning = "This is not a clean green light. It still needs discipline, validation, and tighter assumptions."

    elif rc_verdict or cv_verdict or pd_verdict or financial_verdict:
        master_verdict = "Proceed to Negotiation / Financing"
        short_positioning = "The deal appears strong enough to keep moving, but only if the next steps stay disciplined."

    else:
        master_verdict = "Not Started"
        short_positioning = "Complete the earlier sections before relying on the model."

    top_risk, top_risk_explainer, secondary_risk = _pick_top_risk(
        rc_verdict,
        cv_verdict,
        pd_verdict,
        financial_verdict,
        rc_scores,
        cv_scores,
        pd_scores,
    )

    next_actions = []
    do_not_do = []

    if rc_verdict in ["High Risk", "Do Not Proceed"]:
        next_actions.extend([
            "Rework the ownership profile before spending more time on concept selection, Discovery, or deal structure.",
            "Identify whether the main constraint is capital, time, downside tolerance, or operator fit.",
            "Do not use better math to justify a weak ownership profile.",
        ])
        do_not_do.extend([
            "Do not move into deeper commitment yet.",
            "Do not assume a stronger concept solves a personal readiness problem.",
        ])

    elif cv_verdict in ["High Concept Risk", "Do Not Proceed"]:
        next_actions.extend([
            "Keep validating the concept until the local economics and support model are stronger.",
            "Talk to operators outside the sales process.",
            "Stress-test the downside case, not just the upside case.",
        ])
        do_not_do.extend([
            "Do not spend more serious money or time on a concept that is still structurally weak.",
            "Do not let early excitement outrun the evidence.",
        ])

    elif pd_verdict in ["High Post-Discovery Risk", "Do Not Proceed"]:
        next_actions.extend([
            "Pause the process and isolate what Discovery actually weakened.",
            "Resolve any mismatch between franchisee reality and the corporate story.",
            "Use the Financial Model only after the post-Discovery concerns are clearer.",
        ])
        do_not_do.extend([
            "Do not keep moving just because Discovery made the process feel more real.",
            "Do not confuse deeper engagement with stronger evidence.",
        ])

    elif financial_verdict in ["High Financial Risk", "Do Not Proceed"]:
        next_actions.extend([
            "Rebuild the model using more conservative assumptions and identify what breaks first.",
            "Reduce dependency on optimistic ramp, thin margins, or weak cash cushion.",
            "Decide whether the issue is capital structure, startup cost, ramp timing, or unit economics.",
        ])
        do_not_do.extend([
            "Do not treat a fragile model as good enough just because other sections look acceptable.",
            "Do not proceed to financing on assumptions that need top-tier performance to survive.",
        ])

    else:
        next_actions.extend([
            "Move into negotiation, financing, or deeper diligence with discipline.",
            "Convert the remaining risks into explicit conditions that must be true before signing.",
            "Keep pressure-testing assumptions instead of treating momentum as confirmation.",
        ])
        do_not_do.extend([
            "Do not relax because the process got this far.",
            "Do not let cleaner outputs replace conservative judgment.",
        ])

    must_be_true = [
        "The opportunity must work under more conservative assumptions than the sales process implies.",
        "The owner profile must match the real operating burden of the concept.",
        "The concept has to hold up in the actual market, not just in the franchise pitch.",
        "Discovery must increase clarity more than commitment.",
        "The deal should still make sense after pressure-testing capital needs, delays, and execution risk.",
    ]

    return {
        "has_any_results": has_any_results,

        "reality_check_score": rc_score,
        "reality_check_verdict": rc_verdict,

        "concept_score": cv_score,
        "concept_verdict": cv_verdict,

        "post_discovery_score": pd_score,
        "post_discovery_verdict": pd_verdict,

        "financial_verdict": financial_verdict,

        "master_verdict": master_verdict,
        "short_positioning": short_positioning,

        "top_risk": top_risk,
        "top_risk_explainer": top_risk_explainer,
        "secondary_risk": secondary_risk,

        "next_actions": next_actions,
        "do_not_do": do_not_do,
        "must_be_true": must_be_true,
    }
