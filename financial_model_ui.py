
import streamlit as st
from pathlib import Path
import base64

st.set_page_config(page_title="Financial Model", layout="wide")

# -----------------------------
# Helpers
# -----------------------------
def money(x: float) -> str:
    return f"${x:,.0f}"

def pct(x: float) -> str:
    return f"{x*100:,.1f}%"

def safe_div(a: float, b: float) -> float:
    return a / b if b not in (0, None) else 0.0

def pmt(principal: float, annual_rate: float, years: float) -> float:
    months = max(int(years * 12), 1)
    if principal <= 0:
        return 0.0
    if annual_rate <= 0:
        return principal / months
    r = annual_rate / 12
    return principal * (r * (1 + r) ** months) / ((1 + r) ** months - 1)

def system_position_label(position_raw: float) -> str:
    if position_raw < 0:
        return "Below system range"
    if position_raw < 0.25:
        return "Bottom quartile"
    if position_raw < 0.5:
        return "Below median"
    if position_raw < 0.75:
        return "Above median"
    if position_raw <= 1.0:
        return "Top quartile"
    return "Aggressive"

def save_section(section_name: str, values: dict):
    for k, v in values.items():
        st.session_state[k] = v
    st.session_state[f"{section_name}_done"] = True

def section_done(name: str) -> bool:
    return bool(st.session_state.get(f"{name}_done", False))

def done_icon(name: str) -> str:
    return "✅" if section_done(name) else "⬜"

# -----------------------------
# Defaults
# -----------------------------
defaults = {
    "fdd_low": 400000.0,
    "fdd_high": 600000.0,
    "fdd_franchise_fee": 40000.0,
    "fdd_revenue": 500000.0,
    "fdd_cogs_pct": 28.0,
    "fdd_labor_pct": 25.0,
    "fdd_occupancy_pct": 9.0,
    "fdd_royalty_pct": 6.0,
    "fdd_marketing_pct": 2.0,
    "fdd_other_pct": 12.0,
    "dist_mode": "Estimate from average (recommended)",
    "units_reported": 100,
    "avg_rev": 500000.0,
    "median_rev": 470000.0,
    "top25": 625000.0,
    "bottom25": 375000.0,
    "loan_mode": "% of total project",
    "debt_pct": 65.0,
    "fixed_loan_amount": 325000.0,
    "rate": 8.0,
    "term_years": 10.0,
    "extra_liquidity": 0.0,
    "orig_fee_pct": 1.5,
    "closing_costs": 8000.0,
    "guarantee_fees": 9000.0,
    "schedule": "7 days/week",
    "days_custom": 365,
    "square_feet": 1800,
    "format_type": "Inline",
    "local_cost_env": "Average",
    "opening_risk": "Minor delay",
    "ramp_speed": "Normal (5 months)",
    "user_buildout": 300000.0,
    "user_equipment": 120000.0,
    "user_soft": 30000.0,
    "user_opening": 25000.0,
    "user_working_cap": 100000.0,
    "startup_training_days": 10.0,
    "startup_staffing_hours_per_day": 8.0,
    "startup_avg_staff_per_hour": 3.0,
    "startup_avg_cost_per_hour": 17.0,
    "unexpected_cost_pct": 10.0,
    "estimate_completeness": "Partial quotes",
    "avg_ticket": 8.75,
    "tx_per_day": 156.0,
    "base_rent": 4500.0,
    "cam": 500.0,
    "electric": 500.0,
    "gas": 150.0,
    "water": 100.0,
    "sewer": 75.0,
    "trash": 100.0,
    "internet": 120.0,
    "phone": 80.0,
    "wage": 17.0,
    "staff_per_hour": 2.5,
    "hours_open_daily": 12.0,
    "owner_comp": 0.0,
    "workers_comp": 250.0,
    "property_ins": 350.0,
    "tech": 650.0,
    "repairs": 500.0,
    "admin_misc": 500.0,
    "actual_cogs_pct": 32.0,
    "payroll_tax_pct": 10.0,
    "actual_royalty_pct": 6.0,
    "actual_marketing_pct": 2.0,
    "merchant_pct": 2.8,
    "leakage_pct": 1.5,
}

for k, v in defaults.items():
    st.session_state.setdefault(k, v)

# -----------------------------
# Title / progress
# -----------------------------
st.title("Financial Model")
st.caption("Step through each section, submit it, then review reality checks and final results together.")

progress_cols = st.columns(7)
progress_items = [
    ("fdd_investment", "FDD Investment"),
    ("fdd_pl", "FDD System P&L"),
    ("fdd_distribution", "Revenue Distribution"),
    ("financing", "Financing"),
    ("deal_setup", "Deal Setup"),
    ("startup", "Startup Assumptions"),
    ("operating", "Operating Assumptions"),
]
for col, (key, label) in zip(progress_cols, progress_items):
    with col:
        st.markdown(f"**{done_icon(key)} {label}**")

# -----------------------------
# 1) FDD Investment Range
# -----------------------------
with st.expander("1) FDD Investment Range", expanded=not section_done("fdd_investment")):
    st.caption("What the franchise says it costs to open.")
    with st.form("form_fdd_investment"):
        c1, c2, c3 = st.columns(3)
        with c1:
            fdd_low = st.number_input("Low investment", min_value=0.0, value=st.session_state["fdd_low"], step=1000.0)
        with c2:
            fdd_high = st.number_input("High investment", min_value=0.0, value=st.session_state["fdd_high"], step=1000.0)
        with c3:
            fdd_franchise_fee = st.number_input("Franchise fee (if separately listed)", min_value=0.0, value=st.session_state["fdd_franchise_fee"], step=500.0)
        submit_1 = st.form_submit_button("Save FDD Investment Range", use_container_width=True)
        if submit_1:
            save_section("fdd_investment", {
                "fdd_low": fdd_low,
                "fdd_high": fdd_high,
                "fdd_franchise_fee": fdd_franchise_fee
            })
            st.success("FDD Investment Range saved.")
    if section_done("fdd_investment"):
        fdd_mid = (st.session_state["fdd_low"] + st.session_state["fdd_high"]) / 2
        s1, s2, s3 = st.columns(3)
        s1.metric("Midpoint investment", money(fdd_mid))
        s2.metric("Range width", pct(safe_div(st.session_state["fdd_high"] - st.session_state["fdd_low"], max(fdd_mid, 1))))
        s3.metric("Franchise fee", money(st.session_state["fdd_franchise_fee"]))

# -----------------------------
# 2) FDD System P&L
# -----------------------------
with st.expander("2) FDD System P&L", expanded=section_done("fdd_investment") and not section_done("fdd_pl")):
    st.caption("What a typical store makes and spends, based on the FDD.")
    with st.form("form_fdd_pl"):
        p1, p2, p3, p4 = st.columns(4)
        with p1:
            fdd_revenue = st.number_input("FDD revenue used in P&L", min_value=0.0, value=st.session_state["fdd_revenue"], step=1000.0)
        with p2:
            fdd_cogs_pct = st.number_input("COGS %", min_value=0.0, max_value=100.0, value=st.session_state["fdd_cogs_pct"], step=0.5)
        with p3:
            fdd_labor_pct = st.number_input("Labor %", min_value=0.0, max_value=100.0, value=st.session_state["fdd_labor_pct"], step=0.5)
        with p4:
            fdd_occupancy_pct = st.number_input("Occupancy %", min_value=0.0, max_value=100.0, value=st.session_state["fdd_occupancy_pct"], step=0.5)

        p5, p6, p7 = st.columns(3)
        with p5:
            fdd_royalty_pct = st.number_input("Royalty %", min_value=0.0, max_value=100.0, value=st.session_state["fdd_royalty_pct"], step=0.5)
        with p6:
            fdd_marketing_pct = st.number_input("Marketing %", min_value=0.0, max_value=100.0, value=st.session_state["fdd_marketing_pct"], step=0.5)
        with p7:
            fdd_other_pct = st.number_input("Other operating expense %", min_value=0.0, max_value=100.0, value=st.session_state["fdd_other_pct"], step=0.5)

        submit_2 = st.form_submit_button("Save FDD System P&L", use_container_width=True)
        if submit_2:
            save_section("fdd_pl", {
                "fdd_revenue": fdd_revenue,
                "fdd_cogs_pct": fdd_cogs_pct,
                "fdd_labor_pct": fdd_labor_pct,
                "fdd_occupancy_pct": fdd_occupancy_pct,
                "fdd_royalty_pct": fdd_royalty_pct,
                "fdd_marketing_pct": fdd_marketing_pct,
                "fdd_other_pct": fdd_other_pct,
                "avg_rev": fdd_revenue if not section_done("fdd_distribution") else st.session_state["avg_rev"],
            })
            st.success("FDD System P&L saved.")
    if section_done("fdd_pl"):
        total_exp = (
            st.session_state["fdd_cogs_pct"] + st.session_state["fdd_labor_pct"] + st.session_state["fdd_occupancy_pct"] +
            st.session_state["fdd_royalty_pct"] + st.session_state["fdd_marketing_pct"] + st.session_state["fdd_other_pct"]
        ) / 100
        margin = max(0.0, 1 - total_exp)
        monthly = st.session_state["fdd_revenue"] * margin / 12
        s1, s2, s3 = st.columns(3)
        s1.metric("EBITDA (Monthly profit before loan)", money(monthly))
        s2.metric("EBITDA margin", pct(margin))
        s3.metric("Total expense %", pct(total_exp))

# -----------------------------
# 3) FDD Revenue Distribution
# -----------------------------
with st.expander("3) FDD Revenue Distribution", expanded=section_done("fdd_pl") and not section_done("fdd_distribution")):
    st.caption("How stores actually perform across the system.")
    with st.form("form_fdd_distribution"):
        dist_mode = st.radio(
            "Revenue distribution input",
            ["Estimate from average (recommended)", "Use actual FDD quartiles"],
            index=0 if st.session_state["dist_mode"].startswith("Estimate") else 1,
            horizontal=True
        )

        c1, c2 = st.columns(2)
        with c1:
            units_reported = st.number_input("Units reported", min_value=1, value=int(st.session_state["units_reported"]), step=1)
        with c2:
            avg_rev = st.number_input(
                "Average revenue",
                min_value=0.0,
                value=float(st.session_state.get("fdd_revenue", defaults["fdd_revenue"])),
                step=1000.0
            )

        if dist_mode.startswith("Estimate"):
            median_rev = avg_rev * 0.94
            top25 = avg_rev * 1.25
            bottom25 = avg_rev * 0.75
            st.caption("Quartiles estimated using a moderate-variation assumption.")
            q1, q2, q3 = st.columns(3)
            q1.metric("Estimated median revenue", money(median_rev))
            q2.metric("Estimated top 25% revenue", money(top25))
            q3.metric("Estimated bottom 25% revenue", money(bottom25))
        else:
            q1, q2, q3 = st.columns(3)
            with q1:
                median_rev = st.number_input("Median revenue", min_value=0.0, value=float(st.session_state["median_rev"]), step=1000.0)
            with q2:
                top25 = st.number_input("Top 25% revenue", min_value=0.0, value=float(st.session_state["top25"]), step=1000.0)
            with q3:
                bottom25 = st.number_input("Bottom 25% revenue", min_value=0.0, value=float(st.session_state["bottom25"]), step=1000.0)

        submit_3 = st.form_submit_button("Save Revenue Distribution", use_container_width=True)
        if submit_3:
            save_section("fdd_distribution", {
                "dist_mode": dist_mode,
                "units_reported": units_reported,
                "avg_rev": avg_rev,
                "median_rev": median_rev,
                "top25": top25,
                "bottom25": bottom25,
            })
            st.success("FDD Revenue Distribution saved.")
    if section_done("fdd_distribution"):
        spread_pct = safe_div((st.session_state["top25"] - st.session_state["bottom25"]), max(st.session_state["median_rev"], 1))
        skew_pct = safe_div((st.session_state["avg_rev"] - st.session_state["median_rev"]), max(st.session_state["median_rev"], 1))
        gap = st.session_state["fdd_revenue"] - st.session_state["avg_rev"]
        gapp = safe_div(gap, max(st.session_state["avg_rev"], 1))
        s1, s2, s3 = st.columns(3)
        s1.metric("Revenue spread", pct(spread_pct))
        s2.metric("Revenue skew", pct(skew_pct))
        s3.metric("P&L revenue vs avg gap", f"{money(gap)} ({pct(gapp)})")

# -----------------------------
# 4) Financing
# -----------------------------
with st.expander("4) Financing", expanded=section_done("fdd_distribution") and not section_done("financing")):
    st.caption("Your loan and monthly payments.")

    loan_mode = st.radio(
        "How do you want to structure financing?",
        ["% of total project", "Fixed loan amount"],
        index=0 if st.session_state["loan_mode"] == "% of total project" else 1,
        horizontal=True,
        key="loan_mode_selector"
    )
    st.caption("Choose how you want to model your loan: based on lender % or your expected borrowing amount.")

    with st.form("form_financing"):
        f1, f2, f3, f4 = st.columns(4)
        with f1:
            rate = st.number_input("Interest rate %", min_value=0.0, value=st.session_state["rate"], step=0.1)
        with f2:
            term_years = st.number_input("Term (years)", min_value=1.0, value=st.session_state["term_years"], step=1.0)
        with f3:
            if loan_mode == "% of total project":
                debt_pct = st.number_input("Debt % of project", min_value=0.0, max_value=100.0, value=st.session_state["debt_pct"], step=1.0)
                fixed_loan_amount = st.session_state["fixed_loan_amount"]
            else:
                fixed_loan_amount = st.number_input("Loan amount (what you expect to borrow)", min_value=0.0, value=st.session_state["fixed_loan_amount"], step=10000.0)
                debt_pct = st.session_state["debt_pct"]
        with f4:
            extra_liquidity = st.number_input("Additional liquidity outside the deal", min_value=0.0, value=st.session_state["extra_liquidity"], step=1000.0)

        f5, f6, f7 = st.columns(3)
        with f5:
            orig_fee_pct = st.number_input("Origination fee %", min_value=0.0, value=st.session_state["orig_fee_pct"], step=0.1)
        with f6:
            closing_costs = st.number_input("Closing / third-party costs", min_value=0.0, value=st.session_state["closing_costs"], step=500.0)
        with f7:
            guarantee_fees = st.number_input("Guarantee / SBA fees", min_value=0.0, value=st.session_state["guarantee_fees"], step=500.0)

        submit_4 = st.form_submit_button("Save Financing", use_container_width=True)
        if submit_4:
            save_section("financing", {
                "loan_mode": loan_mode,
                "debt_pct": debt_pct,
                "fixed_loan_amount": fixed_loan_amount,
                "rate": rate,
                "term_years": term_years,
                "extra_liquidity": extra_liquidity,
                "orig_fee_pct": orig_fee_pct,
                "closing_costs": closing_costs,
                "guarantee_fees": guarantee_fees,
            })
            st.success("Financing saved.")
    if section_done("financing"):
        fdd_mid = (st.session_state["fdd_low"] + st.session_state["fdd_high"]) / 2
        if st.session_state["loan_mode"] == "% of total project":
            loan = fdd_mid * (st.session_state["debt_pct"] / 100)
        else:
            loan = min(st.session_state["fixed_loan_amount"], fdd_mid)
        monthly = pmt(loan, st.session_state["rate"] / 100, st.session_state["term_years"])
        months = max(int(st.session_state["term_years"] * 12), 1)
        total_paid = monthly * months
        fees = loan * (st.session_state["orig_fee_pct"] / 100) + st.session_state["closing_costs"] + st.session_state["guarantee_fees"]
        equity_needed = max(0.0, fdd_mid - loan)
        s1, s2, s3, s4 = st.columns(4)
        s1.metric("Estimated loan", money(loan))
        s2.metric("Monthly loan payment", money(monthly))
        s3.metric("Total interest over term", money(max(0.0, total_paid - loan)))
        s4.metric("Implied equity needed", money(equity_needed))

# -----------------------------
# 5) Deal Setup
# -----------------------------
with st.expander("5) Deal Setup", expanded=section_done("financing") and not section_done("deal_setup")):
    st.caption("Your location and setup.")
    with st.form("form_deal_setup"):
        d1, d2, d3, d4 = st.columns(4)
        with d1:
            schedule = st.selectbox("Operating schedule", ["7 days/week", "6 days/week", "5 days/week", "Custom"], index=["7 days/week","6 days/week","5 days/week","Custom"].index(st.session_state["schedule"]))
        with d2:
            if schedule == "7 days/week":
                st.number_input("Operating days per year", value=365, disabled=True)
                days_custom = 365
            elif schedule == "6 days/week":
                st.number_input("Operating days per year", value=313, disabled=True)
                days_custom = 313
            elif schedule == "5 days/week":
                st.number_input("Operating days per year", value=260, disabled=True)
                days_custom = 260
            else:
                days_custom = st.number_input("Operating days per year", min_value=1, max_value=365, value=int(st.session_state["days_custom"]), step=1)
        with d3:
            square_feet = st.number_input("Square footage", min_value=0, value=int(st.session_state["square_feet"]), step=50)
        with d4:
            format_type = st.selectbox("Format", ["Inline", "Drive-thru", "End cap", "Other"], index=["Inline","Drive-thru","End cap","Other"].index(st.session_state["format_type"]))

        d5, d6, d7 = st.columns(3)
        with d5:
            local_cost_env = st.selectbox("Local cost environment", ["Low", "Average", "High"], index=["Low","Average","High"].index(st.session_state["local_cost_env"]))
        with d6:
            opening_risk = st.selectbox("Opening timeline risk", ["On schedule", "Minor delay", "Moderate delay", "Heavy delay"], index=["On schedule","Minor delay","Moderate delay","Heavy delay"].index(st.session_state["opening_risk"]))
        with d7:
            ramp_speed = st.selectbox("Ramp speed", ["Fast (3 months)", "Normal (5 months)", "Slow (8 months)"], index=["Fast (3 months)","Normal (5 months)","Slow (8 months)"].index(st.session_state["ramp_speed"]))

        submit_5 = st.form_submit_button("Save Deal Setup", use_container_width=True)
        if submit_5:
            save_section("deal_setup", {
                "schedule": schedule,
                "days_custom": days_custom,
                "square_feet": square_feet,
                "format_type": format_type,
                "local_cost_env": local_cost_env,
                "opening_risk": opening_risk,
                "ramp_speed": ramp_speed,
            })
            st.success("Deal Setup saved.")
    if section_done("deal_setup"):
        operating_days = st.session_state["days_custom"]
        s1, s2, s3 = st.columns(3)
        s1.metric("Operating days per year", f"{operating_days:,.0f}")
        s2.metric("Square feet", f"{st.session_state['square_feet']:,.0f}")
        s3.metric("Format", st.session_state["format_type"])

# -----------------------------
# 6) Startup Assumptions
# -----------------------------
with st.expander("6) Startup Assumptions", expanded=section_done("deal_setup") and not section_done("startup")):
    st.caption("What you think it will cost.")
    with st.form("form_startup"):
        s1, s2, s3 = st.columns(3)
        with s1:
            user_buildout = st.number_input("Buildout estimate", min_value=0.0, value=st.session_state["user_buildout"], step=1000.0)
        with s2:
            user_equipment = st.number_input("Equipment estimate", min_value=0.0, value=st.session_state["user_equipment"], step=1000.0)
        with s3:
            user_soft = st.number_input("Soft costs estimate", min_value=0.0, value=st.session_state["user_soft"], step=1000.0)

        s4, s5, s6, s7 = st.columns(4)
        with s4:
            user_opening = st.number_input("Opening / pre-opening costs", min_value=0.0, value=st.session_state["user_opening"], step=1000.0)
        with s5:
            user_working_cap = st.number_input("Cash needed to stay open (working capital)", min_value=0.0, value=st.session_state["user_working_cap"], step=1000.0)
        with s6:
            unexpected_cost_pct = st.number_input("Unexpected cost % on your estimate", min_value=0.0, max_value=100.0, value=st.session_state["unexpected_cost_pct"], step=1.0)
        with s7:
            estimate_completeness = st.selectbox("How complete is your estimate?", ["Rough guess", "Partial quotes", "Fully quoted"], index=["Rough guess","Partial quotes","Fully quoted"].index(st.session_state["estimate_completeness"]))

        submit_6 = st.form_submit_button("Save Startup Assumptions", use_container_width=True)
        if submit_6:
            save_section("startup", {
                "user_buildout": user_buildout,
                "user_equipment": user_equipment,
                "user_soft": user_soft,
                "user_opening": user_opening,
                "user_working_cap": user_working_cap,
                "unexpected_cost_pct": unexpected_cost_pct,
                "estimate_completeness": estimate_completeness,
            })
            st.success("Startup Assumptions saved.")
    if section_done("startup"):
        startup_labor_preview = (
            st.session_state["startup_training_days"] * st.session_state["startup_staffing_hours_per_day"] *
            st.session_state["startup_avg_staff_per_hour"] * st.session_state["startup_avg_cost_per_hour"]
        )
        total = (
            st.session_state["fdd_franchise_fee"] + st.session_state["user_buildout"] + st.session_state["user_equipment"] +
            st.session_state["user_soft"] + st.session_state["user_opening"] + st.session_state["user_working_cap"] + startup_labor_preview
        )
        s1, s2, s3 = st.columns(3)
        s1.metric("Calculated startup labor", money(startup_labor_preview))
        s2.metric("Your startup estimate", money(total))
        s3.metric("Estimate + unexpected costs", money(total * (1 + st.session_state["unexpected_cost_pct"] / 100)))

# -----------------------------
# 7) Operating Assumptions
# -----------------------------
with st.expander("7) Operating Assumptions", expanded=section_done("startup") and not section_done("operating")):
    st.caption("How your store will run day to day.")
    with st.form("form_operating"):
        o1, o2 = st.columns(2)
        with o1:
            avg_ticket = st.number_input("Average ticket", min_value=0.01, value=st.session_state["avg_ticket"], step=0.25)
        with o2:
            tx_per_day = st.number_input("Transactions per day", min_value=0.0, value=st.session_state["tx_per_day"], step=1.0)

        o4, o5, o6, o7 = st.columns(4)
        with o4:
            base_rent = st.number_input("Base rent / month", min_value=0.0, value=st.session_state["base_rent"], step=100.0)
        with o5:
            cam = st.number_input("CAM / month", min_value=0.0, value=st.session_state["cam"], step=50.0)
        with o6:
            electric = st.number_input("Electric / month", min_value=0.0, value=st.session_state["electric"], step=25.0)
        with o7:
            gas = st.number_input("Gas / month", min_value=0.0, value=st.session_state["gas"], step=25.0)

        o8, o9, o10, o11 = st.columns(4)
        with o8:
            water = st.number_input("Water / month", min_value=0.0, value=st.session_state["water"], step=10.0)
        with o9:
            sewer = st.number_input("Sewer / month", min_value=0.0, value=st.session_state["sewer"], step=10.0)
        with o10:
            trash = st.number_input("Trash / month", min_value=0.0, value=st.session_state["trash"], step=10.0)
        with o11:
            internet = st.number_input("Internet / month", min_value=0.0, value=st.session_state["internet"], step=10.0)

        o12, o13, o14, o15 = st.columns(4)
        with o12:
            phone = st.number_input("Phone / month", min_value=0.0, value=st.session_state["phone"], step=10.0)
        with o13:
            wage = st.number_input("Average wage per hour", min_value=0.0, value=st.session_state["wage"], step=0.25)
        with o14:
            staff_per_hour = st.number_input("Average staff per hour", min_value=0.0, value=st.session_state["staff_per_hour"], step=0.25)
        with o15:
            hours_open_daily = st.number_input("Hours open per day", min_value=0.0, max_value=24.0, value=st.session_state["hours_open_daily"], step=0.5)
        labor_hours_per_day = staff_per_hour * hours_open_daily
        st.caption(f"Calculated staffing hours per day: {labor_hours_per_day:,.1f}")
        owner_comp = st.number_input("Owner salary / draw / month", min_value=0.0, value=st.session_state["owner_comp"], step=100.0)

        o16, o17, o18, o19 = st.columns(4)
        with o16:
            workers_comp = st.number_input("Workers comp / month", min_value=0.0, value=st.session_state["workers_comp"], step=25.0)
        with o17:
            property_ins = st.number_input("Property insurance / month", min_value=0.0, value=st.session_state["property_ins"], step=25.0)
        with o18:
            tech = st.number_input("Tech / POS / software / month", min_value=0.0, value=st.session_state["tech"], step=25.0)
        with o19:
            repairs = st.number_input("Repairs / maintenance / month", min_value=0.0, value=st.session_state["repairs"], step=25.0)

        o20, o21, o22, o23 = st.columns(4)
        with o20:
            admin_misc = st.number_input("Admin / misc. / month", min_value=0.0, value=st.session_state["admin_misc"], step=25.0)
        with o21:
            actual_cogs_pct = st.number_input("COGS %", min_value=0.0, max_value=100.0, value=st.session_state["actual_cogs_pct"], step=0.5)
        with o22:
            payroll_tax_pct = st.number_input("Payroll tax / burden %", min_value=0.0, max_value=100.0, value=st.session_state["payroll_tax_pct"], step=0.5)
        with o23:
            actual_royalty_pct = st.number_input("Royalty %", min_value=0.0, max_value=100.0, value=st.session_state["actual_royalty_pct"], step=0.5)

        o24, o25, o26 = st.columns(3)
        with o24:
            actual_marketing_pct = st.number_input("Marketing %", min_value=0.0, max_value=100.0, value=st.session_state["actual_marketing_pct"], step=0.5)
        with o25:
            merchant_pct = st.number_input("Merchant processing %", min_value=0.0, max_value=100.0, value=st.session_state["merchant_pct"], step=0.1)
        with o26:
            leakage_pct = st.number_input("Delivery / discount leakage %", min_value=0.0, max_value=100.0, value=st.session_state["leakage_pct"], step=0.1)

        submit_7 = st.form_submit_button("Save Operating Assumptions", use_container_width=True)
        if submit_7:
            save_section("operating", {
                "avg_ticket": avg_ticket,
                "tx_per_day": tx_per_day,
                "base_rent": base_rent,
                "cam": cam,
                "electric": electric,
                "gas": gas,
                "water": water,
                "sewer": sewer,
                "trash": trash,
                "internet": internet,
                "phone": phone,
                "wage": wage,
                "staff_per_hour": staff_per_hour,
                "hours_open_daily": hours_open_daily,
                "labor_hours_per_day": labor_hours_per_day,
                "owner_comp": owner_comp,
                "workers_comp": workers_comp,
                "property_ins": property_ins,
                "tech": tech,
                "repairs": repairs,
                "admin_misc": admin_misc,
                "actual_cogs_pct": actual_cogs_pct,
                "payroll_tax_pct": payroll_tax_pct,
                "actual_royalty_pct": actual_royalty_pct,
                "actual_marketing_pct": actual_marketing_pct,
                "merchant_pct": merchant_pct,
                "leakage_pct": leakage_pct,
            })

            # -----------------------------------
            # Bridge to Deal Model (Pro)
            # -----------------------------------
            days = st.session_state["days_custom"]
            annual_revenue = avg_ticket * tx_per_day * days
            monthly_revenue = annual_revenue / 12

            monthly_labor = wage * labor_hours_per_day * (days / 12)
            monthly_payroll_tax = monthly_labor * (payroll_tax_pct / 100)

            monthly_occupancy = base_rent + cam

            other_fixed = (
                monthly_occupancy
                + electric + gas + water + sewer + trash + internet + phone
                + workers_comp + property_ins
                + tech + repairs + admin_misc
                + owner_comp
            )

            ramp_map = {
                "Fast (3 months)": 3,
                "Normal (5 months)": 5,
                "Slow (8 months)": 8,
            }

            st.session_state["fm_target_monthly_revenue"] = monthly_revenue
            st.session_state["fm_cogs_pct"] = actual_cogs_pct / 100
            st.session_state["fm_labor_pct"] = (monthly_labor + monthly_payroll_tax) / max(monthly_revenue, 1)
            st.session_state["fm_royalty_pct"] = actual_royalty_pct / 100
            st.session_state["fm_marketing_pct"] = actual_marketing_pct / 100
            st.session_state["fm_other_variable_pct"] = (merchant_pct + leakage_pct) / 100
            st.session_state["fm_other_fixed"] = other_fixed
            st.session_state["fm_occupancy"] = monthly_occupancy
            st.session_state["fm_ramp_months"] = ramp_map.get(st.session_state["ramp_speed"], 5)
            st.session_state["fm_starting_cash"] = user_working_cap

            st.success("Operating Assumptions saved and synced to Deal Model.")
    if section_done("operating"):
        days = st.session_state["days_custom"]
        annual_rev = st.session_state["avg_ticket"] * st.session_state["tx_per_day"] * days
        s1, s2, s3 = st.columns(3)
        s1.metric("Annual revenue", money(annual_rev))
        s2.metric("Revenue per operating day", money(safe_div(annual_rev, days)))
        s3.metric("Transactions/day", f"{st.session_state['tx_per_day']:,.0f}")

# -----------------------------
# Combined analysis
# -----------------------------
all_done = all(section_done(k) for k, _ in progress_items)
from paywall_ui import require_premium_or_stop

if all_done:
    require_premium_or_stop()

    st.markdown("---")
    st.header("Reality Checks")
    st.caption("This is where your assumptions are compared against the FDD, financing pressure, and modeled startup costs.")

    st.warning(
        "**Reality check**\n"
        "This is where most people get it wrong. The FDD may not include every real-world cost, and it does not determine your revenue. "
        "The numbers shown are system averages, often from mature locations with years of brand awareness. "
        "In a new market, it will likely take longer to reach those levels."
    )

    # pull values
    fdd_low = st.session_state["fdd_low"]
    fdd_high = st.session_state["fdd_high"]
    fdd_franchise_fee = st.session_state["fdd_franchise_fee"]
    fdd_revenue = st.session_state["fdd_revenue"]
    fdd_cogs_pct = st.session_state["fdd_cogs_pct"] / 100
    fdd_labor_pct = st.session_state["fdd_labor_pct"] / 100
    fdd_occupancy_pct = st.session_state["fdd_occupancy_pct"] / 100
    fdd_royalty_pct = st.session_state["fdd_royalty_pct"] / 100
    fdd_marketing_pct = st.session_state["fdd_marketing_pct"] / 100
    fdd_other_pct = st.session_state["fdd_other_pct"] / 100

    avg_rev = st.session_state["avg_rev"]
    median_rev = st.session_state["median_rev"]
    top25 = st.session_state["top25"]
    bottom25 = st.session_state["bottom25"]

    loan_mode = st.session_state["loan_mode"]
    debt_pct = st.session_state["debt_pct"] / 100
    fixed_loan_amount = st.session_state["fixed_loan_amount"]
    rate = st.session_state["rate"] / 100
    term_years = st.session_state["term_years"]
    extra_liquidity = st.session_state["extra_liquidity"]
    orig_fee_pct = st.session_state["orig_fee_pct"] / 100
    closing_costs = st.session_state["closing_costs"]
    guarantee_fees = st.session_state["guarantee_fees"]

    schedule = st.session_state["schedule"]
    operating_days = st.session_state["days_custom"]
    square_feet = st.session_state["square_feet"]
    format_type = st.session_state["format_type"]
    local_cost_env = st.session_state["local_cost_env"]
    opening_risk = st.session_state["opening_risk"]
    ramp_speed = st.session_state["ramp_speed"]

    user_buildout = st.session_state["user_buildout"]
    user_equipment = st.session_state["user_equipment"]
    user_soft = st.session_state["user_soft"]
    user_opening = st.session_state["user_opening"]
    user_working_cap = st.session_state["user_working_cap"]
    startup_training_days = st.session_state["startup_training_days"]
    startup_staffing_hours_per_day = st.session_state["startup_staffing_hours_per_day"]
    startup_avg_staff_per_hour = st.session_state["startup_avg_staff_per_hour"]
    startup_avg_cost_per_hour = st.session_state["startup_avg_cost_per_hour"]
    unexpected_cost_pct = st.session_state["unexpected_cost_pct"] / 100
    estimate_completeness = st.session_state["estimate_completeness"]

    avg_ticket = st.session_state["avg_ticket"]
    tx_per_day = st.session_state["tx_per_day"]
    base_rent = st.session_state["base_rent"]
    cam = st.session_state["cam"]
    electric = st.session_state["electric"]
    gas = st.session_state["gas"]
    water = st.session_state["water"]
    sewer = st.session_state["sewer"]
    trash = st.session_state["trash"]
    internet = st.session_state["internet"]
    phone = st.session_state["phone"]
    wage = st.session_state["wage"]
    staff_per_hour = st.session_state["staff_per_hour"]
    hours_open_daily = st.session_state["hours_open_daily"]
    labor_hours_per_day = staff_per_hour * hours_open_daily
    owner_comp = st.session_state["owner_comp"]
    workers_comp = st.session_state["workers_comp"]
    property_ins = st.session_state["property_ins"]
    tech = st.session_state["tech"]
    repairs = st.session_state["repairs"]
    admin_misc = st.session_state["admin_misc"]
    actual_cogs_pct = st.session_state["actual_cogs_pct"] / 100
    payroll_tax_pct = st.session_state["payroll_tax_pct"] / 100
    actual_royalty_pct = st.session_state["actual_royalty_pct"] / 100
    actual_marketing_pct = st.session_state["actual_marketing_pct"] / 100
    merchant_pct = st.session_state["merchant_pct"] / 100
    leakage_pct = st.session_state["leakage_pct"] / 100

    market_factor_map = {"Low": 0.92, "Average": 1.00, "High": 1.18}
    delay_months_map = {"On schedule": 0, "Minor delay": 1, "Moderate delay": 2, "Heavy delay": 3}
    ramp_months_map = {"Fast (3 months)": 3, "Normal (5 months)": 5, "Slow (8 months)": 8}
    market_factor = market_factor_map[local_cost_env]
    delay_months = delay_months_map[opening_risk]
    ramp_months = ramp_months_map[ramp_speed]
    drive_factor = 1.18 if format_type == "Drive-thru" else 1.00

    # calculations
    annual_revenue = avg_ticket * tx_per_day * operating_days
    gap_to_fdd_avg = annual_revenue - avg_rev
    gap_to_fdd_median = annual_revenue - median_rev
    req_tx_for_avg = safe_div(avg_rev, max(avg_ticket * operating_days, 1))
    req_tx_for_top25 = safe_div(top25, max(avg_ticket * operating_days, 1))
    position_raw = safe_div((annual_revenue - bottom25), max(top25 - bottom25, 1))
    position_label = system_position_label(position_raw)

    fdd_mid = (fdd_low + fdd_high) / 2
    loan_on_fdd = (fdd_mid * debt_pct) if loan_mode == "% of total project" else min(fixed_loan_amount, fdd_mid)
    monthly_debt_on_fdd = pmt(loan_on_fdd, rate, term_years)
    months = max(int(term_years * 12), 1)
    total_paid_on_fdd = monthly_debt_on_fdd * months
    financing_fees_on_fdd = loan_on_fdd * orig_fee_pct + closing_costs + guarantee_fees

    profile_build_psf = 210.0
    equip_anchor = 120000.0 * (1.08 if format_type == "Drive-thru" else 1.0)
    modeled_buildout = square_feet * profile_build_psf * market_factor * drive_factor
    modeled_equipment = equip_anchor * market_factor
    modeled_soft = (modeled_buildout + modeled_equipment) * 0.10
    monthly_occupancy = base_rent + cam
    modeled_opening = (modeled_buildout + modeled_equipment) * 0.04 + (monthly_occupancy * delay_months)

    monthly_revenue = annual_revenue / 12
    monthly_labor = wage * labor_hours_per_day * (operating_days / 12)
    monthly_payroll_tax = monthly_labor * payroll_tax_pct
    monthly_cogs = monthly_revenue * actual_cogs_pct
    monthly_royalty = monthly_revenue * actual_royalty_pct
    monthly_marketing = monthly_revenue * actual_marketing_pct
    monthly_merchant = monthly_revenue * merchant_pct
    monthly_leakage = monthly_revenue * leakage_pct
    monthly_utilities = electric + gas + water + sewer + trash + internet + phone
    monthly_insurance = workers_comp + property_ins
    monthly_fixed_other = monthly_occupancy + monthly_utilities + monthly_insurance + tech + repairs + admin_misc + owner_comp

    monthly_profit_before_loan = monthly_revenue - (
        monthly_cogs + monthly_labor + monthly_payroll_tax + monthly_royalty +
        monthly_marketing + monthly_merchant + monthly_leakage + monthly_fixed_other
    )

    base_working_cap = max(0.0, (monthly_fixed_other + monthly_labor + monthly_payroll_tax) * 0.35 * max(3, ramp_months))
    loss_support = max(0.0, -monthly_profit_before_loan) * max(3, round(ramp_months))
    modeled_working_cap = base_working_cap + loss_support + (monthly_fixed_other * delay_months)
    final_modeled_working_cap = max(user_working_cap, modeled_working_cap) if user_working_cap > 0 else modeled_working_cap

    contingency_pct = {"Rough guess": 0.22, "Partial quotes": 0.15, "Fully quoted": 0.10}[estimate_completeness]
    modeled_contingency = (modeled_buildout + modeled_equipment + modeled_soft) * contingency_pct

    startup_labor_cost = startup_training_days * startup_staffing_hours_per_day * startup_avg_staff_per_hour * startup_avg_cost_per_hour

    modeled_startup_pre_financing = (
        fdd_franchise_fee + modeled_buildout + modeled_equipment + modeled_soft +
        modeled_opening + final_modeled_working_cap + modeled_contingency + startup_labor_cost
    )
    modeled_loan = (modeled_startup_pre_financing * debt_pct) if loan_mode == "% of total project" else min(fixed_loan_amount, modeled_startup_pre_financing)
    modeled_financing_fees = modeled_loan * orig_fee_pct + closing_costs + guarantee_fees
    modeled_total_capital = modeled_startup_pre_financing + modeled_financing_fees
    stress_total_capital = modeled_total_capital * (
        1.20 if estimate_completeness == "Rough guess" else 1.14 if estimate_completeness == "Partial quotes" else 1.08
    )

    user_start_total = fdd_franchise_fee + user_buildout + user_equipment + user_soft + user_opening + user_working_cap + startup_labor_cost
    user_start_with_unexpected = user_start_total * (1 + unexpected_cost_pct)

    rc1, rc2, rc3, rc4 = st.columns(4)
    rc1.metric("Your estimate + unexpected costs", money(user_start_with_unexpected))
    rc2.metric("Modeled estimate", money(modeled_total_capital))
    rc3.metric("Stress-case estimate", money(stress_total_capital))
    rc4.metric("Capital gap", money(modeled_total_capital - user_start_with_unexpected))

    st.write("**How your sales assumptions compare to the FDD**")
    cmp1, cmp2, cmp3 = st.columns(3)
    cmp1.metric("Gap vs FDD average", money(gap_to_fdd_avg))
    cmp2.metric("Gap vs FDD median", money(gap_to_fdd_median))
    cmp3.metric("System position", position_label)

    cmp4, cmp5 = st.columns(2)
    cmp4.metric("Transactions/day needed for FDD average", f"{req_tx_for_avg:,.0f}")
    cmp5.metric("Transactions/day needed for top 25%", f"{req_tx_for_top25:,.0f}")

    st.write("**Traffic Reality Check**")
    st.caption("Most operators overestimate conversion and demand. Even small overestimates can materially change the outcome.")

    conv_option = st.selectbox(
        "Conversion assumption (passing traffic to paying customer)",
        [
            "Very conservative (0.5%)",
            "Moderate (1.0%)",
            "Strong (1.5%)",
            "Very strong (2.0%)"
        ],
        index=1,
        key="traffic_conversion_assumption"
    )

    conversion_map = {
        "Very conservative (0.5%)": 0.005,
        "Moderate (1.0%)": 0.010,
        "Strong (1.5%)": 0.015,
        "Very strong (2.0%)": 0.020
    }
    conversion_rate = conversion_map[conv_option]

    hours_open_assumption = st.number_input(
        "Hours open per day (for hourly view)",
        min_value=1.0,
        max_value=24.0,
        value=12.0,
        step=0.5,
        key="hours_open_assumption"
    )

    avg_cust_per_hour = safe_div(req_tx_for_avg, hours_open_assumption)
    top_cust_per_hour = safe_div(req_tx_for_top25, hours_open_assumption)
    implied_traffic_for_avg = safe_div(req_tx_for_avg, conversion_rate)
    implied_traffic_for_top = safe_div(req_tx_for_top25, conversion_rate)

    tr1, tr2 = st.columns(2)
    tr1.metric("Customers/hour needed for FDD average", f"{avg_cust_per_hour:,.1f}")
    tr2.metric("Customers/hour needed for top 25%", f"{top_cust_per_hour:,.1f}")

    tr3, tr4 = st.columns(2)
    tr3.metric("Implied daily traffic needed for FDD average", f"{implied_traffic_for_avg:,.0f}")
    tr4.metric("Implied daily traffic needed for top 25%", f"{implied_traffic_for_top:,.0f}")

    st.info("This does not predict your traffic. It shows what reality would likely need to look like to hit the FDD average or top-quartile performance.")

    st.write("**Break-Even Reality Check**")
    site_traffic = st.number_input(
        "Estimated daily passing traffic at your site",
        min_value=0.0,
        value=30000.0,
        step=1000.0,
        key="site_traffic_break_even"
    )

    modeled_monthly_debt = pmt(modeled_loan, rate, term_years)
    variable_pct_local = actual_cogs_pct + actual_royalty_pct + actual_marketing_pct + merchant_pct + leakage_pct
    contribution_margin_local = max(0.0001, 1 - variable_pct_local)
    break_even_monthly_revenue_local = safe_div(
        (monthly_labor + monthly_payroll_tax + monthly_fixed_other + modeled_monthly_debt),
        contribution_margin_local
    )
    break_even_tx_day_local = safe_div((break_even_monthly_revenue_local * 12 / operating_days), avg_ticket)

    break_even_capture_rate = safe_div(break_even_tx_day_local, site_traffic) if site_traffic > 0 else 0.0
    avg_capture_rate = safe_div(req_tx_for_avg, site_traffic) if site_traffic > 0 else 0.0
    top_capture_rate = safe_div(req_tx_for_top25, site_traffic) if site_traffic > 0 else 0.0

    br1, br2, br3 = st.columns(3)
    br1.metric("Break-even transactions/day", f"{break_even_tx_day_local:,.0f}")
    br2.metric("Required capture rate to break even", pct(break_even_capture_rate))
    br3.metric("Your site traffic input", f"{site_traffic:,.0f}")

    br4, br5 = st.columns(2)
    br4.metric("Required capture rate for FDD average", pct(avg_capture_rate))
    br5.metric("Required capture rate for top 25%", pct(top_capture_rate))

    st.caption("This shows what share of total passing traffic you would need to capture to break even or reach the FDD benchmarks.")

    st.write("**Where your startup estimate may be off**")
    st.table({
        "Category": ["Franchise fee","Buildout","Equipment","Soft costs","Opening / pre-opening","Startup labor","Working capital","Unexpected / contingency","Financing fees","Total"],
        "Your estimate": [
            money(fdd_franchise_fee), money(user_buildout), money(user_equipment), money(user_soft),
            money(user_opening), money(startup_labor_cost), money(user_working_cap), money(user_start_with_unexpected - user_start_total),
            money(0), money(user_start_with_unexpected)
        ],
        "Modeled": [
            money(fdd_franchise_fee), money(modeled_buildout), money(modeled_equipment), money(modeled_soft),
            money(modeled_opening), money(startup_labor_cost), money(final_modeled_working_cap), money(modeled_contingency),
            money(modeled_financing_fees), money(modeled_total_capital)
        ]
    })

    # FDD P&L vs Your Assumptions P&L (Year 1)
    fdd_total_expense_pct = (
        fdd_cogs_pct + fdd_labor_pct + fdd_occupancy_pct +
        fdd_royalty_pct + fdd_marketing_pct + fdd_other_pct
    )
    fdd_ebitda_annual = fdd_revenue * max(0.0, 1 - fdd_total_expense_pct)

    your_year1_revenue = annual_revenue
    your_year1_cogs = monthly_cogs * 12
    your_year1_labor = (monthly_labor + monthly_payroll_tax) * 12
    your_year1_occupancy = monthly_occupancy * 12
    your_year1_royalty = monthly_royalty * 12
    your_year1_marketing = monthly_marketing * 12
    your_year1_other = (monthly_utilities + monthly_insurance + tech + repairs + admin_misc + owner_comp + monthly_merchant + monthly_leakage) * 12
    your_year1_ebitda = monthly_profit_before_loan * 12

    st.write("**FDD P&L vs Your Assumptions P&L (Year 1)**")
    st.table({
        "Metric": [
            "Revenue",
            "COGS",
            "Labor",
            "Occupancy",
            "Royalty",
            "Marketing",
            "Other",
            "EBITDA"
        ],
        "FDD P&L": [
            money(fdd_revenue),
            money(fdd_revenue * fdd_cogs_pct),
            money(fdd_revenue * fdd_labor_pct),
            money(fdd_revenue * fdd_occupancy_pct),
            money(fdd_revenue * fdd_royalty_pct),
            money(fdd_revenue * fdd_marketing_pct),
            money(fdd_revenue * fdd_other_pct),
            money(fdd_ebitda_annual)
        ],
        "Your Assumptions P&L (Year 1)": [
            money(your_year1_revenue),
            money(your_year1_cogs),
            money(your_year1_labor),
            money(your_year1_occupancy),
            money(your_year1_royalty),
            money(your_year1_marketing),
            money(your_year1_other),
            money(your_year1_ebitda)
        ],
        "Difference": [
            money(your_year1_revenue - fdd_revenue),
            money(your_year1_cogs - (fdd_revenue * fdd_cogs_pct)),
            money(your_year1_labor - (fdd_revenue * fdd_labor_pct)),
            money(your_year1_occupancy - (fdd_revenue * fdd_occupancy_pct)),
            money(your_year1_royalty - (fdd_revenue * fdd_royalty_pct)),
            money(your_year1_marketing - (fdd_revenue * fdd_marketing_pct)),
            money(your_year1_other - (fdd_revenue * fdd_other_pct)),
            money(your_year1_ebitda - fdd_ebitda_annual)
        ]
    })

    st.markdown("---")
    st.header("Results")
    st.caption("Your monthly numbers, cash flow, and final decision.")

    modeled_monthly_debt = pmt(modeled_loan, rate, term_years)
    modeled_total_paid = modeled_monthly_debt * months
    modeled_total_interest = max(0.0, modeled_total_paid - modeled_loan)
    modeled_total_loan_cost = modeled_total_paid + modeled_financing_fees

    monthly_money_left_after_loan = monthly_profit_before_loan - modeled_monthly_debt
    dscr = safe_div(monthly_profit_before_loan, modeled_monthly_debt) if modeled_monthly_debt > 0 else 99.0
    variable_pct = actual_cogs_pct + actual_royalty_pct + actual_marketing_pct + merchant_pct + leakage_pct
    contribution_margin = max(0.0001, 1 - variable_pct)
    break_even_monthly_revenue = (monthly_labor + monthly_payroll_tax + monthly_fixed_other + modeled_monthly_debt) / contribution_margin
    break_even_tx_day = safe_div((break_even_monthly_revenue * 12 / operating_days), avg_ticket)

    starting_cash = final_modeled_working_cap + extra_liquidity
    cash = starting_cash
    cash_series = []
    for month in range(1, 13):
        frac = min(1.0, max(0.40, month / max(ramp_months, 1)))
        month_rev = monthly_revenue * frac
        month_cogs = month_rev * actual_cogs_pct
        month_royalty = month_rev * actual_royalty_pct
        month_marketing = month_rev * actual_marketing_pct
        month_merchant = month_rev * merchant_pct
        month_leakage = month_rev * leakage_pct
        month_labor = monthly_labor * (0.85 + 0.15 * frac)
        month_payroll = month_labor * payroll_tax_pct
        month_profit_before_loan = month_rev - (
            month_cogs + month_labor + month_payroll + month_royalty +
            month_marketing + month_merchant + month_leakage + monthly_fixed_other
        )
        month_after_loan = month_profit_before_loan - modeled_monthly_debt
        cash += month_after_loan
        cash_series.append(cash)

    lowest_cash = min(cash_series) if cash_series else starting_cash
    lowest_cash_month = (cash_series.index(lowest_cash) + 1) if cash_series else 0
    added_cash_needed = abs(lowest_cash) if lowest_cash < 0 else 0.0

    r1, r2, r3, r4 = st.columns(4)
    r1.metric("Monthly revenue", money(monthly_revenue))
    r2.metric("EBITDA (Monthly profit before loan)", money(monthly_profit_before_loan))
    r3.metric("Monthly loan payment", money(modeled_monthly_debt))
    r4.metric("Money left after loan", money(monthly_money_left_after_loan))

    r5, r6, r7, r8 = st.columns(4)
    r5.metric("DSCR", f"{dscr:.2f}x" if modeled_monthly_debt > 0 else "N/A")
    r6.metric("Sales needed to not lose money", money(break_even_monthly_revenue))
    r7.metric("Break-even transactions / day", f"{break_even_tx_day:,.0f}")
    r8.metric("Added cash needed", money(added_cash_needed))

    st.line_chart({"Ending cash balance": cash_series})

    risk_flags = []
    if modeled_total_capital - user_start_with_unexpected > 50000:
        risk_flags.append("Your startup estimate still appears low versus the modeled estimate.")
    if position_label in ["Top quartile", "Aggressive"]:
        risk_flags.append("Your sales assumptions rely on above-average to top-quartile system performance.")
    if dscr < 1.0:
        risk_flags.append("The business does not fully cover the loan payment.")
    if monthly_money_left_after_loan < 0:
        risk_flags.append("The store is losing money after the loan payment at stabilization.")
    if added_cash_needed > 0:
        risk_flags.append("The 12-month cash curve goes negative.")
    if operating_days < 313:
        risk_flags.append("Fewer operating days increase the daily sales needed to make the deal work.")
    if delay_months >= 2:
        risk_flags.append("Opening delays are increasing rent drag and cash needed.")

    if dscr < 1.0 or monthly_money_left_after_loan < 0 or added_cash_needed > 0 or position_label == "Aggressive":
        st.error("High Risk: Under these assumptions, the deal shows meaningful pressure from capital needs, debt, cash flow, or aggressive sales expectations.")
    elif dscr < 1.25 or position_label == "Top quartile" or modeled_total_capital > user_start_with_unexpected:
        st.warning("Caution: The deal may work, but the margin for error looks thin. Focus on startup capital, daily sales realism, and debt pressure.")
    else:
        st.success("Proceed: The deal may work under these assumptions, but it still needs real bids, lender terms, and validation.")

    st.write("**Top risk drivers**")
    if risk_flags:
        for item in risk_flags:
            st.write(f"- {item}")
    else:
        st.write("- No major risk flags triggered under the current assumptions, but this still needs real-world validation.")
else:
    st.info("Complete and save each section above. Reality Checks and Results will appear once all sections are submitted.")
