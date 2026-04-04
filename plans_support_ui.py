import streamlit as st


PRO_PLAN = {
    "icon": "🧭",
    "badge": "Core Upgrade",
    "name": "Reality Check Pro",
    "price": "Configurable Pricing",
    "tagline": "Build, validate, and execute the deal with more structure and control.",
    "best_for": "Users who are moving forward and want tools for deal building, modeling, and execution tracking.",
    "includes": [
        "Deal Workspace to track sites, lenders, contractors, and investors",
        "Deal Model with forecast, downside case, and scenario testing",
        "Buildout & Launch Tracker for permits, vendors, budget, blockers, and opening readiness",
    ],
    "cta_note": "Upgrade flow can be connected later. This page is the commercial packaging layer for now.",
}


CONSULTING_OPTIONS = [
    {
        "icon": "🔎",
        "name": "Second Opinion",
        "price": "$150–$400",
        "tagline": "A focused outside view on concept, risks, and assumptions.",
        "best_for": "Users who want a structured review before going deeper.",
        "includes": [
            "1 structured call",
            "Review of concept, risks, and assumptions",
            "Clear pressure-test discussion",
        ],
    },
    {
        "icon": "📘",
        "name": "Business Plan Build",
        "price": "$750–$1,250",
        "tagline": "Turn the deal into a clearer plan with stronger financial framing.",
        "best_for": "Users preparing for lender, investor, or serious decision conversations.",
        "includes": [
            "Financial model refinement",
            "Business plan document",
            "Sources & Uses alignment",
            "Risk and assumption analysis",
            "1–2 structured calls",
        ],
    },
    {
        "icon": "📅",
        "name": "Monthly Support — Standard",
        "price": "~$199/month",
        "tagline": "Light ongoing support with clear boundaries.",
        "best_for": "Users who want periodic guidance without a high-touch engagement.",
        "includes": [
            "1 call per month",
            "Up to 3 async questions",
            "Structured, focused feedback",
        ],
    },
    {
        "icon": "⭐",
        "name": "Monthly Support — Premium",
        "price": "~$349/month",
        "tagline": "More active support and a tighter feedback loop.",
        "best_for": "Users who want more involved deal support and faster responses.",
        "includes": [
            "2 calls per month",
            "Priority responses",
            "Structured support",
        ],
    },
]


ADD_ONS = [
    {
        "icon": "📊",
        "name": "Deal Stress Test Report",
        "price": "$99–$199",
        "value": "Downside scenarios, break-even sensitivity, risk flags, and a what-breaks-first summary.",
    },
    {
        "icon": "🏗️",
        "name": "Buildout Budget Reality Check",
        "price": "$99–$249",
        "value": "A focused review of buildout categories, overrun pressure points, and contractor question prompts.",
    },
    {
        "icon": "📄",
        "name": "Lease & Terms Question Guide",
        "price": "$29–$79",
        "value": "A practical checklist of lease questions, negotiation points, and exit considerations.",
    },
    {
        "icon": "❓",
        "name": "Top 25 Questions Guide",
        "price": "$19–$49",
        "value": "A compact guide covering franchise, financial, lease, and buildout questions to ask.",
    },
    {
        "icon": "✅",
        "name": "Opening Readiness Checklist",
        "price": "$49–$99",
        "value": "A readiness-focused checklist built to help prevent delays and identify launch gaps.",
    },
    {
        "icon": "💼",
        "name": "Lender Prep Pack",
        "price": "$149–$399",
        "value": "A summary package with financial highlights and talking points for lender conversations.",
    },
]


def _inject_styles() -> None:
    st.markdown(
        """
        <style>
        .ps-hero {
            border: 1px solid rgba(120,120,120,.25);
            border-radius: 20px;
            padding: 1.35rem 1.35rem 1.05rem 1.35rem;
            margin-bottom: 1rem;
            background: rgba(255,255,255,.02);
        }
        .ps-kicker {
            font-size: 0.82rem;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            opacity: 0.72;
            margin-bottom: 0.45rem;
        }
        .ps-title {
            font-size: 1.9rem;
            font-weight: 700;
            line-height: 1.15;
            margin-bottom: 0.55rem;
        }
        .ps-subtitle {
            font-size: 1rem;
            opacity: 0.92;
            margin-bottom: 0.15rem;
        }
        .ps-section-title {
            font-size: 1.18rem;
            font-weight: 700;
            margin-top: 0.25rem;
            margin-bottom: 0.4rem;
        }
        .ps-section-subtitle {
            font-size: 0.95rem;
            opacity: 0.82;
            margin-bottom: 0.75rem;
        }
        .ps-card {
            border: 1px solid rgba(120,120,120,.22);
            border-radius: 18px;
            padding: 1rem 1rem 0.9rem 1rem;
            background: rgba(255,255,255,.02);
            margin-bottom: 1rem;
        }
        .ps-card-featured {
            border: 1px solid rgba(120,120,120,.34);
            border-radius: 20px;
            padding: 1.15rem 1.15rem 0.95rem 1.15rem;
            background: rgba(255,255,255,.035);
            margin-bottom: 1rem;
        }
        .ps-mini-card {
            border: 1px solid rgba(120,120,120,.2);
            border-radius: 18px;
            padding: 0.9rem 0.95rem 0.8rem 0.95rem;
            background: rgba(255,255,255,.02);
            margin-bottom: 1rem;
            min-height: 230px;
        }
        .ps-card-header {
            display: flex;
            align-items: center;
            gap: 0.55rem;
            margin-bottom: 0.25rem;
        }
        .ps-icon {
            font-size: 1.2rem;
            line-height: 1;
        }
        .ps-card-title {
            font-size: 1.18rem;
            font-weight: 700;
            line-height: 1.2;
        }
        .ps-badge {
            display: inline-block;
            font-size: 0.74rem;
            font-weight: 600;
            padding: 0.22rem 0.5rem;
            border-radius: 999px;
            border: 1px solid rgba(120,120,120,.28);
            opacity: 0.9;
            margin-bottom: 0.55rem;
        }
        .ps-price {
            font-size: 1rem;
            font-weight: 600;
            margin-top: 0.1rem;
            margin-bottom: 0.5rem;
            opacity: 0.96;
        }
        .ps-tagline {
            font-size: 0.95rem;
            margin-bottom: 0.7rem;
            opacity: 0.92;
        }
        .ps-bestfor {
            font-size: 0.91rem;
            margin-top: 0.75rem;
            padding-top: 0.6rem;
            border-top: 1px solid rgba(120,120,120,.18);
            opacity: 0.9;
        }
        .ps-helper {
            border: 1px solid rgba(120,120,120,.24);
            border-radius: 18px;
            padding: 1rem 1rem 0.75rem 1rem;
            background: rgba(255,255,255,.02);
            margin-top: 0.75rem;
        }
        .ps-muted {
            opacity: 0.84;
        }
        .ps-list-title {
            font-size: 0.92rem;
            font-weight: 600;
            margin-bottom: 0.35rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def _render_hero() -> None:
    st.markdown(
        """
        <div class="ps-hero">
            <div class="ps-kicker">Plans & Support</div>
            <div class="ps-title">You’ve done the early work. Now choose how you want to move forward.</div>
            <div class="ps-subtitle">
                Use Pro tools to build and execute the deal yourself, or add structured support if you want a second opinion,
                a business plan build, or ongoing guidance.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_unlocks_next() -> None:
    st.markdown('<div class="ps-section-title">What Unlocks Next</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="ps-section-subtitle">This is the shift from evaluation into real deal building and execution.</div>',
        unsafe_allow_html=True,
    )

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown(
            """
            <div class="ps-mini-card">
                <div class="ps-card-header">
                    <div class="ps-icon">🗂️</div>
                    <div class="ps-card-title">Deal Workspace</div>
                </div>
                <div class="ps-tagline">Track the real moving parts of the deal in one place.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.write("- Site selection tracking")
        st.write("- Lease and lender tracking")
        st.write("- Contractor and investor tracking")

    with c2:
        st.markdown(
            """
            <div class="ps-mini-card">
                <div class="ps-card-header">
                    <div class="ps-icon">📈</div>
                    <div class="ps-card-title">Deal Model</div>
                </div>
                <div class="ps-tagline">Go beyond rough math and pressure test the economics.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.write("- 3-year forecast")
        st.write("- Scenario and downside analysis")
        st.write("- What-breaks-first view")

    with c3:
        st.markdown(
            """
            <div class="ps-mini-card">
                <div class="ps-card-header">
                    <div class="ps-icon">🚧</div>
                    <div class="ps-card-title">Buildout &amp; Launch Tracker</div>
                </div>
                <div class="ps-tagline">Manage execution, delays, vendors, and opening readiness.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.write("- Permits and regulatory tracking")
        st.write("- Budget vs actual")
        st.write("- Timeline, blockers, and readiness")


def _render_pro_plan() -> None:
    st.markdown('<div class="ps-section-title">Pro App Plan</div>', unsafe_allow_html=True)

    st.markdown(
        f"""
        <div class="ps-card-featured">
            <div class="ps-badge">{PRO_PLAN["badge"]}</div>
            <div class="ps-card-header">
                <div class="ps-icon">{PRO_PLAN["icon"]}</div>
                <div class="ps-card-title">{PRO_PLAN["name"]}</div>
            </div>
            <div class="ps-price">{PRO_PLAN["price"]}</div>
            <div class="ps-tagline">{PRO_PLAN["tagline"]}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="ps-list-title">What’s included</div>', unsafe_allow_html=True)
        for item in PRO_PLAN["includes"][:2]:
            st.write(f"- {item}")
    with c2:
        st.markdown('<div class="ps-list-title">Also included</div>', unsafe_allow_html=True)
        for item in PRO_PLAN["includes"][2:]:
            st.write(f"- {item}")

    st.markdown(
        f"""
        <div class="ps-bestfor"><strong>Best for:</strong> {PRO_PLAN["best_for"]}</div>
        """,
        unsafe_allow_html=True,
    )

    c1, c2 = st.columns([1, 2])
    with c1:
        st.button("Unlock Pro", key="unlock_pro_top", use_container_width=True, disabled=True)
    with c2:
        st.caption(PRO_PLAN["cta_note"])


def _render_consulting_card(option: dict) -> None:
    st.markdown(
        f"""
        <div class="ps-card">
            <div class="ps-card-header">
                <div class="ps-icon">{option["icon"]}</div>
                <div class="ps-card-title">{option["name"]}</div>
            </div>
            <div class="ps-price">{option["price"]}</div>
            <div class="ps-tagline">{option["tagline"]}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown('<div class="ps-list-title">Includes</div>', unsafe_allow_html=True)
    for item in option["includes"]:
        st.write(f"- {item}")
    st.markdown(
        f"""
        <div class="ps-bestfor"><strong>Best for:</strong> {option["best_for"]}</div>
        """,
        unsafe_allow_html=True,
    )


def _render_consulting_cards() -> None:
    st.markdown('<div class="ps-section-title">Structured Support Options</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="ps-section-subtitle">These are separate from the app subscription and built to stay structured, time-bounded, and scalable.</div>',
        unsafe_allow_html=True,
    )

    row1 = st.columns(2)
    with row1[0]:
        _render_consulting_card(CONSULTING_OPTIONS[0])
    with row1[1]:
        _render_consulting_card(CONSULTING_OPTIONS[1])

    row2 = st.columns(2)
    with row2[0]:
        _render_consulting_card(CONSULTING_OPTIONS[2])
    with row2[1]:
        _render_consulting_card(CONSULTING_OPTIONS[3])


def _render_add_ons() -> None:
    st.markdown('<div class="ps-section-title">Optional Add-Ons</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="ps-section-subtitle">Use targeted reports and guides when you want help with one specific part of the deal.</div>',
        unsafe_allow_html=True,
    )

    cols = st.columns(2)
    for idx, addon in enumerate(ADD_ONS):
        with cols[idx % 2]:
            st.markdown(
                f"""
                <div class="ps-card">
                    <div class="ps-card-header">
                        <div class="ps-icon">{addon["icon"]}</div>
                        <div class="ps-card-title">{addon["name"]}</div>
                    </div>
                    <div class="ps-price">{addon["price"]}</div>
                    <div class="ps-tagline">{addon["value"]}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )


def _render_helper_box() -> None:
    st.markdown(
        """
        <div class="ps-helper">
            <div class="ps-card-title">Which option may fit you best?</div>
            <div class="ps-muted">
                Choose <strong>Pro</strong> if you want the tools to structure, validate, and execute the deal yourself.
                Choose <strong>Second Opinion</strong> if you want a focused outside review.
                Choose <strong>Business Plan Build</strong> if you need a stronger package for lender or investor conversations.
                Choose <strong>Monthly Support</strong> if you want structured ongoing help without turning this into open-ended consulting.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_next_step() -> None:
    st.markdown('<div class="ps-section-title">Next Step</div>', unsafe_allow_html=True)
    st.info("Once you understand what tools and support are available, continue into Post-Discovery to pressure test the deal more seriously.")

    c1, c2 = st.columns([1, 1])
    with c1:
        if st.button("Continue to Post-Discovery", use_container_width=True):
            st.session_state["current_page"] = "Post-Discovery"
            st.rerun()
    with c2:
        st.button("Unlock Pro", key="unlock_pro_bottom", use_container_width=True, disabled=True)


def render_plans_support() -> None:
    _inject_styles()

    st.title("Plans & Support")
    _render_hero()
    _render_unlocks_next()
    st.markdown("---")
    _render_pro_plan()
    st.markdown("---")
    _render_consulting_cards()
    st.markdown("---")
    _render_add_ons()
    _render_helper_box()
    _render_next_step()
