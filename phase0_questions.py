CATEGORY_WEIGHTS = {
    "financial": 25,
    "risk": 20,
    "operator": 20,
    "skills": 15,
    "lifestyle": 10,
    "market_prework": 10,
}

CATEGORY_META = {
    "financial": {
        "title": "Financial Readiness",
        "intro": "This section tests whether you can survive the business financially, not just afford to start it."
    },
    "risk": {
        "title": "Risk Discipline",
        "intro": "This section looks at judgment, emotional discipline, and willingness to walk away."
    },
    "operator": {
        "title": "Operator Fit",
        "intro": "This section measures whether you are realistically suited for the day-to-day ownership burden."
    },
    "skills": {
        "title": "Execution Skills",
        "intro": "This section focuses on the practical skills needed to run the business."
    },
    "lifestyle": {
        "title": "Lifestyle Readiness",
        "intro": "This section checks whether your life can absorb the stress, time, and disruption."
    },
    "market_prework": {
        "title": "Industry & Real Estate Pre-Work",
        "intro": "This section tests whether you understand the industry and real estate reality before getting emotionally attached to a concept."
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
    "financial": [
        {
            "id": "liquidity",
            "label": "After paying your initial investment, how much real cash cushion would you still have left?",
            "help": "Think in terms of accessible liquidity, not retirement money or paper net worth."
        },
        {
            "id": "contingency_capital",
            "label": "If the business underperforms for 12–18 months, how prepared are you to inject more capital?",
            "help": "Most people underestimate how long underperformance can last."
        },
        {
            "id": "pg_comfort",
            "label": "How comfortable are you signing personal guarantees that could put personal assets at risk?",
            "help": "This includes the possibility that your home, savings, or other personal assets could be exposed."
        },
        {
            "id": "pg_understanding",
            "label": "How fully do you understand what a personal guarantee can mean in a bad outcome?",
            "help": "This is not just signing paperwork. It is real downside exposure."
        },
        {
            "id": "loss_tolerance",
            "label": "If this investment goes badly, how prepared are you to absorb a meaningful financial loss?",
            "help": "Be honest about your downside tolerance, not your optimism."
        },
        {
            "id": "debt_pressure",
            "label": "How prepared are you to carry debt payments while revenue ramps slower than expected?",
            "help": "Assume the business takes longer than projected to stabilize."
        },
        {
            "id": "runway_realism",
            "label": "How confident are you that your runway assumptions are based on a slow ramp, not a best-case ramp?",
            "help": "Many new operators assume the store will make money much sooner than reality."
        },
    ],
    "risk": [
        {
            "id": "walk_away",
            "label": "If the deal looks wrong late in the process, how willing are you to walk away anyway?",
            "help": "A lot of bad deals happen because people get emotionally committed."
        },
        {
            "id": "emotion_control",
            "label": "How well can you separate emotion from business decisions under pressure?",
            "help": "Especially after time, money, and pride are already invested."
        },
        {
            "id": "uncertainty",
            "label": "How comfortable are you making decisions with incomplete information?",
            "help": "Franchise buyers often want certainty that does not exist."
        },
        {
            "id": "stress_tolerance",
            "label": "How well do you handle sustained financial and operational stress?",
            "help": "Think months of pressure, not a bad week."
        },
        {
            "id": "booming_industry_bias",
            "label": "How well are you avoiding the assumption that a strong industry automatically means your location will work?",
            "help": "A growing category does not guarantee your unit economics, site, or ramp."
        },
    ],
    "operator": [
        {
            "id": "ownership_style",
            "label": "Are you approaching this like an active operator or hoping it works more like an investment?",
            "help": "Many first-time buyers underestimate how operator-heavy this becomes."
        },
        {
            "id": "ops_knowledge",
            "label": "If your manager quit tomorrow, how capable are you of actually running the business yourself?",
            "help": "Scheduling, inventory, customer issues, staffing, and daily problem-solving."
        },
        {
            "id": "daily_involvement",
            "label": "How willing are you to be highly involved day-to-day during launch and instability?",
            "help": "Early ownership rarely stays passive."
        },
        {
            "id": "people_management",
            "label": "How strong are you at managing employees, accountability, scheduling, and conflict?",
            "help": "This matters more than most buyers expect."
        },
        {
            "id": "problem_solving",
            "label": "How confident are you dealing with operational fires, last-minute staffing gaps, and customer issues?",
            "help": "You do not need perfection. You do need steadiness."
        },
    ],
    "skills": [
        {
            "id": "accounting",
            "label": "Can you look at a P&L and identify where the business is losing money without someone walking you through it?",
            "help": "Margins, labor, COGS, fixed costs, and cash pressure."
        },
        {
            "id": "marketing",
            "label": "How capable are you at driving local awareness and customer traffic if corporate support is limited?",
            "help": "Not theory — actual customer acquisition."
        },
        {
            "id": "social_media",
            "label": "How capable are you at using social media or local promotion to generate trial and repeat business?",
            "help": "This matters more in some concepts than others, but most owners need some ability here."
        },
        {
            "id": "inventory",
            "label": "How capable are you at controlling inventory, labor, and day-to-day operating discipline?",
            "help": "This is usually where margin erosion starts."
        },
        {
            "id": "learn_gaps",
            "label": "How willing are you to make real time to learn what you do not know?",
            "help": "Accounting, people management, operations, marketing, compliance, inventory."
        },
    ],
    "lifestyle": [
        {
            "id": "time_capacity",
            "label": "How realistic is your available time capacity during launch and the first year?",
            "help": "Assume the business needs more of you than expected."
        },
        {
            "id": "family_support",
            "label": "How strong is your household or family support for the pressure this could create?",
            "help": "Support matters when hours get longer and stress increases."
        },
        {
            "id": "lifestyle_impact",
            "label": "How prepared are you for the lifestyle disruption this business could cause?",
            "help": "Income stress, schedule changes, mental load, reduced flexibility."
        },
        {
            "id": "burnout_risk",
            "label": "How likely are you to become overwhelmed if the business takes more time, money, and energy than expected?",
            "help": "Try to answer this honestly, not aspirationally."
        },
    ],
    "market_prework": [
        {
            "id": "industry_understanding",
            "label": "Before evaluating a specific concept, how well do you understand the industry you are entering?",
            "help": "Margins, labor model, customer behavior, site dependence, and operating rhythm."
        },
        {
            "id": "real_estate_requirements",
            "label": "How well do you understand the type of real estate this concept actually requires?",
            "help": "Drive-thru, inline, end cap, parking, visibility, access, size, and co-tenancy all matter."
        },
        {
            "id": "local_real_estate_awareness",
            "label": "How well do you understand what is actually available in your local commercial real estate market?",
            "help": "Availability, cost, landlord quality, competition for sites, and timeline."
        },
        {
            "id": "site_timeline_realism",
            "label": "How realistic are your expectations for finding a site, signing a lease, and opening?",
            "help": "This is usually slower and harder than first-time buyers expect."
        },
    ],
}
