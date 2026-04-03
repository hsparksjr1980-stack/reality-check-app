import pandas as pd


MONTH_LABELS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def _safe_float(value, default=0.0):
    try:
        if value is None or value == "":
            return float(default)
        return float(value)
    except (TypeError, ValueError):
        return float(default)


def _safe_int(value, default=0):
    try:
        if value is None or value == "":
            return int(default)
        return int(value)
    except (TypeError, ValueError):
        return int(default)


def _safe_div(a, b):
    return a / b if b else 0.0


def _growth_multiplier(growth_pct, year_num):
    return (1 + _safe_float(growth_pct, 0.0)) ** max(year_num - 1, 0)


def _get_year1_monthly_plan(inputs):
    """
    Returns a list of 12 dicts with:
    month_in_year, month_label, tickets, avg_ticket, revenue
    """
    forecast_mode = inputs.get("forecast_mode", "flat")
    revenue_mode = inputs.get("revenue_mode", "annual_revenue")
    seasonality_mode = inputs.get("seasonality_mode", "monthly_revenue")

    if forecast_mode == "seasonal":
        plan_df = inputs.get("monthly_plan")
        if isinstance(plan_df, pd.DataFrame) and not plan_df.empty:
            working = plan_df.copy()

            if "Month" not in working.columns:
                working["Month"] = MONTH_LABELS[: len(working)]

            if seasonality_mode == "monthly_revenue":
                if "Revenue" not in working.columns:
                    working["Revenue"] = 0.0
                working["Revenue"] = pd.to_numeric(working["Revenue"], errors="coerce").fillna(0.0)

                rows = []
                for i in range(min(12, len(working))):
                    revenue = float(working.iloc[i]["Revenue"])
                    rows.append(
                        {
                            "month_in_year": i + 1,
                            "month_label": MONTH_LABELS[i],
                            "tickets": 0.0,
                            "avg_ticket": 0.0,
                            "revenue": revenue,
                        }
                    )
                while len(rows) < 12:
                    rows.append(
                        {
                            "month_in_year": len(rows) + 1,
                            "month_label": MONTH_LABELS[len(rows)],
                            "tickets": 0.0,
                            "avg_ticket": 0.0,
                            "revenue": 0.0,
                        }
                    )
                return rows

            # seasonality_mode == "monthly_tickets"
            if "Tickets" not in working.columns:
                working["Tickets"] = 0.0
            if "Avg Ticket" not in working.columns:
                working["Avg Ticket"] = 0.0

            working["Tickets"] = pd.to_numeric(working["Tickets"], errors="coerce").fillna(0.0)
            working["Avg Ticket"] = pd.to_numeric(working["Avg Ticket"], errors="coerce").fillna(0.0)

            rows = []
            for i in range(min(12, len(working))):
                tickets = float(working.iloc[i]["Tickets"])
                avg_ticket = float(working.iloc[i]["Avg Ticket"])
                revenue = tickets * avg_ticket
                rows.append(
                    {
                        "month_in_year": i + 1,
                        "month_label": MONTH_LABELS[i],
                        "tickets": tickets,
                        "avg_ticket": avg_ticket,
                        "revenue": revenue,
                    }
                )
            while len(rows) < 12:
                rows.append(
                    {
                        "month_in_year": len(rows) + 1,
                        "month_label": MONTH_LABELS[len(rows)],
                        "tickets": 0.0,
                        "avg_ticket": 0.0,
                        "revenue": 0.0,
                    }
                )
            return rows

    # flat mode
    if revenue_mode == "annual_tickets":
        annual_tickets = _safe_float(inputs.get("annual_tickets", 0.0))
        avg_ticket = _safe_float(inputs.get("avg_ticket", 0.0))
        annual_revenue = annual_tickets * avg_ticket
        monthly_tickets = annual_tickets / 12
        monthly_revenue = annual_revenue / 12

        return [
            {
                "month_in_year": i + 1,
                "month_label": MONTH_LABELS[i],
                "tickets": monthly_tickets,
                "avg_ticket": avg_ticket,
                "revenue": monthly_revenue,
            }
            for i in range(12)
        ]

    annual_revenue = _safe_float(inputs.get("annual_revenue", 0.0))
    monthly_revenue = annual_revenue / 12

    return [
        {
            "month_in_year": i + 1,
            "month_label": MONTH_LABELS[i],
            "tickets": 0.0,
            "avg_ticket": 0.0,
            "revenue": monthly_revenue,
        }
        for i in range(12)
    ]


def build_3year_forecast(inputs):
    year1_plan = _get_year1_monthly_plan(inputs)

    revenue_growth_pct = _safe_float(inputs.get("revenue_growth_pct", 0.03))
    cogs_pct = _safe_float(inputs.get("cogs_pct", 0.0))
    labor_pct = _safe_float(inputs.get("labor_pct", 0.0))
    royalty_pct = _safe_float(inputs.get("royalty_pct", 0.0))
    marketing_pct = _safe_float(inputs.get("marketing_pct", 0.0))
    merchant_pct = _safe_float(inputs.get("merchant_pct", 0.0))
    leakage_pct = _safe_float(inputs.get("leakage_pct", 0.0))

    base_rent = _safe_float(inputs.get("base_rent", 0.0))
    cam = _safe_float(inputs.get("cam", 0.0))

    electric = _safe_float(inputs.get("electric", 0.0))
    gas = _safe_float(inputs.get("gas", 0.0))
    water = _safe_float(inputs.get("water", 0.0))
    sewer = _safe_float(inputs.get("sewer", 0.0))
    trash = _safe_float(inputs.get("trash", 0.0))
    internet = _safe_float(inputs.get("internet", 0.0))
    phone = _safe_float(inputs.get("phone", 0.0))

    workers_comp = _safe_float(inputs.get("workers_comp", 0.0))
    property_ins = _safe_float(inputs.get("property_ins", 0.0))
    tech = _safe_float(inputs.get("tech", 0.0))
    repairs = _safe_float(inputs.get("repairs", 0.0))
    admin_misc = _safe_float(inputs.get("admin_misc", 0.0))
    owner_comp = _safe_float(inputs.get("owner_comp", 0.0))

    starting_cash = _safe_float(inputs.get("starting_cash", 0.0))
    debt_payment = _safe_float(inputs.get("debt_payment", 0.0))

    growths = {
        "cogs": _safe_float(inputs.get("cogs_growth_pct", 0.03)),
        "labor": _safe_float(inputs.get("labor_growth_pct", 0.03)),
        "royalty": _safe_float(inputs.get("royalty_growth_pct", 0.03)),
        "marketing": _safe_float(inputs.get("marketing_growth_pct", 0.03)),
        "merchant": _safe_float(inputs.get("merchant_growth_pct", 0.03)),
        "leakage": _safe_float(inputs.get("leakage_growth_pct", 0.03)),
        "occupancy": _safe_float(inputs.get("occupancy_growth_pct", 0.03)),
        "utilities": _safe_float(inputs.get("utilities_growth_pct", 0.03)),
        "insurance": _safe_float(inputs.get("insurance_growth_pct", 0.03)),
        "tech": _safe_float(inputs.get("tech_growth_pct", 0.03)),
        "repairs": _safe_float(inputs.get("repairs_growth_pct", 0.03)),
        "admin": _safe_float(inputs.get("admin_growth_pct", 0.03)),
        "owner_comp": _safe_float(inputs.get("owner_comp_growth_pct", 0.03)),
    }

    rows = []
    cash = starting_cash

    for year_num in range(1, 4):
        revenue_mult = _growth_multiplier(revenue_growth_pct, year_num)

        for month_data in year1_plan:
            month_in_year = month_data["month_in_year"]
            month_label = month_data["month_label"]

            tickets = _safe_float(month_data["tickets"], 0.0)
            avg_ticket = _safe_float(month_data["avg_ticket"], 0.0)
            base_revenue = _safe_float(month_data["revenue"], 0.0)

            revenue = base_revenue * revenue_mult

            if tickets > 0 and avg_ticket > 0:
                tickets = tickets * revenue_mult
                revenue = tickets * avg_ticket

            cogs = revenue * cogs_pct * _growth_multiplier(growths["cogs"], year_num)
            labor = revenue * labor_pct * _growth_multiplier(growths["labor"], year_num)
            royalty = revenue * royalty_pct * _growth_multiplier(growths["royalty"], year_num)
            marketing = revenue * marketing_pct * _growth_multiplier(growths["marketing"], year_num)
            merchant_fees = revenue * merchant_pct * _growth_multiplier(growths["merchant"], year_num)
            leakage = revenue * leakage_pct * _growth_multiplier(growths["leakage"], year_num)

            occupancy = (base_rent + cam) * _growth_multiplier(growths["occupancy"], year_num)

            utilities = (
                electric + gas + water + sewer + trash + internet + phone
            ) * _growth_multiplier(growths["utilities"], year_num)

            insurance = (
                workers_comp + property_ins
            ) * _growth_multiplier(growths["insurance"], year_num)

            tech_cost = tech * _growth_multiplier(growths["tech"], year_num)
            repairs_cost = repairs * _growth_multiplier(growths["repairs"], year_num)
            admin_cost = admin_misc * _growth_multiplier(growths["admin"], year_num)
            owner_comp_cost = owner_comp * _growth_multiplier(growths["owner_comp"], year_num)

            gross_profit = revenue - cogs

            total_operating_expenses = (
                labor
                + royalty
                + marketing
                + merchant_fees
                + leakage
                + occupancy
                + utilities
                + insurance
                + tech_cost
                + repairs_cost
                + admin_cost
                + owner_comp_cost
            )

            ebitda = gross_profit - (
                labor
                + royalty
                + marketing
                + merchant_fees
                + leakage
                + occupancy
                + utilities
                + insurance
                + tech_cost
                + repairs_cost
                + admin_cost
                + owner_comp_cost
            )

            net_income = ebitda - debt_payment
            cash += net_income

            month_index = (year_num - 1) * 12 + month_in_year

            rows.append(
                {
                    "Month Index": month_index,
                    "Year": year_num,
                    "Month In Year": month_in_year,
                    "Month Label": month_label,
                    "Tickets": tickets,
                    "Avg Ticket": avg_ticket,
                    "Revenue": revenue,
                    "COGS": cogs,
                    "Gross Profit": gross_profit,
                    "Labor": labor,
                    "Royalty": royalty,
                    "Marketing": marketing,
                    "Merchant Fees": merchant_fees,
                    "Leakage": leakage,
                    "Occupancy": occupancy,
                    "Utilities": utilities,
                    "Insurance": insurance,
                    "Tech/POS": tech_cost,
                    "Repairs": repairs_cost,
                    "Admin/Misc": admin_cost,
                    "Owner Comp": owner_comp_cost,
                    "Total Operating Expenses": total_operating_expenses,
                    "EBITDA": ebitda,
                    "Debt Service": debt_payment,
                    "Net Income": net_income,
                    "Ending Cash": cash,
                }
            )

    return pd.DataFrame(rows)


def build_pnl(df):
    if df is None or df.empty:
        return pd.DataFrame()

    return df.groupby("Year", as_index=False).agg(
        {
            "Tickets": "sum",
            "Revenue": "sum",
            "COGS": "sum",
            "Gross Profit": "sum",
            "Labor": "sum",
            "Royalty": "sum",
            "Marketing": "sum",
            "Merchant Fees": "sum",
            "Leakage": "sum",
            "Occupancy": "sum",
            "Utilities": "sum",
            "Insurance": "sum",
            "Tech/POS": "sum",
            "Repairs": "sum",
            "Admin/Misc": "sum",
            "Owner Comp": "sum",
            "Total Operating Expenses": "sum",
            "EBITDA": "sum",
            "Debt Service": "sum",
            "Net Income": "sum",
        }
    )


def build_monthly_pnl_views(df):
    if df is None or df.empty:
        return {}

    line_items = [
        "Tickets",
        "Avg Ticket",
        "Revenue",
        "COGS",
        "Gross Profit",
        "Labor",
        "Royalty",
        "Marketing",
        "Merchant Fees",
        "Leakage",
        "Occupancy",
        "Utilities",
        "Insurance",
        "Tech/POS",
        "Repairs",
        "Admin/Misc",
        "Owner Comp",
        "Total Operating Expenses",
        "EBITDA",
        "Debt Service",
        "Net Income",
        "Ending Cash",
    ]

    yearly_views = {}

    for year_num in sorted(df["Year"].unique()):
        year_df = df[df["Year"] == year_num].copy().sort_values("Month In Year")
        month_labels = year_df["Month Label"].tolist()

        rows = []
        for item in line_items:
            row = {"Line Item": item}
            values = year_df[item].tolist()

            for label, value in zip(month_labels, values):
                row[label] = value

            if item == "Avg Ticket":
                row["Total"] = year_df[item].mean()
            elif item == "Ending Cash":
                row["Total"] = year_df[item].iloc[-1]
            else:
                row["Total"] = year_df[item].sum()

            rows.append(row)

        yearly_views[int(year_num)] = pd.DataFrame(rows)

    return yearly_views


def build_balance_sheet_summary(df, inputs, sources_uses):
    if df is None or df.empty:
        return pd.DataFrame()

    def _year_end_cash(year_num):
        year_df = df.loc[df["Year"] == year_num, "Ending Cash"]
        if year_df.empty:
            return 0.0
        return float(year_df.iloc[-1])

    debt = _safe_float(sources_uses.get("debt", 0.0))
    equity = _safe_float(sources_uses.get("equity", 0.0))

    return pd.DataFrame(
        [
            {
                "Year": 1,
                "Cash": _year_end_cash(1),
                "Debt (modeled opening)": debt,
                "Equity Invested": equity,
            },
            {
                "Year": 2,
                "Cash": _year_end_cash(2),
                "Debt (modeled opening)": debt,
                "Equity Invested": equity,
            },
            {
                "Year": 3,
                "Cash": _year_end_cash(3),
                "Debt (modeled opening)": debt,
                "Equity Invested": equity,
            },
        ]
    )


def calculate_metrics(df, inputs, sources_uses):
    if df is None or df.empty:
        return {
            "roi": 0.0,
            "payback_month": None,
            "break_even_month": None,
            "lowest_cash": 0.0,
            "lowest_cash_month": None,
            "equity_at_risk": 0.0,
            "dscr": 0.0,
            "stabilized_monthly_net": 0.0,
        }

    debt_payment = _safe_float(inputs.get("debt_payment", 0.0))
    equity_at_risk = _safe_float(sources_uses.get("equity", 0.0)) + max(
        _safe_float(sources_uses.get("gap", 0.0)), 0.0
    )

    monthly_net = df["Net Income"]
    monthly_ebitda = df["EBITDA"]

    stabilized_monthly_net = float(monthly_net.tail(12).mean())
    stabilized_annual_net = stabilized_monthly_net * 12
    roi = _safe_div(stabilized_annual_net, equity_at_risk)

    cumulative_net = monthly_net.cumsum()
    payback_month = next(
        (i + 1 for i, v in enumerate(cumulative_net) if v >= equity_at_risk),
        None,
    )
    break_even_month = next(
        (i + 1 for i, v in enumerate(monthly_net) if v > 0),
        None,
    )

    lowest_cash = float(df["Ending Cash"].min())
    lowest_cash_month = int(df.loc[df["Ending Cash"].idxmin(), "Month Index"])

    stabilized_monthly_ebitda = float(monthly_ebitda.tail(12).mean())
    dscr = _safe_div(stabilized_monthly_ebitda, debt_payment) if debt_payment > 0 else 0.0

    return {
        "roi": float(roi),
        "payback_month": payback_month,
        "break_even_month": break_even_month,
        "lowest_cash": float(lowest_cash),
        "lowest_cash_month": lowest_cash_month,
        "equity_at_risk": float(equity_at_risk),
        "dscr": float(dscr),
        "stabilized_monthly_net": float(stabilized_monthly_net),
    }


def run_downside_case(inputs, sources_uses):
    downside = dict(inputs)

    if downside.get("forecast_mode") == "seasonal":
        plan_df = downside.get("monthly_plan")
        if isinstance(plan_df, pd.DataFrame) and not plan_df.empty:
            plan_df = plan_df.copy()
            if "Revenue" in plan_df.columns:
                plan_df["Revenue"] = pd.to_numeric(plan_df["Revenue"], errors="coerce").fillna(0.0) * 0.85
            if "Tickets" in plan_df.columns:
                plan_df["Tickets"] = pd.to_numeric(plan_df["Tickets"], errors="coerce").fillna(0.0) * 0.90
            downside["monthly_plan"] = plan_df
    else:
        downside["annual_revenue"] = _safe_float(inputs.get("annual_revenue", 0.0)) * 0.85
        downside["annual_tickets"] = _safe_float(inputs.get("annual_tickets", 0.0)) * 0.90

    downside["labor_pct"] = _safe_float(inputs.get("labor_pct", 0.0)) + 0.03
    downside["cogs_pct"] = _safe_float(inputs.get("cogs_pct", 0.0)) + 0.03
    downside["ramp_months"] = _safe_int(inputs.get("ramp_months", 1), 1) + 3

    df_down = build_3year_forecast(downside)
    metrics_down = calculate_metrics(df_down, downside, sources_uses)
    return df_down, metrics_down


def what_breaks_first(base_metrics, downside_metrics, sources_uses, inputs):
    issues = []

    if _safe_float(sources_uses.get("gap", 0.0)) > 0:
        issues.append("Your capital stack does not currently cover total uses.")

    if _safe_float(base_metrics.get("lowest_cash", 0.0)) < 0:
        issues.append("Cash goes negative before the business stabilizes.")

    if _safe_float(base_metrics.get("dscr", 0.0)) < 1.25:
        issues.append("Debt service coverage is thin even before stress testing.")

    if _safe_float(downside_metrics.get("lowest_cash", 0.0)) < 0:
        issues.append("A downside case produces a cash shortfall quickly.")

    downside_break_even = downside_metrics.get("break_even_month")
    if downside_break_even is None or downside_break_even > 18:
        issues.append("Break-even takes too long under a more realistic downside case.")

    if _safe_float(downside_metrics.get("roi", 0.0)) < 0.15:
        issues.append("Return on invested equity becomes weak once downside pressure is introduced.")

    if not issues:
        issues.append(
            "No single early break point dominates, but the deal still needs lender, lease, and buildout discipline."
        )

    return issues[:3]
