# deal_model_ui.py

from __future__ import annotations

import pandas as pd
import streamlit as st

from deal_model_logic import (
    MONTH_LABELS,
    build_3year_forecast,
    build_balance_sheet_summary,
    build_monthly_pnl_views,
    build_pnl,
    calculate_metrics,
    run_downside_case,
    what_breaks_first,
)
from deal_workspace_logic import calc_sources_uses
from ui_styles import (
    close_shell,
    open_shell,
    render_card,
    render_page_header,
    render_section_intro,
)


def pct(x: float) -> str:
    return f"{x * 100:,.1f}%"


def money(x: float) -> str:
    return f"${x:,.0f}"


def _safe_float(value, fallback: float = 0.0) -> float:
    try:
        if value is None or value == "":
            return float(fallback)
        return float(value)
    except (TypeError, ValueError):
        return float(fallback)


def _get_default(session_key: str, fm_key: str, fallback):
    return st.session_state.get(session_key, st.session_state.get(fm_key, fallback))


def _init_monthly_plan() -> None:
    if "deal_monthly_plan" not in st.session_state:
        st.session_state["deal_monthly_plan"] = pd.DataFrame(
            {
                "Month": MONTH_LABELS,
                "Revenue": [0.0] * 12,
                "Tickets": [0.0] * 12,
                "Avg Ticket": [0.0] * 12,
            }
        )


def _make_number_input(
    label: str,
    key: str,
    value,
    step=100.0,
    min_value=0.0,
    max_value=None,
    fmt: str | None = None,
):
    kwargs = {
        "label": label,
        "min_value": min_value,
        "value": value,
        "step": step,
        "key": key,
    }
    if max_value is not None:
        kwargs["max_value"] = max_value
    if fmt is not None:
        kwargs["format"] = fmt
    return st.number_input(**kwargs)


def _render_workspace_metrics(su: dict) -> None:
    render_section_intro(
        title="Live inputs from Deal Workspace",
        body="These values are being pulled into the model from the workspace so the forecast stays connected to the current deal structure.",
    )
    st.markdown('<div class="rc-gap-md"></div>', unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4, gap="medium")
    with c1:
        render_card(
            label="Sources & Uses",
            title=money(su["total_uses"]),
            body="Total uses currently flowing in from the workspace.",
        )
    with c2:
        render_card(
            label="Funding",
            title=money(su["total_sources"]),
            body="Total debt and equity sources currently selected.",
        )
    with c3:
        render_card(
            label="Gap",
            title=money(su["gap"]),
            body="Positive values indicate additional funding is still needed.",
        )
    with c4:
        render_card(
            label="Debt service",
            title=money(su["debt_payment"]),
            body="Estimated monthly debt payment from the selected structure.",
        )


def _render_revenue_setup():
    render_section_intro(
        title="Revenue setup",
        body="Choose how Year 1 revenue should be built, then decide whether the forecast should stay flat or use a monthly plan.",
    )
    st.markdown('<div class="rc-gap-md"></div>', unsafe_allow_html=True)

    revenue_mode = st.radio(
        "Revenue setup mode",
        ["Annual Revenue", "Annual Tickets x Average Ticket"],
        horizontal=True,
        key="deal_revenue_mode_radio",
    )

    forecast_mode = st.radio(
        "Forecast mode",
        ["Flat Monthly", "Seasonal Monthly Plan"],
        horizontal=True,
        key="deal_forecast_mode_radio",
    )

    revenue_mode_internal = "annual_revenue" if revenue_mode == "Annual Revenue" else "annual_tickets"
    forecast_mode_internal = "flat" if forecast_mode == "Flat Monthly" else "seasonal"

    annual_revenue = 0.0
    annual_tickets = 0.0
    avg_ticket = 0.0
    seasonality_mode_internal = "monthly_revenue"

    if forecast_mode_internal == "flat":
        if revenue_mode_internal == "annual_revenue":
            annual_revenue = _make_number_input(
                "Annual Revenue",
                "deal_annual_revenue_input",
                float(_get_default("deal_annual_revenue", "fm_target_monthly_revenue", 120000.0) * 12),
                step=10000.0,
            )
            implied_monthly_revenue = annual_revenue / 12

            m1, m2 = st.columns(2, gap="large")
            with m1:
                st.metric("Monthly Revenue", money(implied_monthly_revenue))
            with m2:
                st.metric("Annual Revenue", money(annual_revenue))
        else:
            col1, col2 = st.columns(2, gap="large")
            with col1:
                annual_tickets = _make_number_input(
                    "Annual Tickets",
                    "deal_annual_tickets_input",
                    float(st.session_state.get("deal_annual_tickets", 60000.0)),
                    step=1000.0,
                )
            with col2:
                avg_ticket = _make_number_input(
                    "Average Ticket",
                    "deal_avg_ticket_input",
                    float(st.session_state.get("deal_avg_ticket", st.session_state.get("avg_ticket", 8.75))),
                    step=0.25,
                )

            annual_revenue = annual_tickets * avg_ticket
            implied_monthly_revenue = annual_revenue / 12

            m1, m2 = st.columns(2, gap="large")
            with m1:
                st.metric("Annual Revenue", money(annual_revenue))
            with m2:
                st.metric("Monthly Revenue", money(implied_monthly_revenue))
    else:
        seasonality_mode = st.radio(
            "Seasonal monthly input",
            ["Monthly Revenue", "Monthly Tickets x Average Ticket"],
            horizontal=True,
            key="deal_seasonality_mode_radio",
        )
        seasonality_mode_internal = "monthly_revenue" if seasonality_mode == "Monthly Revenue" else "monthly_tickets"

        plan_df = st.session_state.get("deal_monthly_plan").copy()

        if seasonality_mode_internal == "monthly_revenue":
            st.caption("Enter monthly revenue by month.")
            edited_plan = st.data_editor(
                plan_df[["Month", "Revenue"]],
                num_rows="fixed",
                use_container_width=True,
                hide_index=True,
                key="deal_monthly_plan_editor_revenue",
            )
            plan_df["Revenue"] = pd.to_numeric(edited_plan["Revenue"], errors="coerce").fillna(0.0)
            plan_df["Tickets"] = 0.0
            plan_df["Avg Ticket"] = 0.0
            annual_revenue = float(plan_df["Revenue"].sum())
            st.metric("Year 1 Revenue from Monthly Plan", money(annual_revenue))
        else:
            st.caption("Enter monthly tickets and average ticket by month.")
            edited_plan = st.data_editor(
                plan_df[["Month", "Tickets", "Avg Ticket"]],
                num_rows="fixed",
                use_container_width=True,
                hide_index=True,
                key="deal_monthly_plan_editor_tickets",
            )
            plan_df["Tickets"] = pd.to_numeric(edited_plan["Tickets"], errors="coerce").fillna(0.0)
            plan_df["Avg Ticket"] = pd.to_numeric(edited_plan["Avg Ticket"], errors="coerce").fillna(0.0)
            plan_df["Revenue"] = plan_df["Tickets"] * plan_df["Avg Ticket"]

            annual_revenue = float(plan_df["Revenue"].sum())
            annual_tickets = float(plan_df["Tickets"].sum())
            avg_ticket = float(plan_df["Revenue"].sum() / max(plan_df["Tickets"].sum(), 1))
            st.metric("Year 1 Revenue from Monthly Plan", money(annual_revenue))

        st.session_state["deal_monthly_plan"] = plan_df

    if forecast_mode_internal == "flat":
        seasonality_mode_internal = "monthly_revenue"

    st.markdown('<div class="rc-gap-md"></div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3, gap="large")
    with c1:
        ramp_months = _make_number_input(
            "Ramp Months",
            "deal_ramp_months_input",
            int(_get_default("deal_ramp_months", "fm_ramp_months", 6)),
            step=1,
            min_value=1,
        )
    with c2:
        starting_cash = _make_number_input(
            "Starting Cash Buffer",
            "deal_starting_cash_input",
            float(_get_default("deal_starting_cash", "fm_starting_cash", 50000.0)),
            step=1000.0,
        )
    with c3:
        revenue_growth_pct = _make_number_input(
            "Revenue Growth % YoY",
            "deal_revenue_growth_pct_input",
            float(st.session_state.get("deal_revenue_growth_pct", 0.03)),
            step=0.01,
            min_value=0.0,
            max_value=1.0,
            fmt="%.2f",
        )

    return {
        "revenue_mode_internal": revenue_mode_internal,
        "forecast_mode_internal": forecast_mode_internal,
        "seasonality_mode_internal": seasonality_mode_internal,
        "annual_revenue": float(annual_revenue),
        "annual_tickets": float(annual_tickets),
        "avg_ticket": float(avg_ticket),
        "ramp_months": int(ramp_months),
        "starting_cash": float(starting_cash),
        "revenue_growth_pct": float(revenue_growth_pct),
    }


def _render_variable_expenses():
    render_section_intro(
        title="Variable expense assumptions",
        body="Set the core variable expense assumptions that should scale with revenue in the forecast.",
    )
    st.markdown('<div class="rc-gap-md"></div>', unsafe_allow_html=True)

    v1, v2, v3, v4, v5, v6 = st.columns(6, gap="medium")
    with v1:
        cogs_pct = _make_number_input(
            "COGS %",
            "deal_cogs_pct_input",
            float(_get_default("deal_cogs_pct", "fm_cogs_pct", 0.30)),
            step=0.01,
            min_value=0.0,
            max_value=1.0,
            fmt="%.2f",
        )
    with v2:
        royalty_pct = _make_number_input(
            "Royalty %",
            "deal_royalty_pct_input",
            float(_get_default("deal_royalty_pct", "fm_royalty_pct", 0.06)),
            step=0.01,
            min_value=0.0,
            max_value=1.0,
            fmt="%.2f",
        )
    with v3:
        marketing_pct = _make_number_input(
            "Marketing %",
            "deal_marketing_pct_input",
            float(_get_default("deal_marketing_pct", "fm_marketing_pct", 0.03)),
            step=0.01,
            min_value=0.0,
            max_value=1.0,
            fmt="%.2f",
        )
    with v4:
        merchant_pct = _make_number_input(
            "Merchant %",
            "deal_merchant_pct_input",
            float(st.session_state.get("deal_merchant_pct", st.session_state.get("merchant_pct", 2.8) / 100)),
            step=0.001,
            min_value=0.0,
            max_value=1.0,
            fmt="%.3f",
        )
    with v5:
        leakage_pct = _make_number_input(
            "Leakage %",
            "deal_leakage_pct_input",
            float(st.session_state.get("deal_leakage_pct", st.session_state.get("leakage_pct", 1.5) / 100)),
            step=0.001,
            min_value=0.0,
            max_value=1.0,
            fmt="%.3f",
        )
    with v6:
        labor_pct = _make_number_input(
            "Labor %",
            "deal_labor_pct_input",
            float(_get_default("deal_labor_pct", "fm_labor_pct", 0.30)),
            step=0.01,
            min_value=0.0,
            max_value=1.0,
            fmt="%.2f",
        )

    return {
        "cogs_pct": float(cogs_pct),
        "royalty_pct": float(royalty_pct),
        "marketing_pct": float(marketing_pct),
        "merchant_pct": float(merchant_pct),
        "leakage_pct": float(leakage_pct),
        "labor_pct": float(labor_pct),
    }


def _render_fixed_costs():
    render_section_intro(
        title="Occupancy, utilities, and fixed costs",
        body="Use the current workspace selections where available, then refine the monthly fixed-cost structure for a more realistic P&L.",
    )
    st.markdown('<div class="rc-gap-md"></div>', unsafe_allow_html=True)

    workspace_rent = _safe_float(st.session_state.get("selected_rent", 0.0))
    workspace_nnn = _safe_float(st.session_state.get("selected_nnn", 0.0))

    o1, o2, o3, o4 = st.columns(4, gap="medium")
    with o1:
        base_rent = _make_number_input(
            "Base Rent",
            "deal_base_rent_input",
            float(st.session_state.get("deal_base_rent", workspace_rent if workspace_rent > 0 else st.session_state.get("base_rent", 4500.0))),
            step=100.0,
        )
    with o2:
        cam = _make_number_input(
            "CAM / NNN",
            "deal_cam_input",
            float(st.session_state.get("deal_cam", workspace_nnn if workspace_nnn > 0 else st.session_state.get("cam", 500.0))),
            step=50.0,
        )
    with o3:
        electric = _make_number_input("Electric", "deal_electric_input", float(st.session_state.get("deal_electric", st.session_state.get("electric", 500.0))), step=25.0)
    with o4:
        gas = _make_number_input("Gas", "deal_gas_input", float(st.session_state.get("deal_gas", st.session_state.get("gas", 150.0))), step=25.0)

    o5, o6, o7, o8 = st.columns(4, gap="medium")
    with o5:
        water = _make_number_input("Water", "deal_water_input", float(st.session_state.get("deal_water", st.session_state.get("water", 100.0))), step=10.0)
    with o6:
        sewer = _make_number_input("Sewer", "deal_sewer_input", float(st.session_state.get("deal_sewer", st.session_state.get("sewer", 75.0))), step=10.0)
    with o7:
        trash = _make_number_input("Trash", "deal_trash_input", float(st.session_state.get("deal_trash", st.session_state.get("trash", 100.0))), step=10.0)
    with o8:
        internet = _make_number_input("Internet", "deal_internet_input", float(st.session_state.get("deal_internet", st.session_state.get("internet", 120.0))), step=10.0)

    o9, o10, o11, o12 = st.columns(4, gap="medium")
    with o9:
        phone = _make_number_input("Phone", "deal_phone_input", float(st.session_state.get("deal_phone", st.session_state.get("phone", 80.0))), step=10.0)
    with o10:
        tech = _make_number_input("Tech / POS", "deal_tech_input", float(st.session_state.get("deal_tech", st.session_state.get("tech", 650.0))), step=25.0)
    with o11:
        repairs = _make_number_input("Repairs", "deal_repairs_input", float(st.session_state.get("deal_repairs", st.session_state.get("repairs", 500.0))), step=25.0)
    with o12:
        admin_misc = _make_number_input("Admin / Misc", "deal_admin_misc_input", float(st.session_state.get("deal_admin_misc", st.session_state.get("admin_misc", 500.0))), step=25.0)

    o13, o14, o15 = st.columns(3, gap="medium")
    with o13:
        workers_comp = _make_number_input("Workers Comp", "deal_workers_comp_input", float(st.session_state.get("deal_workers_comp", st.session_state.get("workers_comp", 250.0))), step=25.0)
    with o14:
        property_ins = _make_number_input("Property Insurance", "deal_property_ins_input", float(st.session_state.get("deal_property_ins", st.session_state.get("property_ins", 350.0))), step=25.0)
    with o15:
        owner_comp = _make_number_input("Owner Comp", "deal_owner_comp_input", float(st.session_state.get("deal_owner_comp", st.session_state.get("owner_comp", 0.0))), step=100.0)

    occupancy = base_rent + cam
    utilities = electric + gas + water + sewer + trash + internet + phone
    insurance = workers_comp + property_ins
    other_fixed = utilities + insurance + tech + repairs + admin_misc + owner_comp

    st.markdown('<div class="rc-gap-md"></div>', unsafe_allow_html=True)

    s1, s2, s3, s4 = st.columns(4, gap="medium")
    with s1:
        render_card(label="Monthly summary", title=money(occupancy), body="Occupancy cost including base rent and CAM / NNN.")
    with s2:
        render_card(label="Utilities", title=money(utilities), body="Combined monthly utilities flowing into the model.")
    with s3:
        render_card(label="Insurance", title=money(insurance), body="Workers comp and property insurance combined.")
    with s4:
        render_card(label="Other fixed", title=money(other_fixed), body="Tech, repairs, admin, and owner comp combined.")

    return {
        "base_rent": float(base_rent),
        "cam": float(cam),
        "electric": float(electric),
        "gas": float(gas),
        "water": float(water),
        "sewer": float(sewer),
        "trash": float(trash),
        "internet": float(internet),
        "phone": float(phone),
        "workers_comp": float(workers_comp),
        "property_ins": float(property_ins),
        "tech": float(tech),
        "repairs": float(repairs),
        "admin_misc": float(admin_misc),
        "owner_comp": float(owner_comp),
    }


def _render_growth_inputs():
    render_section_intro(
        title="Year-over-year growth by bucket",
        body="Set how major line items should grow after Year 1 so the 3-year forecast reflects a more realistic operating path.",
    )
    st.markdown('<div class="rc-gap-md"></div>', unsafe_allow_html=True)

    g1, g2, g3, g4 = st.columns(4, gap="medium")
    with g1:
        cogs_growth_pct = _make_number_input("COGS Growth %", "deal_cogs_growth_pct_input", float(st.session_state.get("deal_cogs_growth_pct", 0.03)), step=0.01, min_value=0.0, max_value=1.0, fmt="%.2f")
    with g2:
        labor_growth_pct = _make_number_input("Labor Growth %", "deal_labor_growth_pct_input", float(st.session_state.get("deal_labor_growth_pct", 0.03)), step=0.01, min_value=0.0, max_value=1.0, fmt="%.2f")
    with g3:
        royalty_growth_pct = _make_number_input("Royalty Growth %", "deal_royalty_growth_pct_input", float(st.session_state.get("deal_royalty_growth_pct", 0.03)), step=0.01, min_value=0.0, max_value=1.0, fmt="%.2f")
    with g4:
        marketing_growth_pct = _make_number_input("Marketing Growth %", "deal_marketing_growth_pct_input", float(st.session_state.get("deal_marketing_growth_pct", 0.03)), step=0.01, min_value=0.0, max_value=1.0, fmt="%.2f")

    g5, g6, g7, g8 = st.columns(4, gap="medium")
    with g5:
        merchant_growth_pct = _make_number_input("Merchant Growth %", "deal_merchant_growth_pct_input", float(st.session_state.get("deal_merchant_growth_pct", 0.03)), step=0.01, min_value=0.0, max_value=1.0, fmt="%.2f")
    with g6:
        leakage_growth_pct = _make_number_input("Leakage Growth %", "deal_leakage_growth_pct_input", float(st.session_state.get("deal_leakage_growth_pct", 0.03)), step=0.01, min_value=0.0, max_value=1.0, fmt="%.2f")
    with g7:
        occupancy_growth_pct = _make_number_input("Occupancy Growth %", "deal_occupancy_growth_pct_input", float(st.session_state.get("deal_occupancy_growth_pct", 0.03)), step=0.01, min_value=0.0, max_value=1.0, fmt="%.2f")
    with g8:
        utilities_growth_pct = _make_number_input("Utilities Growth %", "deal_utilities_growth_pct_input", float(st.session_state.get("deal_utilities_growth_pct", 0.03)), step=0.01, min_value=0.0, max_value=1.0, fmt="%.2f")

    g9, g10, g11, g12 = st.columns(4, gap="medium")
    with g9:
        insurance_growth_pct = _make_number_input("Insurance Growth %", "deal_insurance_growth_pct_input", float(st.session_state.get("deal_insurance_growth_pct", 0.03)), step=0.01, min_value=0.0, max_value=1.0, fmt="%.2f")
    with g10:
        tech_growth_pct = _make_number_input("Tech Growth %", "deal_tech_growth_pct_input", float(st.session_state.get("deal_tech_growth_pct", 0.03)), step=0.01, min_value=0.0, max_value=1.0, fmt="%.2f")
    with g11:
        repairs_growth_pct = _make_number_input("Repairs Growth %", "deal_repairs_growth_pct_input", float(st.session_state.get("deal_repairs_growth_pct", 0.03)), step=0.01, min_value=0.0, max_value=1.0, fmt="%.2f")
    with g12:
        admin_growth_pct = _make_number_input("Admin Growth %", "deal_admin_growth_pct_input", float(st.session_state.get("deal_admin_growth_pct", 0.03)), step=0.01, min_value=0.0, max_value=1.0, fmt="%.2f")

    owner_comp_growth_pct = _make_number_input(
        "Owner Comp Growth %",
        "deal_owner_comp_growth_pct_input",
        float(st.session_state.get("deal_owner_comp_growth_pct", 0.03)),
        step=0.01,
        min_value=0.0,
        max_value=1.0,
        fmt="%.2f",
    )

    return {
        "cogs_growth_pct": float(cogs_growth_pct),
        "labor_growth_pct": float(labor_growth_pct),
        "royalty_growth_pct": float(royalty_growth_pct),
        "marketing_growth_pct": float(marketing_growth_pct),
        "merchant_growth_pct": float(merchant_growth_pct),
        "leakage_growth_pct": float(leakage_growth_pct),
        "occupancy_growth_pct": float(occupancy_growth_pct),
        "utilities_growth_pct": float(utilities_growth_pct),
        "insurance_growth_pct": float(insurance_growth_pct),
        "tech_growth_pct": float(tech_growth_pct),
        "repairs_growth_pct": float(repairs_growth_pct),
        "admin_growth_pct": float(admin_growth_pct),
        "owner_comp_growth_pct": float(owner_comp_growth_pct),
    }


def _persist_inputs(inputs: dict) -> None:
    for key, value in inputs.items():
        if key != "monthly_plan":
            st.session_state[f"deal_{key}"] = value


def _build_and_render_results(inputs: dict, su: dict) -> None:
    df = build_3year_forecast(inputs)
    pnl = build_pnl(df)
    monthly_pnls = build_monthly_pnl_views(df)
    bs = build_balance_sheet_summary(df, inputs, su)
    metrics = calculate_metrics(df, inputs, su)

    df_down, metrics_down = run_downside_case(inputs, su)
    breakpoints = what_breaks_first(metrics, metrics_down, su, inputs)

    st.session_state["deal_model_df"] = df
    st.session_state["deal_model_pnl"] = pnl
    st.session_state["deal_model_monthly_pnls"] = monthly_pnls
    st.session_state["deal_model_bs"] = bs
    st.session_state["deal_model_downside_df"] = df_down
    st.session_state["deal_model_breakpoints"] = breakpoints

    st.session_state["deal_model_roi"] = metrics["roi"]
    st.session_state["deal_model_payback"] = metrics["payback_month"]
    st.session_state["deal_model_break_even_month"] = metrics["break_even_month"]
    st.session_state["deal_model_lowest_cash"] = metrics["lowest_cash"]
    st.session_state["deal_model_lowest_cash_month"] = metrics["lowest_cash_month"]
    st.session_state["deal_model_dscr"] = metrics["dscr"]
    st.session_state["deal_model_equity_at_risk"] = metrics["equity_at_risk"]
    st.session_state["deal_model_stabilized_monthly_net"] = metrics["stabilized_monthly_net"]

    st.session_state["deal_model_downside_roi"] = metrics_down["roi"]
    st.session_state["deal_model_downside_payback"] = metrics_down["payback_month"]
    st.session_state["deal_model_downside_break_even_month"] = metrics_down["break_even_month"]
    st.session_state["deal_model_downside_lowest_cash"] = metrics_down["lowest_cash"]

    if metrics["lowest_cash"] < 0 or metrics["dscr"] < 1.0 or float(su["gap"]) > 0:
        st.session_state["financial_verdict"] = "High Financial Risk"
    elif metrics["dscr"] < 1.25 or metrics_down["lowest_cash"] < 0:
        st.session_state["financial_verdict"] = "Proceed with Caution"
    else:
        st.session_state["financial_verdict"] = "Proceed to Negotiation / Financing"

    st.markdown('<div class="rc-gap-lg"></div>', unsafe_allow_html=True)

    render_section_intro(
        title="Key metrics",
        body="Use these outputs to judge whether the deal can produce an acceptable return, survive early pressure, and remain fundable.",
    )
    st.markdown('<div class="rc-gap-md"></div>', unsafe_allow_html=True)

    m1, m2, m3, m4 = st.columns(4, gap="medium")
    with m1:
        render_card(label="ROI", title=pct(metrics["roi"]), body="Projected return on invested equity.")
    with m2:
        render_card(label="Payback", title=f"{metrics['payback_month']} mo" if metrics["payback_month"] else "No payback", body="Estimated payback period based on the model.")
    with m3:
        render_card(label="Break-even", title=f"Month {metrics['break_even_month']}" if metrics["break_even_month"] else "Not reached", body="First month cumulative cash turns positive.")
    with m4:
        render_card(label="Lowest cash", title=money(metrics["lowest_cash"]), body="Lowest ending cash balance in the base case.")

    st.markdown('<div class="rc-gap-md"></div>', unsafe_allow_html=True)

    m5, m6, m7, m8 = st.columns(4, gap="medium")
    with m5:
        render_card(label="Lowest cash month", title=str(metrics["lowest_cash_month"]) if metrics["lowest_cash_month"] else "N/A", body="Month where liquidity is most constrained.")
    with m6:
        render_card(label="Equity at risk", title=money(metrics["equity_at_risk"]), body="Estimated equity exposure in the structure.")
    with m7:
        render_card(label="DSCR", title=f"{metrics['dscr']:.2f}x", body="Debt service coverage under the base case.")
    with m8:
        render_card(label="Verdict", title=st.session_state["financial_verdict"], body="Directional financial read based on the current model.")

    st.markdown('<div class="rc-gap-lg"></div>', unsafe_allow_html=True)

    render_section_intro(
        title="What breaks first",
        body="These are the first places the model becomes fragile under pressure.",
    )
    st.markdown('<div class="rc-gap-sm"></div>', unsafe_allow_html=True)
    for item in breakpoints:
        st.write(f"- {item}")

    st.markdown('<div class="rc-gap-lg"></div>', unsafe_allow_html=True)

    render_section_intro(
        title="Downside case",
        body="Compare the base case to a stressed case so the model is not dependent on everything going right.",
    )
    st.markdown('<div class="rc-gap-md"></div>', unsafe_allow_html=True)

    d1, d2, d3, d4 = st.columns(4, gap="medium")
    with d1:
        render_card(label="Downside ROI", title=pct(metrics_down["roi"]), body="Return under the downside case.")
    with d2:
        render_card(label="Downside break-even", title=f"Month {metrics_down['break_even_month']}" if metrics_down["break_even_month"] else "Not reached", body="Break-even timing under stress.")
    with d3:
        render_card(label="Downside lowest cash", title=money(metrics_down["lowest_cash"]), body="Liquidity floor under the downside case.")
    with d4:
        render_card(label="Downside payback", title=f"{metrics_down['payback_month']} mo" if metrics_down["payback_month"] else "No payback", body="Payback timing under stress.")

    st.markdown('<div class="rc-gap-lg"></div>', unsafe_allow_html=True)

    render_section_intro(
        title="Forecast outputs",
        body="These views preserve the detailed outputs so you can review annual performance, monthly cash movement, and simplified balance-sheet posture.",
    )
    st.markdown('<div class="rc-gap-md"></div>', unsafe_allow_html=True)

    st.markdown("### 3-Year Annual Summary")
    st.dataframe(pnl, use_container_width=True, hide_index=True)

    st.markdown('<div class="rc-gap-md"></div>', unsafe_allow_html=True)
    st.markdown("### Year 1 Monthly P&L")
    st.dataframe(monthly_pnls[1], use_container_width=True, hide_index=True)

    st.markdown('<div class="rc-gap-md"></div>', unsafe_allow_html=True)
    st.markdown("### Year 2 Monthly P&L")
    st.dataframe(monthly_pnls[2], use_container_width=True, hide_index=True)

    st.markdown('<div class="rc-gap-md"></div>', unsafe_allow_html=True)
    st.markdown("### Year 3 Monthly P&L")
    st.dataframe(monthly_pnls[3], use_container_width=True, hide_index=True)

    st.markdown('<div class="rc-gap-md"></div>', unsafe_allow_html=True)
    st.markdown("### Simplified Balance Sheet View")
    st.dataframe(bs, use_container_width=True, hide_index=True)

    st.markdown('<div class="rc-gap-md"></div>', unsafe_allow_html=True)
    st.markdown("### 3-Year Cash Curve")
    st.line_chart(df.set_index("Month Index")["Ending Cash"])

    st.markdown('<div class="rc-gap-md"></div>', unsafe_allow_html=True)
    st.markdown("### Monthly Forecast Detail")
    st.dataframe(df, use_container_width=True, hide_index=True)


def render_deal_model() -> None:
    _init_monthly_plan()
    su = calc_sources_uses(st.session_state)

    open_shell()

    render_page_header(
        eyebrow="Execution — Deal Model",
        title="Estimate what the deal can really produce.",
        subtitle=(
            "Use this model to estimate a truer P&L, review forecast performance, and test whether the economics still work "
            "under more realistic operating assumptions."
        ),
        wide=True,
    )

    st.markdown('<div class="rc-gap-lg"></div>', unsafe_allow_html=True)

    _render_workspace_metrics(su)

    st.markdown('<div class="rc-gap-lg"></div>', unsafe_allow_html=True)

    revenue_inputs = _render_revenue_setup()

    st.markdown('<div class="rc-gap-lg"></div>', unsafe_allow_html=True)

    variable_inputs = _render_variable_expenses()

    st.markdown('<div class="rc-gap-lg"></div>', unsafe_allow_html=True)

    fixed_cost_inputs = _render_fixed_costs()

    st.markdown('<div class="rc-gap-lg"></div>', unsafe_allow_html=True)

    growth_inputs = _render_growth_inputs()

    inputs = {
        "revenue_mode": revenue_inputs["revenue_mode_internal"],
        "forecast_mode": revenue_inputs["forecast_mode_internal"],
        "seasonality_mode": revenue_inputs["seasonality_mode_internal"],
        "annual_revenue": revenue_inputs["annual_revenue"],
        "annual_tickets": revenue_inputs["annual_tickets"],
        "avg_ticket": revenue_inputs["avg_ticket"],
        "monthly_plan": st.session_state.get("deal_monthly_plan").copy(),
        "ramp_months": revenue_inputs["ramp_months"],
        "starting_cash": revenue_inputs["starting_cash"],
        "revenue_growth_pct": revenue_inputs["revenue_growth_pct"],
        "debt_payment": float(su["debt_payment"]),
        **variable_inputs,
        **fixed_cost_inputs,
        **growth_inputs,
    }

    _persist_inputs(inputs)

    st.markdown('<div class="rc-gap-lg"></div>', unsafe_allow_html=True)

    if st.button(
        "Build 3-Year Deal Model",
        key="build_deal_model",
        use_container_width=True,
        type="primary",
    ):
        _build_and_render_results(inputs, su)

    st.markdown('<div class="rc-gap-md"></div>', unsafe_allow_html=True)

    if st.button(
        "Open Execution Report",
        key="deal_model_open_execution_report",
        use_container_width=True,
    ):
        st.session_state["current_page"] = "Execution Report"
        st.rerun()

    close_shell()
