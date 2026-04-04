APP_TIERS = [
    {
        "name": "Free Tier",
        "price": "$0",
        "includes": [
            "Self & idea validation",
            "Pre-discovery financial model",
            "Post-discovery review",
            "Final decision gate",
        ],
        "boundaries": [
            "No deal execution tools",
            "No buildout tracking",
            "No full deal model",
        ],
    },
    {
        "name": "Pro Tier",
        "price": "Configurable",
        "includes": [
            "Deal Workspace",
            "Deal Model",
            "Buildout & Launch Tracker",
            "Structured execution tools",
        ],
        "boundaries": [
            "Does not replace legal review",
            "Does not replace lender underwriting",
            "Does not replace contractor project management",
        ],
    },
]

CONSULTING_OPTIONS = [
    {
        "name": "Second Opinion",
        "price": "$150–$400",
        "what_you_get": "1 structured call focused on concept, risks, and assumptions.",
        "time": "Single call",
        "boundaries": "Not legal advice, not full underwriting, not open-ended support.",
    },
    {
        "name": "Business Plan Build",
        "price": "$750–$1,250",
        "what_you_get": "Financial model refinement, business plan document, sources & uses alignment, risk review, 1–2 calls.",
        "time": "Defined scope engagement",
        "boundaries": "Limited revisions, not full SBA packaging, not legal drafting.",
    },
    {
        "name": "Monthly Execution Support – Standard",
        "price": "$199/mo",
        "what_you_get": "1 monthly call and up to 3 focused async questions.",
        "time": "Ongoing monthly",
        "boundaries": "No unlimited access, no project management, no document rewrites.",
    },
    {
        "name": "Monthly Execution Support – Premium",
        "price": "$349/mo",
        "what_you_get": "2 calls per month and priority structured support.",
        "time": "Ongoing monthly",
        "boundaries": "Still structured and time-bounded, not fractional COO support.",
    },
]

ADD_ONS = [
    ("Deal Stress Test Report", "$99–$199", "Downside scenarios, break-even sensitivity, risk flags, what breaks first."),
    ("Buildout Budget Reality Check", "$99–$249", "Cost category review, overrun risk areas, contractor prompts."),
    ("Lease & Terms Question Guide", "$29–$79", "Lease checklist, negotiation questions, exit considerations."),
    ("Top 25 Questions Guide", "$19–$49", "Franchise, financial, lease, and buildout questions."),
    ("Opening Readiness Checklist", "$49–$99", "Delay prevention checklist, readiness scoring, alert structure."),
    ("Pre-Commitment Risk Score", "Free or $9–$29", "Risk classification and decision support output."),
    ("Lender Prep Pack", "$149–$399", "Summary package, financial highlights, and lender talking points."),
]
