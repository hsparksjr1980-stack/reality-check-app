import pandas as pd


def st_session():
    import streamlit as st
    return st.session_state


def _empty_df(columns):
    return pd.DataFrame(columns=columns)


def init_workspace_state():
    defaults = {
        "funding_debt": _empty_df([
            "Bank / Lender",
            "Product (SBA/Conventional/Private)",
            "Loan Amount",
            "Rate (%)",
            "Term (years)",
            "Amort (years)",
            "Monthly Payment (est)",
            "DSCR Req",
            "Collateral / PG",
            "Status",
            "Notes",
        ]),
        "funding_equity": _empty_df([
            "Partner / Investor",
            "Equity Amount",
            "Ownership (%)",
            "Pref Return (%)",
            "Distribution Split",
            "Role (Active/Passive)",
            "Control Rights",
            "Status",
            "Notes",
        ]),
        "quotes": _empty_df([
            "Category (GC/Equipment/Signage/Arch/Permits)",
            "Vendor",
            "Quote Amount",
            "Scope Included",
            "Exclusions",
            "Contingency Included (Y/N)",
            "Timeline (weeks)",
            "Status",
            "Notes",
        ]),
        "leases": _empty_df([
            "Property / Landlord",
            "Rent (Monthly)",
            "NNN / CAM",
            "Term (years)",
            "TI Allowance",
            "Free Rent (months)",
            "Escalation (%)",
            "Deposit",
            "Exclusivity",
            "Drive-thru / Parking",
            "Status",
            "Notes",
        ]),
        "selected_loan": 0.0,
        "selected_rate": 8.5,
        "selected_term": 10.0,
        "selected_rent": 0.0,
        "selected_nnn": 0.0,
        "selected_ti": 0.0,
        "total_quotes": 0.0,
        "working_cap_override": 50000.0,
        "contingency_pct_override": 0.10,
        "su_total_uses": 0.0,
        "su_total_sources": 0.0,
        "su_gap": 0.0,
        "su_net_buildout": 0.0,
    }

    ss = st_session()
    for k, v in defaults.items():
        if k not in ss:
            ss[k] = v


def add_row(df, columns):
    if df is None or df.empty:
        return pd.DataFrame([{c: "" for c in columns}], columns=columns)

    working_df = df.copy()
    for c in columns:
        if c not in working_df.columns:
            working_df[c] = ""

    working_df = working_df[columns]
    new = pd.DataFrame([{c: "" for c in columns}], columns=columns)
    return pd.concat([working_df, new], ignore_index=True)


def delete_row(df):
    if df is None or df.empty:
        return df
    return df.iloc[:-1].copy()


def _sum_numeric(series):
    return pd.to_numeric(series, errors="coerce").fillna(0).sum()


def _safe_float(value, default=0.0):
    try:
        if value is None or value == "":
            return float(default)
        return float(value)
    except (TypeError, ValueError):
        return float(default)


def calc_monthly_debt_payment(principal, annual_rate_pct, term_years):
    principal = _safe_float(principal, 0.0)
    annual_rate_pct = _safe_float(annual_rate_pct, 0.0)
    term_years = _safe_float(term_years, 0.0)

    if principal <= 0 or term_years <= 0:
        return 0.0

    monthly_rate = annual_rate_pct / 100 / 12
    n = int(term_years * 12)

    if n <= 0:
        return 0.0

    if monthly_rate == 0:
        return principal / n

    return principal * (monthly_rate * (1 + monthly_rate) ** n) / (((1 + monthly_rate) ** n) - 1)


def calc_sources_uses(ss):
    uses_quotes = _safe_float(ss.get("total_quotes", 0.0))
    ti = _safe_float(ss.get("selected_ti", 0.0))
    net_buildout = max(uses_quotes - ti, 0.0)

    working_cap = _safe_float(ss.get("working_cap_override", 50000.0), 50000.0)
    contingency_pct = _safe_float(ss.get("contingency_pct_override", 0.10), 0.10)
    contingency = contingency_pct * net_buildout

    total_uses = net_buildout + working_cap + contingency

    debt = _safe_float(ss.get("selected_loan", 0.0))

    eq_df = ss.get("funding_equity", pd.DataFrame())
    equity = 0.0
    if isinstance(eq_df, pd.DataFrame) and not eq_df.empty and "Equity Amount" in eq_df.columns:
        equity = float(_sum_numeric(eq_df["Equity Amount"]))

    total_sources = debt + equity

    debt_payment = calc_monthly_debt_payment(
        ss.get("selected_loan", 0.0),
        ss.get("selected_rate", 8.5),
        ss.get("selected_term", 10),
    )

    selected_rent = _safe_float(ss.get("selected_rent", 0.0))
    selected_nnn = _safe_float(ss.get("selected_nnn", 0.0))
    monthly_occupancy = selected_rent + selected_nnn

    return {
        "uses_quotes": float(uses_quotes),
        "ti": float(ti),
        "net_buildout": float(net_buildout),
        "working_cap": float(working_cap),
        "contingency_pct": float(contingency_pct),
        "contingency": float(contingency),
        "total_uses": float(total_uses),
        "debt": float(debt),
        "equity": float(equity),
        "total_sources": float(total_sources),
        "gap": float(total_uses - total_sources),
        "debt_payment": float(debt_payment),
        "monthly_occupancy": float(monthly_occupancy),
    }
