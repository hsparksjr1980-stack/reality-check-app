from phase1_questions import CATEGORY_WEIGHTS, QUESTION_BANK, CATEGORY_META

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

    if answers.get("outer_market_readiness", 0) <= 1:
        penalty += 7

    if answers.get("unit_economics_confidence", 0) <= 1:
        penalty += 8

    if answers.get("break_even_realism", 0) <= 1:
        penalty += 6

    if answers.get("operator_calls", 0) <= 1:
        penalty += 5

    if answers.get("negative_case_testing", 0) <= 1:
        penalty += 5

    if answers.get("support_confidence", 0) <= 1 and answers.get("system_dependence", 0) <= 1:
        penalty += 6

    return max(score - penalty, 0)

def get_verdict(score):
    if score >= 80:
        return "Validated Opportunity"
    elif score >= 60:
        return "Needs More Validation"
    elif score >= 40:
        return "High Concept Risk"
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

    if answers.get("unit_economics_confidence", 0) == 0:
        warnings.append("You do not currently appear to have confidence that the economics work in your actual market.")

    if answers.get("outer_market_readiness", 0) == 0:
        warnings.append("The franchisor may not be ready to support your market the way you need.")

    if answers.get("operator_calls", 0) == 0:
        warnings.append("You have not yet done enough independent operator validation.")

    return warnings

def generate_risk_flags(answers):
    flags = []

    if answers.get("unit_economics_confidence", 0) <= 1 and answers.get("break_even_realism", 0) <= 1:
        flags.append({
            "title": "Economics Risk",
            "description": "Your numbers may not hold up once local costs and slower ramp are factored in.",
            "impact": "This is one of the fastest ways a concept fails in a new market."
        })

    if answers.get("outer_market_readiness", 0) <= 1:
        flags.append({
            "title": "Outer-Market Support Risk",
            "description": "The franchisor may be stronger in its core market than in yours.",
            "impact": "This can show up in supply chain gaps, weak vendor coverage, bad assumptions, and poor local support."
        })

    if answers.get("operator_calls", 0) <= 1:
        flags.append({
            "title": "Validation Risk",
            "description": "You may not yet have enough candid operator feedback to trust what you are seeing.",
            "impact": "That increases the odds of buying into a concept you do not fully understand."
        })

    if answers.get("support_confidence", 0) <= 1 and answers.get("system_dependence", 0) <= 1:
        flags.append({
            "title": "System Dependence Risk",
            "description": "Your success may depend too heavily on franchisor systems that you are not confident in.",
            "impact": "When systems fail, operators end up absorbing the cost."
        })

    if answers.get("competition_awareness", 0) <= 1:
        flags.append({
            "title": "Market Blind Spot",
            "description": "Your view of the local market may still be incomplete.",
            "impact": "That can lead to overestimating demand and underestimating alternatives."
        })

    if not flags:
        flags.append({
            "title": "No Major Early Validation Trigger",
            "description": "You are not currently showing a single major concept-selection failure point.",
            "impact": "The next questions become financing, site, and lease structure."
        })

    return flags[:3]

def get_meaning_text(score):
    if score < 40:
        return [
            "This concept currently shows too much unresolved risk.",
            "You should not move forward until the economics, support model, and validation process improve materially."
        ]
    elif score < 60:
        return [
            "This opportunity may still be workable, but it has clear validation gaps.",
            "You need more evidence before this should be treated as a real go decision."
        ]
    elif score < 80:
        return [
            "This concept is plausible, but not yet fully de-risked.",
            "More local validation and economic pressure testing are still warranted."
        ]
    else:
        return [
            "This concept appears reasonably validated at this stage.",
            "That does not remove risk, but it suggests the concept itself may be viable enough to move into financing and site work."
        ]

def generate_insights(answers, score):
    insights = []

    if answers.get("outer_market_readiness", 0) <= 1:
        insights.append("Your answers suggest the franchisor may not be fully prepared to support your market.")
    if answers.get("unit_economics_confidence", 0) <= 1:
        insights.append("Your local economics may still be more assumption-driven than reality-tested.")
    if answers.get("operator_calls", 0) <= 1:
        insights.append("You likely need more candid feedback from operators who are not part of the sales process.")
    if answers.get("competition_awareness", 0) <= 1:
        insights.append("Your understanding of the local competitive landscape may still be incomplete.")
    if answers.get("negative_case_testing", 0) <= 1:
        insights.append("You may not have spent enough time trying to disprove the opportunity.")

    if not insights:
        if score >= 80:
            insights.append("You appear to have done a stronger-than-average job validating the concept before moving forward.")
        else:
            insights.append("The concept may be workable, but more proof would still help reduce avoidable risk.")

    return insights

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
