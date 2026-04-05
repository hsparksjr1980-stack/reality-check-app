# plans_support_ui.py

from __future__ import annotations

import html
from typing import Final

import streamlit as st

from ui_styles import close_shell, open_shell, render_page_header, render_section_intro


PLAN_ITEMS: Final[list[dict[str, object]]] = [
    {
        "id": "free",
        "category": "plan",
        "name": "Free",
        "price": 0,
        "price_note": "Included with the base assessment experience.",
        "description": (
            "Best for early-stage evaluation when you want to assess fit, concept quality, "
            "and initial economics before going deeper."
        ),
        "features": [
            "Reality Check and Concept Validation",
            "Opportunity Fit and early outputs",
            "Preliminary report and decision support",
        ],
        "featured": False,
    },
    {
        "id": "pro",
        "category": "plan",
        "name": "Pro",
        "price": 2495,
        "price_note": "Unlock deeper execution tools and reporting.",
        "description": (
            "Best for users moving forward who want more support with deal work, deeper "
            "modeling, execution planning, and reporting."
        ),
        "features": [
            "Deal Workspace access",
            "Deal Model and 3-year forecast tools",
            "Buildout and launch tracking support",
            "Execution Report access",
        ],
        "featured": True,
    },
]

SERVICE_ITEMS: Final[list[dict[str, object]]] = [
    {
        "id": "strategy_session",
        "category": "consulting",
        "name": "Strategy Session",
        "price": 495,
        "description": "A focused session to review scores, concerns, and next-step decision path.",
    },
    {
        "id": "opportunity_review",
        "category": "consulting",
        "name": "Opportunity Review",
        "price": 1250,
        "description": "A direct review of the opportunity, key assumptions, and main risk areas.",
    },
    {
        "id": "model_review",
        "category": "service",
        "name": "Model Review",
        "price": 750,
        "description": "Pressure test assumptions, economics, and where the model may be overstating the case.",
    },
    {
        "id": "diligence_support",
        "category": "service",
        "name": "Diligence Support",
        "price": 950,
        "description": "Help organizing diligence questions, follow-up items, and red flags before moving forward.",
    },
    {
        "id": "decision_memo",
        "category": "service",
        "name": "Decision Memo",
        "price": 650,
        "description": "A concise decision-oriented summary of the opportunity, risks, and recommendation.",
    },
]


def _money(value: int | float) -> str:
    return f"${float(value):,.0f}"


def _inject_local_styles() -> None:
    st.markdown(
        """
        <style>
            .ps-card {
                background: #ffffff;
                border: 1px solid #e5e7eb;
                border-radius: 20px;
                box-shadow: 0 8px 24px rgba(17, 24, 39, 0.06);
                padding: 1.2rem 1.2rem 1.05rem 1.2rem;
                height: 100%;
            }

            .ps-card-featured {
                border-color: rgba(46, 107, 230, 0.28);
                box-shadow: 0 10px 28px rgba(46, 107, 230, 0.10);
            }

            .ps-label {
                display: inline-block;
                font-size: 0.72rem;
                font-weight: 700;
                letter-spacing: 0.08em;
                text-transform: uppercase;
                color: #6b7280;
                margin-bottom: 0.55rem;
            }

            .ps-badge {
                display: inline-block;
                margin-left: 0.45rem;
                padding: 0.18rem 0.5rem;
                border-radius: 999px;
                background: rgba(46, 107, 230, 0.08);
                border: 1px solid rgba(46, 107, 230, 0.18);
                color: #2e6be6;
                font-size: 0.68rem;
                font-weight: 700;
                letter-spacing: 0.04em;
                text-transform: uppercase;
                vertical-align: middle;
            }

            .ps-title {
                font-size: 1.24rem;
                font-weight: 800;
                line-height: 1.18;
                color: #111827;
                margin-bottom: 0.35rem;
            }

            .ps-price {
                font-size: 1.8rem;
                font-weight: 800;
                line-height: 1;
                color: #111827;
                margin-bottom: 0.25rem;
            }

            .ps-price-note {
                font-size: 0.9rem;
                line-height: 1.5;
                color: #6b7280;
                margin-bottom: 0.85rem;
            }

            .ps-body {
                font-size: 0.95rem;
                line-height: 1.62;
                color: #4b5563;
                margin-bottom: 0.9rem;
            }

            .ps-list {
                margin: 0;
                padding-left: 1.05rem;
                color: #374151;
                font-size: 0.92rem;
                line-height: 1.62;
            }

            .ps-list li {
                margin-bottom: 0.32rem;
            }

            .ps-mini-card {
                background: #ffffff;
                border: 1px solid #e5e7eb;
                border-radius: 18px;
                box-shadow: 0 8px 24px rgba(17, 24, 39, 0.05);
                padding: 1rem 1rem 0.95rem 1rem;
                height: 100%;
            }

            .ps-mini-title {
                font-size: 1rem;
                font-weight: 750;
                line-height: 1.3;
                color: #111827;
                margin-bottom: 0.25rem;
            }

            .ps-mini-price {
                font-size: 1.05rem;
                font-weight: 800;
                line-height: 1.2;
                color: #111827;
                margin-bottom: 0.35rem;
            }

            .ps-mini-body {
                font-size: 0.92rem;
                line-height: 1.58;
                color: #4b5563;
                margin-bottom: 0;
            }

            .ps-basket {
                background: #ffffff;
                border: 1px solid #e5e7eb;
                border-radius: 20px;
                box-shadow: 0 8px 24px rgba(17, 24, 39, 0.05);
                padding: 1.1rem 1.1rem 1rem 1.1rem;
            }

            .ps-basket-title {
                font-size: 1.05rem;
                font-weight: 780;
                color: #111827;
                margin-bottom: 0.4rem;
            }

            .ps-basket-item {
                font-size: 0.93rem;
                line-height: 1.55;
                color: #374151;
                padding: 0.3rem 0;
                border-bottom: 1px solid #f3f4f6;
            }

            .ps-basket-total {
                font-size: 1.2rem;
                font-weight: 800;
                color: #111827;
                margin-top: 0.8rem;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def _ensure_cart_state() -> None:
    st.session_state.setdefault("selected_plan_id", "free")
    st.session_state.setdefault("selected_service_ids", [])
    st.session_state.setdefault("cart_items", [])
    st.session_state.setdefault("cart_subtotal", 0.0)
    st.session_state.setdefault("checkout_ready", False)
    st.session_state.setdefault("subscription_status", "free")


def _find_item(item_id: str) -> dict[str, object] | None:
    for item in PLAN_ITEMS + SERVICE_ITEMS:
        if item["id"] == item_id:
            return item
    return None


def _rebuild_cart() -> None:
    selected_plan_id = str(st.session_state.get("selected_plan_id", "free"))
    selected_service_ids = list(st.session_state.get("selected_service_ids", []))

    items: list[dict[str, object]] = []
    subtotal = 0.0

    plan = _find_item(selected_plan_id)
    if plan is not None:
        items.append(plan)
        subtotal += float(plan["price"])

    for service_id in selected_service_ids:
        service = _find_item(service_id)
        if service is not None:
            items.append(service)
            subtotal += float(service["price"])

    st.session_state["cart_items"] = items
    st.session_state["cart_subtotal"] = subtotal
    st.session_state["checkout_ready"] = len(items) > 0


def _set_plan(plan_id: str) -> None:
    st.session_state["selected_plan_id"] = plan_id
    _rebuild_cart()
    st.rerun()


def _toggle_service(service_id: str) -> None:
    current = set(st.session_state.get("selected_service_ids", []))
    if service_id in current:
        current.remove(service_id)
    else:
        current.add(service_id)
    st.session_state["selected_service_ids"] = sorted(current)
    _rebuild_cart()
    st.rerun()


def _clear_basket() -> None:
    st.session_state["selected_plan_id"] = "free"
    st.session_state["selected_service_ids"] = []
    _rebuild_cart()
    st.rerun()


def _render_plan_card(item: dict[str, object]) -> None:
    is_selected = str(st.session_state.get("selected_plan_id", "free")) == item["id"]
    featured = bool(item.get("featured", False))
    badge_html = '<span class="ps-badge">Recommended</span>' if featured else ""
    class_name = "ps-card ps-card-featured" if featured else "ps-card"
    features_html = "".join(f"<li>{html.escape(str(feature))}</li>" for feature in item["features"])

    st.markdown(
        f"""
        <div class="{class_name}">
            <div class="ps-label">Plan{badge_html}</div>
            <div class="ps-title">{html.escape(str(item["name"]))}</div>
            <div class="ps-price">{_money(float(item["price"]))}</div>
            <div class="ps-price-note">{html.escape(str(item["price_note"]))}</div>
            <div class="ps-body">{html.escape(str(item["description"]))}</div>
            <ul class="ps-list">{features_html}</ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="rc-gap-md"></div>', unsafe_allow_html=True)

    button_label = "Selected" if is_selected else f"Choose {item['name']}"
    if st.button(
        button_label,
        key=f"plan_{item['id']}",
        use_container_width=True,
        type="primary" if featured or is_selected else "secondary",
        disabled=is_selected,
    ):
        _set_plan(str(item["id"]))


def _render_service_card(item: dict[str, object]) -> None:
    selected_ids = set(st.session_state.get("selected_service_ids", []))
    is_selected = item["id"] in selected_ids

    st.markdown(
        f"""
        <div class="ps-mini-card">
            <div class="ps-label">{html.escape(str(item["category"]))}</div>
            <div class="ps-mini-title">{html.escape(str(item["name"]))}</div>
            <div class="ps-mini-price">{_money(float(item["price"]))}</div>
            <div class="ps-mini-body">{html.escape(str(item["description"]))}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="rc-gap-md"></div>', unsafe_allow_html=True)

    button_label = "Remove from Basket" if is_selected else "Add to Basket"
    if st.button(
        button_label,
        key=f"service_{item['id']}",
        use_container_width=True,
        type="primary" if is_selected else "secondary",
    ):
        _toggle_service(str(item["id"]))


def _render_basket() -> None:
    items = list(st.session_state.get("cart_items", []))
    subtotal = float(st.session_state.get("cart_subtotal", 0.0))

    st.markdown(
        '<div class="ps-basket"><div class="ps-basket-title">Selected Items</div>',
        unsafe_allow_html=True,
    )

    if not items:
        st.write("No items selected yet.")
    else:
        for item in items:
            st.markdown(
                f'<div class="ps-basket-item">{html.escape(str(item["name"]))} — {_money(float(item["price"]))}</div>',
                unsafe_allow_html=True,
            )

    st.markdown(
        f'<div class="ps-basket-total">Subtotal: {_money(subtotal)}</div></div>',
        unsafe_allow_html=True,
    )

    st.markdown('<div class="rc-gap-md"></div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2, gap="large")
    with c1:
        if st.button(
            "Continue to Checkout",
            key="plans_continue_to_checkout",
            use_container_width=True,
            type="primary",
            disabled=not bool(st.session_state.get("checkout_ready", False)),
        ):
            st.session_state["current_page"] = "Paywall"
            st.rerun()

    with c2:
        if st.button(
            "Clear Basket",
            key="plans_clear_basket",
            use_container_width=True,
        ):
            _clear_basket()

    if st.session_state.get("dev_pro_access", False):
        st.markdown('<div class="rc-gap-sm"></div>', unsafe_allow_html=True)
        st.info("Developer override is enabled. Pro pages are currently accessible without checkout.")


def render_plans_support() -> None:
    _inject_local_styles()
    _ensure_cart_state()
    _rebuild_cart()

    open_shell()

    render_page_header(
        eyebrow="Plans & Support",
        title="Select the support that fits your next step.",
        subtitle=(
            "Choose your platform plan, add any advisory support you want, "
            "and continue to checkout when your basket is ready."
        ),
        wide=True,
    )

    st.markdown('<div class="rc-gap-lg"></div>', unsafe_allow_html=True)

    render_section_intro(
        title="Platform access",
        body="Choose one plan. You can add consulting and one-off services on top of it.",
    )
    st.markdown('<div class="rc-gap-md"></div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="large")
    with col1:
        _render_plan_card(PLAN_ITEMS[0])
    with col2:
        _render_plan_card(PLAN_ITEMS[1])

    st.markdown('<div class="rc-gap-lg"></div>', unsafe_allow_html=True)

    render_section_intro(
        title="Consulting and one-off support",
        body="Add any focused support you want included in the basket.",
    )
    st.markdown('<div class="rc-gap-md"></div>', unsafe_allow_html=True)

    row1 = st.columns(2, gap="large")
    with row1[0]:
        _render_service_card(SERVICE_ITEMS[0])
    with row1[1]:
        _render_service_card(SERVICE_ITEMS[1])

    row2 = st.columns(3, gap="medium")
    with row2[0]:
        _render_service_card(SERVICE_ITEMS[2])
    with row2[1]:
        _render_service_card(SERVICE_ITEMS[3])
    with row2[2]:
        _render_service_card(SERVICE_ITEMS[4])

    st.markdown('<div class="rc-gap-lg"></div>', unsafe_allow_html=True)

    render_section_intro(
        title="Basket",
        body="Review the current selection before moving to checkout.",
    )
    st.markdown('<div class="rc-gap-md"></div>', unsafe_allow_html=True)

    _render_basket()

    close_shell()
