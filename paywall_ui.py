# paywall_ui.py

from __future__ import annotations

import html
from typing import Final

import streamlit as st

from ui_styles import close_shell, open_shell, render_card, render_page_header, render_section_intro


PLAN_UNLOCKS: Final[dict[str, list[str]]] = {
    "free": [
        "Core assessment workflow",
        "Free report access",
    ],
    "pro": [
        "Deal Workspace",
        "Deal Model",
        "Buildout & Launch Tracker",
        "Execution Report",
    ],
}


def _money(value: int | float) -> str:
    return f"${float(value):,.0f}"


def _inject_local_styles() -> None:
    st.markdown(
        """
        <style>
            .pw-box {
                background: #ffffff;
                border: 1px solid #e5e7eb;
                border-radius: 20px;
                box-shadow: 0 8px 24px rgba(17, 24, 39, 0.06);
                padding: 1.2rem;
            }

            .pw-row {
                display: flex;
                justify-content: space-between;
                gap: 1rem;
                padding: 0.55rem 0;
                border-bottom: 1px solid #f3f4f6;
                color: #374151;
                font-size: 0.95rem;
            }

            .pw-row:last-child {
                border-bottom: none;
            }

            .pw-total {
                font-size: 1.28rem;
                font-weight: 800;
                color: #111827;
                padding-top: 0.8rem;
            }

            .pw-note {
                font-size: 0.92rem;
                line-height: 1.6;
                color: #4b5563;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def _ensure_checkout_state() -> None:
    st.session_state.setdefault("selected_plan_id", "free")
    st.session_state.setdefault("selected_service_ids", [])
    st.session_state.setdefault("cart_items", [])
    st.session_state.setdefault("cart_subtotal", 0.0)
    st.session_state.setdefault("checkout_ready", False)
    st.session_state.setdefault("subscription_status", "free")
    st.session_state.setdefault("purchased_services", [])
    st.session_state.setdefault("checkout_complete", False)


def _complete_checkout() -> None:
    selected_plan_id = str(st.session_state.get("selected_plan_id", "free"))
    selected_service_ids = list(st.session_state.get("selected_service_ids", []))

    st.session_state["subscription_status"] = "active" if selected_plan_id == "pro" else "free"
    st.session_state["premium_access"] = selected_plan_id == "pro"
    st.session_state["purchased_services"] = selected_service_ids
    st.session_state["checkout_complete"] = True

    if selected_plan_id == "pro":
        st.session_state["move_forward"] = True
        st.session_state["current_page"] = "Deal Workspace"
    else:
        st.session_state["current_page"] = "Overview"

    st.rerun()


def _back_to_plans() -> None:
    st.session_state["current_page"] = "Plans & Support"
    st.rerun()


def _render_basket_summary() -> None:
    cart_items = list(st.session_state.get("cart_items", []))
    subtotal = float(st.session_state.get("cart_subtotal", 0.0))

    st.markdown('<div class="pw-box">', unsafe_allow_html=True)

    if not cart_items:
        st.write("Your basket is currently empty.")
    else:
        for item in cart_items:
            st.markdown(
                f"""
                <div class="pw-row">
                    <div>{html.escape(str(item["name"]))}</div>
                    <div>{_money(float(item["price"]))}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown(
            f'<div class="pw-total">Total: {_money(subtotal)}</div>',
            unsafe_allow_html=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)


def render_paywall() -> None:
    _ensure_checkout_state()
    _inject_local_styles()

    cart_items = list(st.session_state.get("cart_items", []))
    subtotal = float(st.session_state.get("cart_subtotal", 0.0))
    checkout_ready = bool(st.session_state.get("checkout_ready", False))
    selected_plan_id = str(st.session_state.get("selected_plan_id", "free"))
    unlocks = PLAN_UNLOCKS.get(selected_plan_id, [])

    open_shell()

    render_page_header(
        eyebrow="Checkout",
        title="Review your basket before payment.",
        subtitle=(
            "This paywall is ready for a future payment provider. For now, it acts as a "
            "clean checkout summary and temporary entitlement handoff."
        ),
        wide=True,
    )

    st.markdown('<div class="rc-gap-lg"></div>', unsafe_allow_html=True)

    if bool(st.session_state.get("dev_pro_access", False)):
        st.info("Developer override is enabled. Pro pages are currently accessible without checkout.")

    if not cart_items:
        st.warning("Your basket is empty. Go back to Plans & Support to choose a plan or services.")

        st.markdown('<div class="rc-gap-md"></div>', unsafe_allow_html=True)

        if st.button(
            "Back to Plans & Support",
            key="paywall_back_empty",
            use_container_width=True,
            type="primary",
        ):
            _back_to_plans()

        close_shell()
        return

    col1, col2 = st.columns([1.35, 1], gap="large")

    with col1:
        render_section_intro(
            title="Basket summary",
            body="Review everything selected in Plans & Support before continuing.",
        )
        st.markdown('<div class="rc-gap-md"></div>', unsafe_allow_html=True)

        _render_basket_summary()

        st.markdown('<div class="rc-gap-lg"></div>', unsafe_allow_html=True)

        render_section_intro(
            title="What happens after checkout",
            body="Platform access and advisory support are handled differently.",
        )
        st.markdown('<div class="rc-gap-md"></div>', unsafe_allow_html=True)

        c1, c2 = st.columns(2, gap="medium")
        with c1:
            render_card(
                label="Plan unlocks",
                title="Included platform access",
                body=", ".join(unlocks) if unlocks else "No additional app unlocks.",
            )
        with c2:
            render_card(
                label="Service fulfillment",
                title="Support is recorded separately",
                body="Consulting and one-off services are saved as purchased support items.",
            )

    with col2:
        render_section_intro(
            title="Order summary",
            body="Use this to confirm the current basket before payment.",
        )
        st.markdown('<div class="rc-gap-md"></div>', unsafe_allow_html=True)

        render_card(
            label="Selected plan",
            title=selected_plan_id.title(),
            body="Only Pro unlocks the execution-side working tools.",
        )

        st.markdown('<div class="rc-gap-md"></div>', unsafe_allow_html=True)

        render_card(
            label="Subtotal",
            title=_money(subtotal),
            body="Current basket total before provider integration.",
        )

        st.markdown('<div class="rc-gap-md"></div>', unsafe_allow_html=True)

        st.markdown(
            """
            <div class="pw-note">
                This is a temporary checkout flow. Later, this button can connect to Stripe or another billing provider.
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown('<div class="rc-gap-md"></div>', unsafe_allow_html=True)

        if st.button(
            "Proceed to Payment",
            key="paywall_proceed",
            use_container_width=True,
            type="primary",
            disabled=not checkout_ready,
        ):
            _complete_checkout()

        if st.button(
            "Back to Plans & Support",
            key="paywall_back",
            use_container_width=True,
        ):
            _back_to_plans()

    close_shell()
