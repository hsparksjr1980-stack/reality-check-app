from post_discovery_questions import CATEGORY_WEIGHTS, QUESTION_BANK, CATEGORY_META

def calculate_category_score(category_key, answers):
    questions = QUESTION_BANK[category_key]
    raw_score = sum(answers.get(q["id"], 0) for q in questions)
    max_raw = len(questions) * 4
    weight = CATEGORY_WEIGHTS[category_key]
    weighted_score = (raw_score / max_raw) * weight if max_raw else 0
    return round(weighted_score, 1), raw_score, max_raw

def calculate_total_score(answers):
    category_scores = {}
    total = 0
    for category_key in QUESTION_BANK.keys():
        weighted_score, raw_score, max_raw = calculate_category_score(category_key, answers)
        category_scores[category_key] = {"weighted_score": weighted_score, "raw_score": raw_score, "max_raw": max_raw}
        total += weighted_score
    total = round(total)
    total = apply_penalties(total, answers)
    return max(total, 0), category_scores

def apply_penalties(score, answers):
    penalty = 0
    if answers.get("hard_questions_answered", 0) <= 1: penalty += 8
    if answers.get("franchisee_story_match", 0) <= 1: penalty += 8
    if answers.get("economics_stronger", 0) <= 1: penalty += 7
    if answers.get("negative_surprises", 0) <= 1: penalty += 7
    if answers.get("emotion_vs_clarity", 0) <= 1: penalty += 6
    if answers.get("walk_away_post_discovery", 0) <= 1: penalty += 5
    if answers.get("transparency", 0) <= 1 and answers.get("credibility_gap", 0) <= 1: penalty += 6
    return max(score - penalty, 0)

def get_verdict(score):
    if score >= 80: return "Proceed to Financial Review"
    elif score >= 60: return "Proceed with Caution"
    elif score >= 40: return "High Post-Discovery Risk"
    return "Do Not Proceed"

def get_score_color(score):
    if score >= 80: return "#2E7D32"
    elif score >= 60: return "#B28704"
    elif score >= 40: return "#C76A00"
    return "#B00020"

def get_critical_warnings(answers):
    warnings = []
    if answers.get("hard_questions_answered", 0) == 0:
        warnings.append("Discovery did not appear to answer your hardest questions. That is usually a stop sign, not a reason to keep hoping.")
    if answers.get("franchisee_story_match", 0) == 0:
        warnings.append("Franchisee feedback appears materially inconsistent with the corporate story.")
    if answers.get("negative_surprises", 0) == 0:
        warnings.append("Discovery appears to have revealed negative surprises that materially change the deal.")
    if answers.get("emotion_vs_clarity", 0) == 0:
        warnings.append("Your current confidence may be coming from momentum, not stronger evidence.")
    return warnings

def generate_risk_flags(answers):
    flags = []
    if answers.get("transparency", 0) <= 1 and answers.get("credibility_gap", 0) <= 1:
        flags.append({"title": "Trust Gap", "description": "Discovery did not materially improve trust in the franchisor's transparency or incentives.", "impact": "That raises the odds of learning the hard truths after you are financially committed."})
    if answers.get("franchisee_story_match", 0) <= 1:
        flags.append({"title": "Story Mismatch", "description": "Franchisee experiences may not align with the version of the business presented by corporate.", "impact": "This is one of the strongest reasons to slow down or stop."})
    if answers.get("economics_stronger", 0) <= 1 or answers.get("startup_cost_confidence", 0) <= 1:
        flags.append({"title": "Economic Uncertainty", "description": "Discovery did not strengthen confidence in the economics enough to justify easy forward momentum.", "impact": "The deal may still be more assumption-driven than reality-tested."})
    if answers.get("emotion_vs_clarity", 0) <= 1:
        flags.append({"title": "Momentum Risk", "description": "You may be more committed because you are further along, not because the facts improved.", "impact": "This is where many buyers keep moving when they should pause."})
    if answers.get("walk_away_post_discovery", 0) <= 1:
        flags.append({"title": "Sunk Cost Risk", "description": "Your willingness to walk away may be weakening as commitment rises.", "impact": "That makes it harder to stop a deal even when the signal worsens."})
    if not flags:
        flags.append({"title": "No Major Discovery Break", "description": "Discovery did not trigger a major single-point failure in the opportunity.", "impact": "The next job is to pressure-test the numbers and confirm the deal survives conservative assumptions."})
    return flags[:3]

def get_meaning_text(score):
    if score < 40:
        return ["Discovery appears to have weakened the case for the deal rather than strengthened it.", "This should be treated as a stop signal unless material facts change."]
    elif score < 60:
        return ["Discovery did not break the deal, but it did not de-risk it enough to move forward comfortably.", "You still need clearer answers before treating this as a viable opportunity."]
    elif score < 80:
        return ["Discovery produced enough signal to continue, but not enough to relax.", "The deal can move forward only with tighter assumptions and sharper scrutiny."]
    else:
        return ["Discovery appears to have added enough clarity to justify moving into deeper financial review.", "That is not a green light to commit. It is a green light to keep pressure-testing."]

def generate_insights(answers, score):
    insights = []
    if answers.get("hard_questions_answered", 0) <= 1: insights.append("The hard questions do not appear to have been resolved well enough at Discovery.")
    if answers.get("transparency", 0) <= 1: insights.append("Corporate transparency may still be weaker than you need for confidence.")
    if answers.get("franchisee_story_match", 0) <= 1: insights.append("What operators experience may differ from what the franchisor emphasizes.")
    if answers.get("economics_stronger", 0) <= 1: insights.append("Discovery did not make the economics feel materially more trustworthy.")
    if answers.get("emotion_vs_clarity", 0) <= 1: insights.append("Your confidence may be increasing faster than the evidence.")
    if not insights:
        insights.append("Discovery appears to have added real signal rather than just momentum." if score >= 80 else "Discovery did not produce a single fatal flaw, but the evidence still needs to work harder.")
    return insights

def get_top_drivers(answers, category_scores):
    question_map = {}
    for category_key, questions in QUESTION_BANK.items():
        for q in questions:
            question_map[q["id"]] = {"label": q["label"], "category": category_key}
    weak_answers = []
    for qid, value in answers.items():
        if value <= 1 and qid in question_map:
            weak_answers.append({"label": question_map[qid]["label"], "category": CATEGORY_META[question_map[qid]["category"]]["title"]})
    sorted_categories = sorted(category_scores.items(), key=lambda x: x[1]["weighted_score"] / CATEGORY_WEIGHTS[x[0]])
    weak_categories = [{"label": CATEGORY_META[k]["title"], "score_text": f"{d['weighted_score']} / {CATEGORY_WEIGHTS[k]}"} for k, d in sorted_categories[:2]]
    return {"weak_categories": weak_categories, "weak_answers": weak_answers[:3]}

def get_post_discovery_decision(score, answers):
    if score < 40:
        verdict, color = "Do Not Move Forward", "#B00020"
        summary = "Discovery appears to have exposed enough risk to stop the process, not just slow it down."
        next_step = "Do not move into serious financial commitment, negotiation, or site work unless new facts materially improve the case."
    elif score < 60:
        verdict, color = "Pause and Re-Validate", "#C76A00"
        summary = "Discovery did not break the deal cleanly, but it also did not justify smooth forward momentum."
        next_step = "Pause. Resolve the missing answers before treating this as a live deal."
    else:
        verdict = "Proceed to Financial Review"
        color = "#2E7D32" if score >= 80 else "#B28704"
        summary = "Discovery added enough signal to justify moving into deeper financial review."
        next_step = "Move into the Financial Model and test whether the deal survives conservative assumptions."
    return {
        "verdict": verdict,
        "color": color,
        "summary": summary,
        "next_step": next_step,
        "what_this_decision_really_means": [
            "This is the point where excitement should either convert into evidence or collapse under it.",
            "If Discovery improved momentum more than clarity, the process is becoming riskier, not safer.",
            "Moving forward now should be based on stronger facts, not just greater commitment."
        ],
    }
