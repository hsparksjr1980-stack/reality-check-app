import streamlit as st
import pandas as pd

from deal_workspace_logic import calc_sources_uses
from deal_model_logic import (
    MONTH_LABELS,
    build_3year_forecast,
    build_pnl,
    build_monthly_pnl_views,
    build_balance_sheet_summary,
    calculate_metrics,
    run_downside_case,
    what_breaks_first,
)


def pct(x):
    return f"{x * 100:,.1f}%"


def money(x):
    return f"${x:,.0f}"


def _safe_float(value, fallback=0.0):
    try:
        if value is None or value == "":
            return float(fallback)
        return float(value)
    except (TypeError, ValueError):
        return float(fallback)


def _get_default(session_key, fm_key, fallback):
    return st.session_state.get(session_key, st.session_state.get(fm_key, fallback))


def _init_monthly_plan():
    if "deal_monthly_plan" not in st.session_state:
        st.session_state["deal_monthly_plan"] = pd.DataFrame(
            {
                "Month": MONTH_LABELS,
                "Revenue": [0.0] * 12,
                "Tickets": [0.0] * 12,
                "Avg Ticket": [0.0] * 12,
            }
        )


def _make_number_input(label, key, value, step=100.0, min_value=0.0, max_value=None, fmt=None):
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


def render_deal_model():
    st.header("Deal Model (Pro)")
    st.caption(
        "Build a 3-year deal-level P&L using either annual revenue or tickets, "
        "with optional monthly seasonality and per-bucket YoY growth."
    )

    _init_monthly_plan()
    su = calc_sources_uses(st.session_state)

    st.markdown("### Live Inputs From Deal Workspace")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Total Uses", money(su["total_uses"]))
    with c2:
        st.metric("Total Sources", money(su["total_sources"]))
    with c3:
        st.metric("Funding Gap", money(su["gap"]))
    with c4:
        st.metric("Monthly Debt Payment", money(su["debt_payment"]))

    # -----------------------------
    # Revenue Setup
    # -----------------------------
    st.markdown("### Revenue Setup")

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

    if forecast_mode_internal == "flat":
        if revenue_mode_internal == "annual_revenue":
            annual_revenue = _make_number_input(
                "Annual Revenue",
                "deal_annual_revenue_input",
                float(_get_default("deal_annual_revenue", "fm_target_monthly_revenue", 120000.0) * 12),
                step=10000.0,
            )
            annual_tickets = 0.0
            avg_ticket = 0.0
            implied_monthly_revenue = annual_revenue / 12

            m1, m2 = st.columns(2)
            with m1:
                st.metric("Monthly Revenue", money(implied_monthly_revenue))
            with m2:
                st.metric("Annual Revenue", money(annual_revenue))

        else:
            col1, col2 = st.columns(2)
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

            m1, m2 = st.columns(2)
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
            annual_tickets = 0.0
            avg_ticket = 0.0
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

    ramp_months = _make_number_input(
        "Ramp Months",
        "deal_ramp_months_input",
        int(_get_default("deal_ramp_months", "fm_ramp_months", 6)),
        step=1,
        min_value=1,
    )

    starting_cash = _make_number_input(
        "Starting Cash Buffer",
        "deal_starting_cash_input",
        float(_get_default("deal_starting_cash", "fm_starting_cash", max(su["working_cap"], 50000.0))),
        step=1000.0,
    )

    revenue_growth_pct = _make_number_input(
        "Revenue Growth % YoY",
        "deal_revenue_growth_pct_input",
        float(st.session_state.get("deal_revenue_growth_pct", 0.03)),
        step=0.01,
        min_value=0.0,
        max_value=1.0,
        fmt="%.2f",
    )

    # -----------------------------
    # Variable Expense Assumptions
    # -----------------------------
    st.markdown("### Variable Expense Assumptions")

    v1, v2, v3, v4, v5, v6 = st.columns(6)
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

    # -----------------------------
    # Occupancy / Fixed Costs
    # -----------------------------
    st.markdown("### Occupancy, Utilities & Fixed Costs")

    workspace_rent = _safe_float(st.session_state.get("selected_rent", 0.0))
    workspace_nnn = _safe_float(st.session_state.get("selected_nnn", 0.0))

    o1, o2, o3, o4 = st.columns(4)
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

    o5, o6, o7, o8 = st.columns(4)
    with o5:
        water = _make_number_input("Water", "deal_water_input", float(st.session_state.get("deal_water", st.session_state.get("water", 100.0))), step=10.0)
    with o6:
        sewer = _make_number_input("Sewer", "deal_sewer_input", float(st.session_state.get("deal_sewer", st.session_state.get("sewer", 75.0))), step=10.0)
    with o7:
        trash = _make_number_input("Trash", "deal_trash_input", float(st.session_state.get("deal_trash", st.session_state.get("trash", 100.0))), step=10.0)
    with o8:
        internet = _make_number_input("Internet", "deal_internet_input", float(st.session_state.get("deal_internet", st.session_state.get("internet", 120.0))), step=10.0)

    o9, o10, o11, o12 = st.columns(4)
    with o9:
        phone = _make_number_input("Phone", "deal_phone_input", float(st.session_state.get("deal_phone", st.session_state.get("phone", 80.0))), step=10.0)
    with o10:
        tech = _make_number_input("Tech / POS", "deal_tech_input", float(st.session_state.get("deal_tech", st.session_state.get("tech", 650.0))), step=25.0)
    with o11:
        repairs = _make_number_input("Repairs", "deal_repairs_input", float(st.session_state.get("deal_repairs", st.session_state.get("repairs", 500.0))), step=25.0)
    with o12:
        admin_misc = _make_number_input("Admin / Misc", "deal_admin_misc_input", float(st.session_state.get("deal_admin_misc", st.session_state.get("admin_misc", 500.0))), step=25.0)

    o13, o14, o15 = st.columns(3)
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

    s1, s2, s3, s4 = st.columns(4)
    with s1:
        st.metric("Occupancy", money(occupancy))
    with s2:
        st.metric("Utilities", money(utilities))
    with s3:
        st.metric("Insurance", money(insurance))
    with s4:
        st.metric("Other Fixed", money(other_fixed))

    # -----------------------------
    # YoY Growth
    # -----------------------------
    st.markdown("### YoY Growth by Bucket")

    g1, g2, g3, g4 = st.columns(4)
    with g1:
        cogs_growth_pct = _make_number_input("COGS Growth %", "deal_cogs_growth_pct_input", float(st.session_state.get("deal_cogs_growth_pct", 0.03)), step=0.01, min_value=0.0, max_value=1.0, fmt="%.2f")
    with g2:
        labor_growth_pct = _make_number_input("Labor Growth %", "deal_labor_growth_pct_input", float(st.session_state.get("deal_labor_growth_pct", 0.03)), step=0.01, min_value=0.0, max_value=1.0, fmt="%.2f")
    with g3:
        royalty_growth_pct = _make_number_input("Royalty Growth %", "deal_royalty_growth_pct_input", float(st.session_state.get("deal_royalty_growth_pct", 0.03)), step=0.01, min_value=0.0, max_value=1.0, fmt="%.2f")
    with g4:
        marketing_growth_pct = _make_number_input("Marketing Growth %", "deal_marketing_growth_pct_input", float(st.session_state.get("deal_marketing_growth_pct", 0.03)), step=0.01, min_value=0.0, max_value=1.0, fmt="%.2f")

    g5, g6, g7, g8 = st.columns(4)
    with g5:
        merchant_growth_pct = _make_number_input("Merchant Growth %", "deal_merchant_growth_pct_input", float(st.session_state.get("deal_merchant_growth_pct", 0.03)), step=0.01, min_value=0.0, max_value=1.0, fmt="%.2f")
    with g6:
        leakage_growth_pct = _make_number_input("Leakage Growth %", "deal_leakage_growth_pct_input", float(st.session_state.get("deal_leakage_growth_pct", 0.03)), step=0.01, min_value=0.0, max_value=1.0, fmt="%.2f")
    with g7:
        occupancy_growth_pct = _make_number_input("Occupancy Growth %", "deal_occupancy_growth_pct_input", float(st.session_state.get("deal_occupancy_growth_pct", 0.03)), step=0.01, min_value=0.0, max_value=1.0, fmt="%.2f")
    with g8:
        utilities_growth_pct = _make_number_input("Utilities Growth %", "deal_utilities_growth_pct_input", float(st.session_state.get("deal_utilities_growth_pct", 0.03)), step=0.01, min_value=0.0, max_value=1.0, fmt="%.2f")

    g9, g10, g11, g12 = st.columns(4)
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

    inputs = {
        "revenue_mode": revenue_mode_internal,
        "forecast_mode": forecast_mode_internal,
        "seasonality_mode": seasonality_mode_internal,
        "annual_revenue": float(annual_revenue),
        "annual_tickets": float(annual_tickets),
        "avg_ticket": float(avg_ticket),
        "monthly_plan": st.session_state.get("deal_monthly_plan").copy(),
        "ramp_months": int(ramp_months),
        "starting_cash": float(starting_cash),
        "revenue_growth_pct": float(revenue_growth_pct),
        "cogs_pct": float(cogs_pct),
        "labor_pct": float(labor_pct),
        "royalty_pct": float(royalty_pct),
        "marketing_pct": float(marketing_pct),
        "merchant_pct": float(merchant_pct),
        "leakage_pct": float(leakage_pct),
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
        "debt_payment": float(su["debt_payment"]),
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

    # persist
    for k, v in inputs.items():
        if k != "monthly_plan":
            st.session_state[f"deal_{k}"] = v

    if st.button("Build 3-Year Deal Model", type="primary"):
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

        st.markdown("---")
        st.subheader("Key Metrics")

        m1, m2, m3, m4 = st.columns(4)
        with m1:
            st.metric("ROI", pct(metrics["roi"]))
        with m2:
            st.metric("Payback", f"{metrics['payback_month']} mo" if metrics["payback_month"] else "No payback")
        with m3:
            st.metric("Break-even", f"Month {metrics['break_even_month']}" if metrics["break_even_month"] else "Not reached")
        with m4:
            st.metric("Lowest Cash", money(metrics["lowest_cash"]))

        m5, m6, m7, m8 = st.columns(4)
        with m5:
            st.metric("Lowest Cash Month", str(metrics["lowest_cash_month"]) if metrics["lowest_cash_month"] else "N/A")
        with m6:
            st.metric("Equity at Risk", money(metrics["equity_at_risk"]))
        with m7:
            st.metric("DSCR", f"{metrics['dscr']:.2f}x")
        with m8:
            st.metric("Financial Verdict", st.session_state["financial_verdict"])

        st.markdown("### What Breaks First")
        for item in breakpoints:
            st.write(f"- {item}")

        st.markdown("### Downside Case")
        d1, d2, d3, d4 = st.columns(4)
        with d1:
            st.metric("Downside ROI", pct(metrics_down["roi"]))
        with d2:
            st.metric("Downside Break-even", f"Month {metrics_down['break_even_month']}" if metrics_down["break_even_month"] else "Not reached")
        with d3:
            st.metric("Downside Lowest Cash", money(metrics_down["lowest_cash"]))
        with d4:
            st.metric("Downside Payback", f"{metrics_down['payback_month']} mo" if metrics_down["payback_month"] else "No payback")

        st.markdown("### 3-Year Annual Summary")
        st.dataframe(pnl, use_container_width=True, hide_index=True)

        st.markdown("### Year 1 Monthly P&L")
        st.dataframe(monthly_pnls[1], use_container_width=True, hide_index=True)

        st.markdown("### Year 2 Monthly P&L")
        st.dataframe(monthly_pnls[2], use_container_width=True, hide_index=True)

        st.markdown("### Year 3 Monthly P&L")
        st.dataframe(monthly_pnls[3], use_container_width=True, hide_index=True)

        st.markdown("### Simplified Balance Sheet View")
        st.dataframe(bs, use_container_width=True, hide_index=True)

        st.markdown("### 3-Year Cash Curve")
        st.line_chart(df.set_index("Month Index")["Ending Cash"])

        st.markdown("### Monthly Forecast Detail")
        st.dataframe(df, use_container_width=True, hide_index=True)
