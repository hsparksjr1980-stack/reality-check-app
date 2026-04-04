import streamlit as st


def _inject_styles() -> None:
    st.markdown(
        """
        <style>
        .ov-hero {
            border: 1px solid rgba(120,120,120,.25);
            border-radius: 20px;
            padding: 1.35rem 1.35rem 1.05rem 1.35rem;
            margin-bottom: 1rem;
            background: rgba(255,255,255,.02);
        }
        .ov-kicker {
            font-size: 0.82rem;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            opacity: 0.72;
            margin-bottom: 0.45rem;
        }
        .ov-title {
            font-size: 1.95rem;
            font-weight: 700;
            line-height: 1.15;
            margin-bottom: 0.55rem;
        }
        .ov-subtitle {
            font-size: 1rem;
            opacity: 0.92;
            margin-bottom: 0.15rem;
        }
        .ov-section-title {
            font-size: 1.18rem;
            font-weight: 700;
            margin-top: 0.25rem;
            margin-bottom: 0.4rem;
        }
        .ov-section-subtitle {
            font-size: 0.95rem;
            opacity: 0.82;
            margin-bottom: 0.75rem;
        }
        .ov-card {
            border: 1px solid rgba(120,120,120,.22);
            border-radius: 18px;
            padding: 1rem 1rem 0.9rem 1rem;
            background: rgba(255,255,255,.02);
            margin-bottom: 1rem;
            min-height: 245px;
        }
        .ov-mini-card {
            border: 1px solid rgba(120,120,120,.2);
            border-radius: 18px;
            padding: 0.95rem 0.95rem 0.8rem 0.95rem;
            background: rgba(255,255,255,.02);
            margin-bottom: 1rem;
        }
        .ov-card-header {
            display: flex;
            align-items: center;
            gap: 0.55rem;
            margin-bottom: 0.25rem;
        }
        .ov-icon {
            font-size: 1.2rem;
            line-height: 1;
        }
        .ov-card-title {
            font-size: 1.15rem;
            font-weight: 700;
            line-height: 1.2;
        }
        .ov-tagline {
            font-size: 0.95rem;
            margin-bottom: 0.7rem;
            opacity: 0.92;
        }
        .ov-muted {
            opacity: 0.84;
        }
        .ov-helper {
            border: 1px solid rgba(120,120,120,.24);
            border-radius: 18px;
            padding: 1rem 1rem 0.75rem 1rem;
            background: rgba(255,255,255,.02);
            margin-top: 0.75rem;
        }
        .ov-roadmap-item {
            border: 1px solid rgba(120,120,120,.18);
            border-radius: 16px;
            padding: 0.8rem 0.9rem;
            background: rgba(255,255,255,.02);
            margin-bottom: 0.65rem;
        }
        .ov-roadmap-step {
            font-size: 0.8rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            opacity: 0.72;
            margin-bottom: 0.2rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def _render_hero() -> None:
    st.markdown(
        """
        <div class="ov-hero">
            <div class="ov-kicker">Reality Check</div>
            <div class="ov-title">Pressure test the franchise opportunity before you commit.</div>
            <div class="ov-subtitle">
                Move from sales language and assumptions to structure, risk, fit, and decision clarity.
                This is a guided reality-check system built to help you uncover what needs to be true before moving forward.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_how_it_works() -> None:
    st.markdown('<div class="ov-section-title">How It Works</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="ov-section-subtitle">The goal is not to push you toward a deal. The goal is to help you understand whether the opportunity fits, works, and holds up under pressure.</div>',
        unsafe_allow_html=True,
    )

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(
            """
            <div class="ov-card">
                <div class="ov-card-header">
                    <div class="ov-icon">🧠</div>
                    <div class="ov-card-title">Evaluate Yourself</div>
                </div>
                <div class="ov-tagline">Start with your time, operating style, and risk posture before getting pulled into the concept.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.write("- Operator vs investor mindset")
        st.write("- Time and lifestyle reality")
        st.write("- Risk and capital tolerance")

    with c2:
        st.markdown(
            """
            <div class="ov-card">
                <div class="ov-card-header">
                    <div class="ov-icon">🧭</div>
                    <div class="ov-card-title">Test Fit</div>
                </div>
                <div class="ov-tagline">Understand what kinds of business categories may align better with how you actually want to operate.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.write("- Concept validation")
        st.write("- Opportunity fit profile")
        st.write("- Category-level recommendations")

    with c3:
        st.markdown(
            """
            <div class="ov-card">
                <div class="ov-card-header">
                    <div class="ov-icon">📈</div>
                    <div class="ov-card-title">Pressure Test the Economics</div>
                </div>
                <div class="ov-tagline">Move past high-level assumptions and test whether the numbers still work when reality moves against you.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.write("- Financial model")
        st.write("- Guardrails")
        st.write("- Downside thinking")

    with c4:
        st.markdown(
            """
            <div class="ov-card">
                <div class="ov-card-header">
                    <div class="ov-icon">✅</div>
                    <div class="ov-card-title">Make a Clearer Decision</div>
                </div>
                <div class="ov-tagline">Decide whether to move forward, move forward with conditions, or walk away before the deal gets harder to unwind.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.write("- Post-discovery review")
        st.write("- Final decision gate")
        st.write("- Pro tools if you move forward")


def _render_what_this_is() -> None:
    st.markdown('<div class="ov-section-title">What This Is — and What It Is Not</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)

    with c1:
        st.markdown(
            """
            <div class="ov-mini-card">
                <div class="ov-card-header">
                    <div class="ov-icon">✔️</div>
                    <div class="ov-card-title">What This Is</div>
                </div>
                <div class="ov-tagline">A structured decision system designed to help you uncover the truth before committing.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.write("- A guided evaluation flow")
        st.write("- A pressure-testing framework")
        st.write("- A tool for fit, risk, and decision clarity")
        st.write("- A way to separate what sounds good from what holds up")

    with c2:
        st.markdown(
            """
            <div class="ov-mini-card">
                <div class="ov-card-header">
                    <div class="ov-icon">✖️</div>
                    <div class="ov-card-title">What This Is Not</div>
                </div>
                <div class="ov-tagline">Not a hype tool, not a franchisor pitch, and not a shortcut around diligence.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.write("- Not a guarantee of success")
        st.write("- Not legal, tax, or investment advice")
        st.write("- Not a brand recommendation engine")
        st.write("- Not a generic calculator divorced from operating reality")


def _render_roadmap() -> None:
    st.markdown('<div class="ov-section-title">App Journey</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="ov-section-subtitle">This is the path from initial interest to decision clarity.</div>',
        unsafe_allow_html=True,
    )

    roadmap = [
        ("Start", "Overview", "Understand the process, philosophy, and what this system is designed to do."),
        ("Phase 1", "Reality Check", "Pressure test your readiness, operating fit, and personal realities."),
        ("Phase 1", "Concept Validation", "Look at the business model and ask whether the concept itself fits the work required."),
        ("Phase 1", "Opportunity Fit & Recommendations", "Translate your inputs into an operator profile, fit signals, and business categories that may align better."),
        ("Phase 1", "Financial Model", "Test whether a concept that fits you also works financially."),
        ("Commercial", "Plans & Support", "See what unlocks next if you want more tools, structure, or support."),
        ("Phase 2", "Post-Discovery", "Pressure test the real deal once more facts, costs, and documents are in view."),
        ("Phase 3", "Final Decision", "Decide whether to move forward, move forward with conditions, or walk away."),
    ]

    for step, title, desc in roadmap:
        st.markdown(
            f"""
            <div class="ov-roadmap-item">
                <div class="ov-roadmap-step">{step}</div>
                <div class="ov-card-title">{title}</div>
                <div class="ov-muted">{desc}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def _render_why_this_matters() -> None:
    st.markdown('<div class="ov-section-title">Why People Get This Wrong</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="ov-section-subtitle">Many bad deals do not look bad early. They look exciting, possible, and justifiable.</div>',
        unsafe_allow_html=True,
    )

    c1, c2 = st.columns(2)

    with c1:
        st.markdown(
            """
            <div class="ov-mini-card">
                <div class="ov-card-header">
                    <div class="ov-icon">⚠️</div>
                    <div class="ov-card-title">Common Industry Pattern</div>
                </div>
                <div class="ov-tagline">Buyers often focus on the concept before pressure testing themselves, the economics, and the actual operating load.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.write("- Interest gets confused with fit")
        st.write("- Revenue stories get mistaken for likely outcomes")
        st.write("- Semi-absentee gets oversimplified")
        st.write("- Early budgets understate how much can move")

    with c2:
        st.markdown(
            """
            <div class="ov-mini-card">
                <div class="ov-card-header">
                    <div class="ov-icon">🔍</div>
                    <div class="ov-card-title">What This App Helps Surface</div>
                </div>
                <div class="ov-tagline">The point is to show where the deal depends on assumptions, unknowns, and conditions that still need to be verified.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.write("- Time and operating mismatch")
        st.write("- Capital pressure and overrun risk")
        st.write("- Labor and management intensity")
        st.write("- Unknowns that still need to become facts")


def _render_framework() -> None:
    st.markdown('<div class="ov-section-title">How to Use This System</div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="ov-helper">
            <div class="ov-card-title">Use the same framework throughout the app</div>
            <div class="ov-muted">
                Each module is built to help you look at the opportunity through the same lens:
                <strong>What to Look At</strong>, <strong>What’s Common in the Industry</strong>,
                <strong>What to Ask</strong>, and <strong>Pressure Test</strong>.
                The goal is not to hand you answers. The goal is to help you uncover what needs to be true.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_cta() -> None:
    st.markdown('<div class="ov-section-title">Next Step</div>', unsafe_allow_html=True)
    st.info("Start with Reality Check to pressure test readiness, operating fit, and personal exposure before focusing on the concept itself.")

    c1, c2 = st.columns([1, 1])

    with c1:
        if st.button("Start Reality Check", key="overview_start_reality_check", use_container_width=True):
            st.session_state["current_page"] = "Reality Check"
            st.rerun()

    with c2:
        if st.button("Go to Concept Validation", key="overview_go_concept_validation", use_container_width=True):
            st.session_state["current_page"] = "Concept Validation"
            st.rerun()


def render_overview() -> None:
    _inject_styles()

    st.title("Overview")
    _render_hero()
    _render_how_it_works()
    st.markdown("---")
    _render_what_this_is()
    st.markdown("---")
    _render_roadmap()
    st.markdown("---")
    _render_why_this_matters()
    _render_framework()
    _render_cta()
