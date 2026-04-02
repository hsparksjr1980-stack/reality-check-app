CATEGORY_WEIGHTS = {
    "signal_quality": 25,
    "franchisor_trust": 25,
    "operator_alignment": 20,
    "economics_shift": 20,
    "decision_discipline": 10,
}

CATEGORY_META = {
    "signal_quality": {"title": "Signal Quality", "intro": "Did Discovery produce real information, or just more enthusiasm?"},
    "franchisor_trust": {"title": "Franchisor Trust", "intro": "Did corporate answers increase trust, or expose gaps, inconsistency, or avoidance?"},
    "operator_alignment": {"title": "Operator Alignment", "intro": "Did franchisee conversations and system realities confirm that this business matches the way you would actually have to operate?"},
    "economics_shift": {"title": "Economic Reality", "intro": "Did Discovery strengthen the economics, weaken them, or leave them too uncertain?"},
    "decision_discipline": {"title": "Decision Discipline", "intro": "This section checks whether you are making a clearer decision, or just getting more committed because you are further along."},
}

SCALE_LABELS = {
    0: "Not at all / Very weak",
    1: "Weak",
    2: "Mixed / Moderate",
    3: "Strong",
    4: "Very strong",
}

QUESTION_BANK = {
    "signal_quality": [
        {"id": "answers_more_clear", "label": "Did Discovery make the opportunity meaningfully clearer rather than just more emotionally engaging?", "help": "The point of Discovery is clarity, not momentum."},
        {"id": "hard_questions_answered", "label": "Were your hardest questions answered directly and specifically?", "help": "Look for real answers, not polished redirection."},
        {"id": "inconsistencies_found", "label": "How confident are you that you did not uncover material inconsistencies between the pitch and reality?", "help": "A high score means low inconsistency risk."},
    ],
    "franchisor_trust": [
        {"id": "transparency", "label": "How transparent did the franchisor appear when discussing hard topics like economics, failures, support gaps, or operator strain?", "help": "Transparency matters more than polish."},
        {"id": "support_confidence_post", "label": "How much stronger is your confidence in the support model after Discovery?", "help": "This should improve only if Discovery gave you real evidence."},
        {"id": "credibility_gap", "label": "How confident are you that the franchisor is not overselling growth while understating operator burden?", "help": "A high score means low credibility-gap risk."},
    ],
    "operator_alignment": [
        {"id": "franchisee_story_match", "label": "How consistent were franchisee stories with what corporate presented?", "help": "A meaningful mismatch is a major warning."},
        {"id": "owner_role_confirmed", "label": "How clearly did Discovery confirm the real owner role this concept requires?", "help": "This should reduce ambiguity, not increase it."},
        {"id": "still_want_model", "label": "After seeing the operating reality more clearly, how strong is your conviction that you still want this model?", "help": "You are testing fit, not excitement."},
    ],
    "economics_shift": [
        {"id": "economics_stronger", "label": "After Discovery, how much stronger is your confidence in the unit economics?", "help": "A weak answer means Discovery may have added risk instead of reducing it."},
        {"id": "startup_cost_confidence", "label": "How much more realistic do your startup cost assumptions feel after Discovery?", "help": "This includes buildout, ramp, labor, vendor, and capital assumptions."},
        {"id": "negative_surprises", "label": "How confident are you that Discovery did not reveal negative surprises that materially change the deal?", "help": "A high score means low surprise risk."},
    ],
    "decision_discipline": [
        {"id": "emotion_vs_clarity", "label": "Are you more confident because the facts improved, or because you are further along and more invested?", "help": "A high score means your conviction comes from evidence, not momentum."},
        {"id": "walk_away_post_discovery", "label": "If Discovery raised serious concerns, how willing are you to stop the process now?", "help": "Sunk cost gets stronger here."},
    ],
}
