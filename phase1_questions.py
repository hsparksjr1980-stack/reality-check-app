CATEGORY_WEIGHTS = {
    "concept_fit": 20,
    "market_fit": 20,
    "franchisor_support": 20,
    "economics": 25,
    "validation": 15,
}

CATEGORY_META = {
    "concept_fit": {
        "title": "Concept Fit",
        "intro": "Does this concept actually match your skills, market, and ownership style?"
    },
    "market_fit": {
        "title": "Market Fit",
        "intro": "Is this concept realistically suited for your local market and trade area?"
    },
    "franchisor_support": {
        "title": "Franchisor Support & System Readiness",
        "intro": "This tests whether the franchisor can actually support your market and operation."
    },
    "economics": {
        "title": "Economics Reality Check",
        "intro": "This tests whether the numbers still work after adjusting for real-world conditions."
    },
    "validation": {
        "title": "Validation Discipline",
        "intro": "This tests whether you have validated the opportunity beyond the sales process."
    },
}

SCALE_LABELS = {
    0: "Not at all / Very weak",
    1: "Weak",
    2: "Mixed / Moderate",
    3: "Strong",
    4: "Very strong",
}

QUESTION_BANK = {
    "concept_fit": [
        {
            "id": "concept_match",
            "label": "How well does this concept actually fit your strengths and working style?",
            "help": "Not just what sounds exciting — what you are truly suited to operate."
        },
        {
            "id": "customer_fit",
            "label": "How confident are you that you understand the target customer in your market?",
            "help": "Who they are, what they want, and why they would choose you."
        },
        {
            "id": "operating_model_fit",
            "label": "How well does the operating model fit the level of involvement you are realistically willing to provide?",
            "help": "Some concepts demand much more owner involvement than buyers expect."
        },
    ],
    "market_fit": [
        {
            "id": "market_demand",
            "label": "How confident are you that there is real demand for this concept in your market?",
            "help": "Use actual market logic, not just hope or enthusiasm."
        },
        {
            "id": "competition_awareness",
            "label": "How well do you understand the existing competition and substitutes in your area?",
            "help": "Direct competitors and informal substitutes both matter."
        },
        {
            "id": "site_dependency",
            "label": "How exposed does this concept seem to site quality and location risk?",
            "help": "If location has to be nearly perfect, risk is higher."
        },
    ],
    "franchisor_support": [
        {
            "id": "support_confidence",
            "label": "How confident are you that the franchisor can support you operationally after opening?",
            "help": "Training, systems, responsiveness, field support, and real execution."
        },
        {
            "id": "outer_market_readiness",
            "label": "How confident are you that the franchisor is ready to support your specific market, not just its home market?",
            "help": "Supply chain, labor assumptions, pricing, tools, and vendor support."
        },
        {
            "id": "system_dependence",
            "label": "How risky would it be if the franchisor’s tools, inventory systems, or reporting were weaker than expected?",
            "help": "High dependence on weak systems is a major risk."
        },
    ],
    "economics": [
        {
            "id": "unit_economics_confidence",
            "label": "How confident are you that the unit economics still work after adjusting for your actual market?",
            "help": "Rent, labor, freight, local pricing, marketing needs, and slower ramp."
        },
        {
            "id": "fdd_reliance",
            "label": "How much are you relying on franchisor averages or FDD performance claims without local adjustment?",
            "help": "A high score means low reliance and better local adjustment."
        },
        {
            "id": "break_even_realism",
            "label": "How realistic do you believe your break-even timeline is after stress testing it?",
            "help": "Assume slower sales ramp and higher costs than expected."
        },
        {
            "id": "margin_pressure",
            "label": "How resilient do the margins appear if labor or COGS run worse than expected?",
            "help": "Thin margins break fast."
        },
    ],
    "validation": [
        {
            "id": "operator_calls",
            "label": "How thoroughly have you spoken with current or former operators beyond the franchisor’s hand-picked references?",
            "help": "Real validation usually comes from candid operators."
        },
        {
            "id": "negative_case_testing",
            "label": "How thoroughly have you tested the downside case and reasons not to move forward?",
            "help": "Most people spend too much time proving yes and not enough proving no."
        },
        {
            "id": "walk_away_phase1",
            "label": "If validation reveals serious issues, how willing are you to walk away from this concept entirely?",
            "help": "Sunk cost bias gets stronger the further you go."
        },
    ],
}
