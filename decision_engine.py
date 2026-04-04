from __future__ import annotations

import streamlit as st


DECISION_BUCKETS = {
    "proceed": "Proceed",
    "proceed_conditions": "Proceed with Conditions",
    "do_not_proceed": "Do Not Proceed",
}


DEFAULT_WEIGHTS = {
    "readiness": 0.20,
    "concept": 0.20,
    "financial": 0.25,
    "post_discovery": 0.25,
    "pressure_test": 0.10,
}


def clamp_score(value: float, min_value: float = 0.0, max_value: float = 100.0) -> float:
    return max(min_value, min(max_value, value))


def normalize_yes_no(value) -> bool | None:
    if value is None:
        return None
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        value = value.strip().lower()
        if value in {"yes", "y", "true"}:
            return True
        if value in {"no", "n", "false"}:
            return False
    return None


def calculate_component_score(values: list[float | int | None]) -> float | None:
    clean = [float(v) for v in values if v is not None]
    if not clean:
        return None
    return round(sum(clean) / len(clean), 1)


def get_phase_scores() -> dict:
    """
    Pull scores from session_state.
    Each page can store a 0-100 score directly.
    If a page does not exist yet, it will remain None.
    """
    return {
        "readiness": st.session_state.get("readiness_score"),
        "concept": st.session_state.get("concept_score"),
        "financial": st.session_state.get("financial_score"),
        "post_discovery": st.session_state.get("post_discovery_score"),
        "pressure_test": st.session_state.get("pressure_test_score"),
    }


def calculate_weighted_score(
    phase_scores: dict,
    weights: dict | None = None,
) -> float:
    weights = weights or DEFAULT_WEIGHTS

    weighted_total = 0.0
    used_weight = 0.0

    for key, weight in weights.items():
        score = phase_scores.get(key)
        if score is None:
            continue
        weighted_total += float(score) * weight
        used_weight += weight

    if used_weight == 0:
        return 0.0

    final_score = weighted_total / used_weight
    return round(clamp_score(final_score), 1)


def evaluate_guardrails() -> dict:
    """
    Expected session_state structure:
    st.session_state["required_guardrails"] = {
        "max_rent_percent": {"target": 10, "actual": 12, "operator": "<="},
        "max_buildout": {"target": 450000, "actual": 520000, "operator": "<="},
        ...
    }
    """
    guardrails = st.session_state.get("required_guardrails", {}) or {}

    results = {}
    passed = 0
    failed = 0
    unknown = 0

    for name, payload in guardrails.items():
        target = payload.get("target")
        actual = payload.get("actual")
        operator = payload.get("operator", "<=")

        status = "unknown"
        if target is not None and actual is not None:
            if operator == "<=":
                status = "pass" if actual <= target else "fail"
            elif operator == ">=":
                status = "pass" if actual >= target else "fail"
            elif operator == "==":
                status = "pass" if actual == target else "fail"

        if status == "pass":
            passed += 1
        elif status == "fail":
            failed += 1
        else:
            unknown += 1

        results[name] = {
            "target": target,
            "actual": actual,
            "operator": operator,
            "status": status,
        }

    return {
        "details": results,
        "passed": passed,
        "failed": failed,
        "unknown": unknown,
        "total": len(results),
    }


def get_hard_stop_flags() -> dict:
    """
    These are the things that should heavily influence or automatically kill a deal.
    You can expand these later.
    """
    flags = {
        "insufficient_liquidity": normalize_yes_no(st.session_state.get("flag_insufficient_liquidity")),
        "unsupported_personal_guarantee_risk": normalize_yes_no(st.session_state.get("flag_personal_guarantee_risk")),
        "buildout_too_high": normalize_yes_no(st.session_state.get("flag_buildout_too_high")),
        "rent_too_high": normalize_yes_no(st.session_state.get("flag_rent_too_high")),
        "no_margin_for_error": normalize_yes_no(st.session_state.get("flag_no_margin_for_error")),
        "unverified_item_19_or_unit_economics": normalize_yes_no(
            st.session_state.get("flag_unverified_unit_economics")
        ),
        "major_unknowns_remaining": normalize_yes_no(st.session_state.get("flag_major_unknowns_remaining")),
    }

    active_flags = [key for key, value in flags.items() if value is True]

    return {
        "all_flags": flags,
        "active_flags": active_flags,
        "active_count": len(active_flags),
    }


def build_conditions_list(guardrail_eval: dict, hard_stop_eval: dict, phase_scores: dict) -> list[str]:
    conditions = []

    for name, payload in guardrail_eval["details"].items():
        if payload["status"] == "fail":
            conditions.append(f"Resolve failed guardrail: {name.replace('_', ' ').title()}")

    for flag in hard_stop_eval["active_flags"]:
        conditions.append(f"Address major risk: {flag.replace('_', ' ').title()}")

    for phase, score in phase_scores.items():
        if score is not None and score < 70:
            conditions.append(f"Strengthen weak area: {phase.replace('_', ' ').title()}")

    # remove duplicates while preserving order
    deduped = []
    seen = set()
    for item in conditions:
        if item not in seen:
            deduped.append(item)
            seen.add(item)

    return deduped


def classify_decision(
    weighted_score: float,
    guardrail_eval: dict,
    hard_stop_eval: dict,
) -> str:
    """
    Basic rule set:
    - 3+ hard-stop flags -> Do Not Proceed
    - 2+ failed guardrails + low score -> Do Not Proceed
    - strong score + no failed guardrails + <=1 hard-stop -> Proceed
    - everything else -> Proceed with Conditions
    """
    failed_guardrails = guardrail_eval["failed"]
    active_hard_stops = hard_stop_eval["active_count"]

    if active_hard_stops >= 3:
        return DECISION_BUCKETS["do_not_proceed"]

    if failed_guardrails >= 2 and weighted_score < 65:
        return DECISION_BUCKETS["do_not_proceed"]

    if weighted_score >= 80 and failed_guardrails == 0 and active_hard_stops <= 1:
        return DECISION_BUCKETS["proceed"]

    if weighted_score < 55:
        return DECISION_BUCKETS["do_not_proceed"]

    return DECISION_BUCKETS["proceed_conditions"]


def summarize_key_risks(guardrail_eval: dict, hard_stop_eval: dict, phase_scores: dict) -> list[str]:
    risks = []

    for flag in hard_stop_eval["active_flags"]:
        risks.append(flag.replace("_", " ").title())

    for name, payload in guardrail_eval["details"].items():
        if payload["status"] == "fail":
            risks.append(f"Failed guardrail: {name.replace('_', ' ').title()}")

    for phase, score in phase_scores.items():
        if score is not None and score < 60:
            risks.append(f"Weak score in {phase.replace('_', ' ').title()}")

    deduped = []
    seen = set()
    for item in risks:
        if item not in seen:
            deduped.append(item)
            seen.add(item)

    return deduped[:10]


def build_decision_packet() -> dict:
    phase_scores = get_phase_scores()
    weighted_score = calculate_weighted_score(phase_scores)
    guardrail_eval = evaluate_guardrails()
    hard_stop_eval = get_hard_stop_flags()
    recommendation = classify_decision(weighted_score, guardrail_eval, hard_stop_eval)
    conditions = build_conditions_list(guardrail_eval, hard_stop_eval, phase_scores)
    key_risks = summarize_key_risks(guardrail_eval, hard_stop_eval, phase_scores)

    confidence = "Low"
    if len([v for v in phase_scores.values() if v is not None]) >= 4:
        confidence = "Medium"
    if len([v for v in phase_scores.values() if v is not None]) == 5 and guardrail_eval["unknown"] == 0:
        confidence = "High"

    packet = {
        "weighted_score": weighted_score,
        "recommendation": recommendation,
        "confidence": confidence,
        "phase_scores": phase_scores,
        "guardrails": guardrail_eval,
        "hard_stops": hard_stop_eval,
        "conditions": conditions,
        "key_risks": key_risks,
    }

    st.session_state["decision_packet"] = packet
    return packet


def render_decision_summary(packet: dict | None = None) -> None:
    packet = packet or st.session_state.get("decision_packet") or build_decision_packet()

    st.subheader("Decision Summary")
    st.metric("Weighted Score", f"{packet['weighted_score']}")
    st.metric("Recommendation", packet["recommendation"])
    st.metric("Confidence", packet["confidence"])

    st.markdown("### Phase Scores")
    for phase, score in packet["phase_scores"].items():
        pretty_name = phase.replace("_", " ").title()
        st.write(f"- **{pretty_name}:** {score if score is not None else 'Not scored yet'}")

    st.markdown("### Key Risks")
    if packet["key_risks"]:
        for risk in packet["key_risks"]:
            st.write(f"- {risk}")
    else:
        st.write("- No major risks identified yet.")

    st.markdown("### Conditions / Required Follow-Up")
    if packet["conditions"]:
        for item in packet["conditions"]:
            st.write(f"- {item}")
    else:
        st.write("- No additional conditions identified.")

    st.markdown("### Guardrail Status")
    guardrails = packet["guardrails"]["details"]
    if not guardrails:
        st.write("- No guardrails entered yet.")
    else:
        for name, payload in guardrails.items():
            pretty_name = name.replace("_", " ").title()
            st.write(
                f"- **{pretty_name}:** {payload['status'].upper()} "
                f"(actual={payload['actual']}, target {payload['operator']} {payload['target']})"
            )
