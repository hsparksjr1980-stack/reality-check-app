from __future__ import annotations

import streamlit as st


PROFILE_DEFINITIONS = {
    "Hands-On Operator": {
        "description": "You appear more aligned with direct, day-to-day ownership and operating involvement.",
        "best_fit": [
            "Food & beverage",
            "Retail",
            "Labor-heavy service businesses",
        ],
    },
    "Manager-Driven Owner": {
        "description": "You appear more aligned with oversight ownership, where a manager may run daily operations but you still stay involved.",
        "best_fit": [
            "Fitness concepts",
            "Multi-unit service businesses",
            "More structured franchise systems",
            "Manager-run franchise concepts",
        ],
    },
    "Systems / Process-Oriented Owner": {
        "description": "You appear more aligned with structured, repeatable models where process and execution matter more than constant people chaos.",
        "best_fit": [
            "Home services",
            "B2B services",
            "Mobile / route-based businesses",
            "Simpler operational models",
        ],
    },
    "Semi-Absentee Investor": {
        "description": "You appear more aligned with lower day-to-day involvement, but should be cautious about how much owner effort many models still require early.",
        "best_fit": [
            "Manager-run franchise concepts",
            "Partnership structures",
            "Simpler operational models",
            "Lower-touch operating models",
        ],
    },
    "Conservative / Risk-Controlled Operator": {
        "description": "You appear more aligned with protecting capital, controlling downside, and avoiding models with heavy overrun exposure.",
        "best_fit": [
            "Lower buildout service businesses",
            "Simpler operational models",
            "Lower fixed-cost concepts",
            "Service businesses",
        ],
    },
}


def clamp_score(value: int | float, low: int = 1, high: int = 5) -> int:
    try:
        value = int(round(float(value)))
    except Exception:
        value = low
    return max(low, min(high, value))


def get_input_scores() -> dict:
    """
    Uses session state values if present.
    These can later be fed directly from Reality Check and Concept Validation.
    """
    scores = {
        "time_availability": clamp_score(st.session_state.get("time_availability_score", 3)),
        "operational_willingness": clamp_score(st.session_state.get("operational_willingness_score", 3)),
        "people_management_comfort": clamp_score(st.session_state.get("people_management_comfort_score", 3)),
        "risk_tolerance": clamp_score(st.session_state.get("risk_tolerance_score", 3)),
        "capital_flexibility": clamp_score(st.session_state.get("capital_flexibility_score", 3)),
    }

    st.session_state["opportunity_fit_scores"] = scores
    return scores


def calculate_profile_match_scores(scores: dict) -> dict:
    """
    Simple explainable scoring.
    Higher points = stronger match.
    """
    t = scores["time_availability"]
    o = scores["operational_willingness"]
    p = scores["people_management_comfort"]
    r = scores["risk_tolerance"]
    c = scores["capital_flexibility"]

    structure_preference = bool(st.session_state.get("prefers_structure_process", False))

    match_scores = {
        "Hands-On Operator": 0,
        "Manager-Driven Owner": 0,
        "Systems / Process-Oriented Owner": 0,
        "Semi-Absentee Investor": 0,
        "Conservative / Risk-Controlled Operator": 0,
    }

    # Hands-On Operator
    if t >= 4:
        match_scores["Hands-On Operator"] += 2
    if o >= 4:
        match_scores["Hands-On Operator"] += 2
    if p >= 3:
        match_scores["Hands-On Operator"] += 1

    # Manager-Driven Owner
    if 2 <= t <= 4:
        match_scores["Manager-Driven Owner"] += 2
    if 2 <= o <= 3:
        match_scores["Manager-Driven Owner"] += 2
    if p >= 3:
        match_scores["Manager-Driven Owner"] += 1

    # Systems / Process-Oriented Owner
    if 2 <= o <= 4:
        match_scores["Systems / Process-Oriented Owner"] += 2
    if p <= 3:
        match_scores["Systems / Process-Oriented Owner"] += 1
    if structure_preference:
        match_scores["Systems / Process-Oriented Owner"] += 2

    # Semi-Absentee Investor
    if t <= 2:
        match_scores["Semi-Absentee Investor"] += 2
    if o <= 2:
        match_scores["Semi-Absentee Investor"] += 2
    if p <= 3:
        match_scores["Semi-Absentee Investor"] += 1

    # Conservative / Risk-Controlled Operator
    if r <= 2:
        match_scores["Conservative / Risk-Controlled Operator"] += 3
    if c <= 3:
        match_scores["Conservative / Risk-Controlled Operator"] += 2

    return match_scores


def pick_profiles(match_scores: dict) -> tuple[str, str | None]:
    ordered = sorted(match_scores.items(), key=lambda x: x[1], reverse=True)
    primary = ordered[0][0]

    secondary = None
    if len(ordered) > 1 and ordered[1][1] > 0 and ordered[1][0] != primary:
        secondary = ordered[1][0]

    return primary, secondary


def build_category_recommendations(primary: str, secondary: str | None) -> list[str]:
    categories = []

    for cat in PROFILE_DEFINITIONS[primary]["best_fit"]:
        if cat not in categories:
            categories.append(cat)

    if secondary:
        for cat in PROFILE_DEFINITIONS[secondary]["best_fit"]:
            if cat not in categories:
                categories.append(cat)

    return categories[:6]


def build_watchouts(scores: dict, primary: str, secondary: str | None) -> list[str]:
    warnings = []

    t = scores["time_availability"]
    o = scores["operational_willingness"]
    p = scores["people_management_comfort"]
    r = scores["risk_tolerance"]
    c = scores["capital_flexibility"]

    if t <= 2:
        warnings.append("High labor businesses may be difficult if your time availability is limited.")
    if o <= 2:
        warnings.append("Concepts that require heavy owner involvement early may be a poor fit if you do not want daily operational responsibility.")
    if p <= 2:
        warnings.append("People-heavy businesses may create friction if team management is not a strength or preference.")
    if c <= 2:
        warnings.append("High buildout models may create pressure if your capital flexibility is tight.")
    if r <= 2:
        warnings.append("More aggressive concepts with wide cost overruns or long ramp periods may not align with a conservative risk profile.")
    if primary == "Semi-Absentee Investor" or secondary == "Semi-Absentee Investor":
        warnings.append("Many concepts sold as semi-absentee still require heavy owner involvement early.")
    if primary == "Hands-On Operator" and c <= 2:
        warnings.append("Being willing to work hard does not eliminate capital pressure if the model is expensive to build or slow to ramp.")

    deduped = []
    seen = set()
    for item in warnings:
        if item not in seen:
            deduped.append(item)
            seen.add(item)

    return deduped[:4]


def build_alternative_paths(scores: dict, primary: str, secondary: str | None) -> list[str]:
    suggestions = []

    if scores["capital_flexibility"] <= 3:
        suggestions.append("Lower-buildout concepts")
        suggestions.append("Service businesses")
    if scores["time_availability"] <= 2:
        suggestions.append("Partnership structures")
        suggestions.append("Simpler investment paths")
    if scores["operational_willingness"] <= 2:
        suggestions.append("Manager-run models")
        suggestions.append("Independent ownership with lower daily operating intensity")
    if scores["risk_tolerance"] <= 2:
        suggestions.append("Lower fixed-cost concepts")
    if primary == "Systems / Process-Oriented Owner":
        suggestions.append("B2B or route-based businesses")
    if primary == "Hands-On Operator":
        suggestions.append("Operating businesses where direct involvement creates value")

    deduped = []
    seen = set()
    for item in suggestions:
        if item not in seen:
            deduped.append(item)
            seen.add(item)

    return deduped[:6]


def build_explanations(scores: dict, primary: str, secondary: str | None) -> list[str]:
    explanations = []

    t = scores["time_availability"]
    o = scores["operational_willingness"]
    p = scores["people_management_comfort"]
    r = scores["risk_tolerance"]
    c = scores["capital_flexibility"]

    if t <= 2 and o <= 2:
        explanations.append(
            "Based on your limited time availability and lower interest in running daily operations, lower-touch or manager-led models may be better aligned."
        )
    if t >= 4 and o >= 4:
        explanations.append(
            "Based on your time availability and willingness to be hands-on, higher-touch operating businesses may fit better than ownership models that rely mostly on passive oversight."
        )
    if p <= 2:
        explanations.append(
            "Based on your lower comfort with people management, businesses that depend on large teams or constant staffing issues may be worth pressure testing carefully."
        )
    if r <= 2 and c <= 3:
        explanations.append(
            "Based on your lower risk tolerance and tighter capital flexibility, lower-buildout and lower fixed-cost categories may be more aligned."
        )
    if st.session_state.get("prefers_structure_process", False):
        explanations.append(
            "Based on your preference for structure and process, more repeatable operating environments may fit better than concepts that depend heavily on constant people management chaos."
        )

    if not explanations:
        explanations.append(
            "Based on your current inputs, the best fit appears to be driven by your balance of time availability, operating willingness, and capital flexibility."
        )

    return explanations[:4]


def build_opportunity_fit_packet() -> dict:
    scores = get_input_scores()
    match_scores = calculate_profile_match_scores(scores)
    primary, secondary = pick_profiles(match_scores)

    packet = {
        "scores": scores,
        "match_scores": match_scores,
        "primary_profile": primary,
        "secondary_profile": secondary,
        "recommended_categories": build_category_recommendations(primary, secondary),
        "watchouts": build_watchouts(scores, primary, secondary),
        "alternative_paths": build_alternative_paths(scores, primary, secondary),
        "why_fit": build_explanations(scores, primary, secondary),
    }

    st.session_state["opportunity_fit_packet"] = packet
    st.session_state["opportunity_fit_primary_profile"] = primary
    st.session_state["opportunity_fit_secondary_profile"] = secondary

    return packet
