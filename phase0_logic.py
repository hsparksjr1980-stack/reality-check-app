from phase0_questions import CATEGORY_WEIGHTS, QUESTION_BANK, CATEGORY_META

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
        category_scores[category_key] = {
            "weighted_score": weighted_score,
            "raw_score": raw_score,
            "max_raw": max_raw,
        }
        total += weighted_score

    total = round(total)
    total = apply_penalties(total, answers)

    return max(total, 0), category_scores

def apply_penalties(score, answers):
    penalty = 0

    if answers.get("liquidity", 0) <= 1:
        penalty += 5

    if answers.get("contingency_capital", 0) == 0:
        penalty += 7
    elif answers.get("contingency_capital", 0) == 1:
        penalty += 4

    if answers.get("pg_comfort", 0) == 0:
        penalty += 5
    elif answers.get("pg_comfort", 0) == 1:
        penalty += 3

    if answers.get("ownership_style", 0) <= 1:
        penalty += 5

    if answers.get("ownership_style", 0) <= 1 and answers.get("daily_involvement", 0) <= 1:
        penalty += 4

    if answers.get("ops_knowledge", 0) == 0:
        penalty += 4

    if answers.get("time_capacity", 0) == 0:
        penalty += 8
    elif answers.get("time_capacity", 0) == 1:
        penalty += 4

    if answers.get("family_support", 0) == 0:
        penalty += 4

    weak_execution = 0
    for key in ["accounting", "inventory", "marketing", "learn_gaps"]:
        if answers.get(key, 0) <= 1:
            weak_execution += 1

    if weak_execution >= 3:
        penalty += 5

    return max(score - penalty, 0)

def get_verdict(score):
    if score >= 80:
        return "Proceed"
    elif score >= 60:
        return "Proceed with Caution"
    elif score >= 40:
        return "High Risk"
    return "Do Not Proceed"

def get_score_color(score):
    if score >= 80:
        return "#2e7d32"
    elif score >= 60:
        return "#b28704"
    elif score >= 40:
        return "#c76a00"
    return "#b00020"

def get_critical_warnings(answers):
    warnings = []

    if answers.get("liquidity", 0) == 0 and answers.get("contingency_capital", 0) == 0:
        warnings.append(
            "You currently show almost no financial cushion for early underperformance. This is one of the clearest early failure patterns."
        )

    if answers.get("ownership_style", 0) <= 1 and answers.get("daily_involvement", 0) <= 1:
        warnings.append(
            "Your answers suggest a passive ownership expectation in a setup that likely requires active operator behavior."
        )

    if answers.get("time_capacity", 0) == 0:
        warnings.append(
            "Your current time capacity appears too limited for launch and early instability."
        )

    if answers.get("pg_comfort", 0) == 0 and answers.get("loss_tolerance", 0) <= 1:
        warnings.append(
            "Your answers suggest the downside risk may be materially higher than your current comfort level."
        )

    return warnings

def generate_risk_flags(answers):
    flags = []

    if answers.get("liquidity", 0) <= 1 and answers.get("contingency_capital", 0) <= 1:
        flags.append({
            "title": "Capital Gap",
            "description": "Your liquidity and fallback capital suggest limited room for early underperformance.",
            "impact": "This often shows up as cash pressure within the first 6–12 months."
        })

    if answers.get("ownership_style", 0) <= 1 and answers.get("ops_knowledge", 0) <= 1:
        flags.append({
            "title": "Operator Misalignment",
            "description": "Your answers suggest you may be approaching this more like an investment than an operating business.",
            "impact": "That mismatch often leads to weak execution, margin pressure, and disappointment."
        })

    if answers.get("pg_comfort", 0) <= 1 and answers.get("walk_away", 0) <= 2:
        flags.append({
            "title": "Guarantee / Risk Misalignment",
            "description": "You may not yet be fully aligned with the personal downside that often comes with franchise financing.",
            "impact": "That can create hesitation before signing or regret after signing."
        })

    if answers.get("accounting", 0) <= 1 and answers.get("inventory", 0) <= 1 and answers.get("learn_gaps", 0) <= 1:
        flags.append({
            "title": "Execution Risk",
            "description": "Your profile shows weak coverage in several core operating disciplines.",
            "impact": "This increases the chance of missing problems early and reacting too slowly when margins slip."
        })

    if answers.get("family_support", 0) <= 1 and answers.get("time_capacity", 0) <= 1:
        flags.append({
            "title": "Lifestyle Pressure",
            "description": "Your support system and time capacity may not be strong enough for early business strain.",
            "impact": "That often leads to stress spillover, burnout, and rushed decision-making."
        })

    if answers.get("emotion_control", 0) <= 1 and answers.get("walk_away", 0) <= 1:
        flags.append({
            "title": "Decision Discipline Risk",
            "description": "Your answers suggest a higher chance of getting pulled forward by emotion or sunk cost.",
            "impact": "That increases the odds of moving ahead when the better decision is to stop."
        })

    if answers.get("marketing", 0) <= 1 and answers.get("social_media", 0) <= 1:
        flags.append({
            "title": "Traffic Generation Risk",
            "description": "Your ability to generate local awareness and demand may currently be underdeveloped.",
            "impact": "If corporate support is weak, this can become a major drag on top-line performance."
        })

    if not flags:
        flags.append({
            "title": "No Severe Early Trigger",
            "description": "You do not currently show a major single-point failure in Phase 0.",
            "impact": "That does not remove risk, but it suggests your biggest issues may show up in later phases like capital, site, or lease structure."
        })

    return flags[:3]

def generate_insights(answers, score):
    insights = []

    if answers.get("liquidity", 0) <= 1:
        insights.append("Your current liquidity profile suggests limited room for mistakes.")
    if answers.get("ownership_style", 0) <= 1:
        insights.append("You appear to be leaning investor, but many franchise systems require operator behavior, especially early.")
    if answers.get("pg_comfort", 0) <= 1:
        insights.append("You may not yet be fully aligned with the reality of personal guarantees and downside exposure.")
    if answers.get("learn_gaps", 0) <= 1:
        insights.append("Your willingness to close knowledge gaps may not yet match the demands of ownership.")
    if answers.get("family_support", 0) <= 1:
        insights.append("Your support system may not be strong enough for the pressure this can create.")
    if answers.get("marketing", 0) <= 1:
        insights.append("Your current profile suggests customer acquisition may be more dependent on outside support than it should be.")

    if not insights:
        if score >= 80:
            insights.append("You do not show an obvious early structural mismatch in Phase 0, but later deal and execution risks still matter.")
        else:
            insights.append("You do not show a single major mismatch, but your profile still has enough risk to justify deeper review before moving forward.")

    return insights

def get_meaning_text(score):
    if score < 40:
        return [
            "You are currently set up for a high-risk outcome.",
            "The gaps identified here typically show up as financial strain, operating stress, or bad decision-making within the first year."
        ]
    elif score < 60:
        return [
            "You may be able to move forward, but there are clear structural risks.",
            "Without changes, this setup has a meaningful chance of struggling to reach stability."
        ]
    elif score < 80:
        return [
            "Your profile is workable, but there are still real issues to tighten before committing.",
            "This is not a clean green light. It is a cautionary profile."
        ]
    else:
        return [
            "Your Phase 0 profile suggests you may be capable of moving forward.",
            "That said, later phases like deal structure, site selection, and economics can still break a good profile."
        ]

def get_top_drivers(answers, category_scores):
    drivers = []

    question_map = {}
    for category_key, questions in QUESTION_BANK.items():
        for q in questions:
            question_map[q["id"]] = {
                "label": q["label"],
                "category": category_key,
            }

    for qid, value in answers.items():
        if value <= 1 and qid in question_map:
            drivers.append({
                "type": "answer",
                "score": value,
                "label": question_map[qid]["label"],
                "category": CATEGORY_META[question_map[qid]["category"]]["title"],
            })

    sorted_categories = sorted(
        category_scores.items(),
        key=lambda x: x[1]["weighted_score"] / CATEGORY_WEIGHTS[x[0]]
    )

    category_drivers = []
    for category_key, details in sorted_categories[:2]:
        category_drivers.append({
            "type": "category",
            "label": CATEGORY_META[category_key]["title"],
            "score_text": f"{details['weighted_score']} / {CATEGORY_WEIGHTS[category_key]}",
        })

    answer_drivers = drivers[:3]

    return {
        "weak_categories": category_drivers,
        "weak_answers": answer_drivers,
    }
