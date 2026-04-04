from phase0_questions import QUESTION_BANK, CATEGORY_WEIGHTS, CATEGORY_META


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

    if answers.get("pg_understanding", 0) <= 1:
        penalty += 5

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

    if answers.get("runway_realism", 0) <= 1:
        penalty += 5

    if answers.get("booming_industry_bias", 0) <= 1:
        penalty += 4

    if answers.get("industry_understanding", 0) <= 1:
        penalty += 4

    if answers.get("real_estate_requirements", 0) <= 1:
        penalty += 5

    if answers.get("local_real_estate_awareness", 0) <= 1:
        penalty += 6

    if answers.get("site_timeline_realism", 0) <= 1:
        penalty += 5

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

    if answers.get("pg_understanding", 0) == 0:
        warnings.append(
            "You do not yet appear fully aligned with what a personal guarantee can mean in a bad outcome."
        )

    if answers.get("local_real_estate_awareness", 0) == 0:
        warnings.append(
            "You do not yet appear to understand the local commercial real estate reality well enough before concept selection."
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

    if answers.get("pg_comfort", 0) <= 1 or answers.get("pg_understanding", 0) <= 1:
        flags.append({
            "title": "Personal Guarantee Risk",
            "description": "You may not yet be fully aligned with the real downside created by personal guarantees.",
            "impact": "This can create hesitation before signing and regret after signing."
        })

    if answers.get("local_real_estate_awareness", 0) <= 1 or answers.get("site_timeline_realism", 0) <= 1:
        flags.append({
            "title": "Real Estate Blind Spot",
            "description": "You may be underestimating how hard site selection, lease timing, and local real estate constraints can be.",
            "impact": "This can delay opening, increase capital needs, and break early assumptions before the business even starts."
        })

    if answers.get("industry_understanding", 0) <= 1 or answers.get("real_estate_requirements", 0) <= 1:
        flags.append({
            "title": "Pre-Concept Homework Risk",
            "description": "You may be evaluating concepts before fully understanding the industry and physical site requirements.",
            "impact": "That increases the odds of falling in love with a concept that does not fit your market."
        })

    if answers.get("booming_industry_bias", 0) <= 1:
        flags.append({
            "title": "Category Momentum Bias",
            "description": "You may be assuming that a strong category or strong system sales automatically mean your location will work.",
            "impact": "That can cause buyers to skip market-specific economics and site reality."
        })

    if not flags:
        flags.append({
            "title": "No Severe Early Trigger",
            "description": "You do not currently show a major single-point failure in Phase 0.",
            "impact": "That does not remove risk, but it suggests your biggest issues may show up in later phases like concept validation, site, lease, or economics."
        })

    return flags[:3]


def generate_insights(answers, score):
    insights = []

    if answers.get("liquidity", 0) <= 1:
        insights.append("Your current liquidity profile suggests limited room for mistakes.")
    if answers.get("ownership_style", 0) <= 1:
        insights.append("You appear to be leaning investor, but many franchise systems require operator behavior, especially early.")
    if answers.get("pg_understanding", 0) <= 1:
        insights.append("You may not yet be fully aligned with the practical meaning of a personal guarantee.")
    if answers.get("runway_realism", 0) <= 1:
        insights.append("Your runway assumptions may still be too optimistic relative to how long ramp and break-even can actually take.")
    if answers.get("local_real_estate_awareness", 0) <= 1:
        insights.append("You may not yet understand the local commercial real estate market well enough before concept selection.")
    if answers.get("industry_understanding", 0) <= 1:
        insights.append("You may need a stronger understanding of the industry before treating a specific concept as a real opportunity.")

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
            "The gaps identified here typically show up as financial strain, opening delays, operating stress, or bad decision-making within the first year."
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
            "That said, later phases like concept validation, site selection, and economics can still break a good profile."
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
