CATEGORY_WEIGHTS = {
    "concept_fit": 15,
    "market_fit": 20,
    "franchisor_support": 25,
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
        {
            "id": "new_market_ramp",
            "label": "How realistic are your expectations for how long it may take to build awareness and ramp in a new market?",
            "help": "A new market usually takes longer than an established brand market."
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
        {
            "id": "pricing_transferability",
            "label": "How confident are you that pricing, labor assumptions, and COGS assumptions transfer cleanly to your market?",
            "help": "What works in one market often does not translate cleanly to another."
        },
        {
            "id": "supply_chain_local_fit",
            "label": "How confident are you that supply chain economics will work in your market after freight, distance, and local vendor reality?",
            "help": "Approved sourcing is not the same as workable landed cost."
        },
        {
            "id": "proprietary_shipping_risk",
            "label": "How well have you accounted for proprietary item freight or shipping costs that may hit your market differently?",
            "help": "Items shipped from the franchisor’s home market can create hidden cost pressure."
        },
        {
            "id": "pos_flexibility",
            "label": "How confident are you that the POS and operating systems are flexible enough for local promotions, meal deals, and real-world operation?",
            "help": "A rigid or outdated POS can limit traffic-driving tactics and create workarounds."
        },
        {
            "id": "reporting_quality",
            "label": "How confident are you that reporting, recipes, and cost tracking are accurate enough for your market?",
            "help": "If recipe costs and reporting are wrong, your margins can look better on paper than in reality."
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
        {
            "id": "real_estate_cost_realism",
            "label": "How well do your site, rent, buildout, and opening timeline assumptions reflect your actual market?",
            "help": "Real estate and buildout often break the model before operations do."
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
