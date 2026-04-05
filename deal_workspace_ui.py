# deal_workspace_ui.py

from __future__ import annotations

import pandas as pd
import streamlit as st

from deal_workspace_logic import (
    add_row,
    calc_sources_uses,
    delete_row,
    init_workspace_state,
)
from ui_styles import (
    close_shell,
    open_shell,
    render_page_header,
    render_section_intro,
)


def _ensure_notes_state() -> None:
    if "workspace_notes" not in st.session_state:
        st.session_state["workspace_notes"] = pd.DataFrame(
            columns=[
                "Priority",
                "Category",
                "Related Section",
                "Note / Follow-Up",
                "Owner",
                "Status",
            ]
        )

    if "workspace_general_notes" not in st.session_state:
        st.session_state["workspace_general_notes"] = ""


def _normalize_df(df: pd.DataFrame | None, columns: list[str]) -> pd.DataFrame:
    if df is None or not isinstance(df, pd.DataFrame):
        return pd.DataFrame(columns=columns)

    working = df.copy()

    for col in columns:
        if col not in working.columns:
            working[col] = ""

    return working[columns]


def _save_workspace_message() -> None:
    st.success("Workspace changes saved to this session.")


def _render_tab_intro(title: str, body: str) -> None:
    render_section_intro(title=title, body=body)
    st.markdown('<div class="rc-gap-md"></div>', unsafe_allow_html=True)


def _table_editor(state_key: str, columns: list[str], title: str) -> None:
    st.markdown(f"### {title}")
    st.caption(
        "Press Enter after editing a cell so the value is committed before switching tabs or pages."
    )

    df = _normalize_df(st.session_state.get(state_key), columns)

    edited = st.data_editor(
        df,
        num_rows="dynamic",
        use_container_width=True,
        hide_index=True,
        key=f"editor_{state_key}",
    )

    st.session_state[state_key] = edited.copy()

    c1, c2, c3 = st.columns(3, gap="medium")

    with c1:
        if st.button(
            f"Add row to {title}",
            key=f"add_{state_key}",
            use_container_width=True,
        ):
            st.session_state[state_key] = add_row(
                st.session_state[state_key],
                columns,
            )
            st.rerun()

    with c2:
        if st.button(
            "Delete last row",
            key=f"del_{state_key}",
            use_container_width=True,
        ):
            st.session_state[state_key] = delete_row(st.session_state[state_key])
            st.rerun()

    with c3:
        if st.button(
            "Save table changes",
            key=f"save_{state_key}",
            use_container_width=True,
            type="primary",
        ):
            st.session_state[state_key] = edited.copy()
            _save_workspace_message()


def _render_notes_tab() -> None:
    _render_tab_intro(
        "Notes & Follow-Ups",
        "Track open items, risks, reminders, and anything that needs a follow-up decision.",
    )

    notes_cols = [
        "Priority",
        "Category",
        "Related Section",
        "Note / Follow-Up",
        "Owner",
        "Status",
    ]
    _table_editor("workspace_notes", notes_cols, "Flagged Notes")

    ndf = _normalize_df(st.session_state.get("workspace_notes"), notes_cols)

    if not ndf.empty:
        open_count = (
            ndf["Status"]
            .fillna("")
            .astype(str)
            .str.strip()
            .str.lower()
            .isin(["open", "todo", "to do", "follow up", "in progress"])
            .sum()
        )

        high_count = (
            ndf["Priority"]
            .fillna("")
            .astype(str)
            .str.strip()
            .str.lower()
            .isin(["high", "urgent"])
            .sum()
        )

        c1, c2 = st.columns(2, gap="medium")
        with c1:
            st.metric("Open Notes", int(open_count))
        with c2:
            st.metric("High Priority", int(high_count))

        st.markdown('<div class="rc-gap-md"></div>', unsafe_allow_html=True)
        st.markdown("### Filtered View")

        f1, f2 = st.columns(2, gap="large")
        with f1:
            status_options = ["All"] + sorted(
                [
                    x
                    for x in ndf["Status"].fillna("").astype(str).unique().tolist()
                    if x.strip() != ""
                ]
            )
            selected_status = st.selectbox(
                "Filter by Status",
                status_options,
                key="workspace_notes_status_filter",
            )

        with f2:
            category_options = ["All"] + sorted(
                [
                    x
                    for x in ndf["Category"].fillna("").astype(str).unique().tolist()
                    if x.strip() != ""
                ]
            )
            selected_category = st.selectbox(
                "Filter by Category",
                category_options,
                key="workspace_notes_category_filter",
            )

        filtered = ndf.copy()
        if selected_status != "All":
            filtered = filtered[
                filtered["Status"].fillna("").astype(str) == selected_status
            ]
        if selected_category != "All":
            filtered = filtered[
                filtered["Category"].fillna("").astype(str) == selected_category
            ]

        st.dataframe(filtered, use_container_width=True, hide_index=True)

    st.markdown('<div class="rc-gap-lg"></div>', unsafe_allow_html=True)
    st.markdown("### General Notes")
    general_notes = st.text_area(
        "Use this for broader notes that do not belong to one specific row.",
        value=st.session_state.get("workspace_general_notes", ""),
        height=180,
        key="workspace_general_notes_box",
    )
    st.session_state["workspace_general_notes"] = general_notes

    if st.button(
        "Save general notes",
        key="save_general_notes",
        use_container_width=True,
        type="primary",
    ):
        st.session_state["workspace_general_notes"] = general_notes
        _save_workspace_message()


def render_deal_workspace() -> None:
    init_workspace_state()
    _ensure_notes_state()

    open_shell()

    render_page_header(
        eyebrow="Execution — Deal Workspace",
        title="Organize the deal details in one working area.",
        subtitle=(
            "Track funding, quotes, lease terms, sources and uses, and follow-up notes "
            "without changing the underlying worksheet flow."
        ),
        wide=True,
    )

    st.markdown('<div class="rc-gap-lg"></div>', unsafe_allow_html=True)

    tabs = st.tabs(["Funding", "Quotes", "Lease", "Sources & Uses", "Notes"])

    with tabs[0]:
        _render_tab_intro(
            "Funding",
            "Track lender options, equity sources, and the selected structure you want used in the downstream modeling.",
        )

        st.markdown("### Debt (Lenders)")
        debt_cols = [
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
        ]
        _table_editor("funding_debt", debt_cols, "Lender Options")

        st.markdown('<div class="rc-gap-lg"></div>', unsafe_allow_html=True)

        st.markdown("### Equity (Partners / Investors)")
        eq_cols = [
            "Partner / Investor",
            "Equity Amount",
            "Ownership (%)",
            "Pref Return (%)",
            "Distribution Split",
            "Role (Active/Passive)",
            "Control Rights",
            "Status",
            "Notes",
        ]
        _table_editor("funding_equity", eq_cols, "Equity Stack")

        st.markdown('<div class="rc-gap-lg"></div>', unsafe_allow_html=True)

        st.markdown("### Selected Structure")
        st.info("Set the lender terms you want used in Sources & Uses and the Deal Model.")

        c1, c2, c3 = st.columns(3, gap="large")
        with c1:
            selected_loan = st.number_input(
                "Selected Loan Amount",
                min_value=0.0,
                value=float(st.session_state.get("selected_loan", 0.0)),
                key="selected_loan_input",
            )
        with c2:
            selected_rate = st.number_input(
                "Selected Rate (%)",
                min_value=0.0,
                value=float(st.session_state.get("selected_rate", 8.5)),
                key="selected_rate_input",
            )
        with c3:
            selected_term = st.number_input(
                "Selected Term (years)",
                min_value=0.0,
                value=float(st.session_state.get("selected_term", 10.0)),
                key="selected_term_input",
            )

        st.session_state["selected_loan"] = float(selected_loan)
        st.session_state["selected_rate"] = float(selected_rate)
        st.session_state["selected_term"] = float(selected_term)

        funding_note = st.text_area(
            "Quick funding note",
            value=st.session_state.get("funding_quick_note", ""),
            height=100,
            key="funding_quick_note_box",
        )
        st.session_state["funding_quick_note"] = funding_note

        if st.button(
            "Save funding changes",
            key="save_funding_changes",
            use_container_width=True,
            type="primary",
        ):
            st.session_state["selected_loan"] = float(selected_loan)
            st.session_state["selected_rate"] = float(selected_rate)
            st.session_state["selected_term"] = float(selected_term)
            st.session_state["funding_quick_note"] = funding_note
            _save_workspace_message()

    with tabs[1]:
        _render_tab_intro(
            "Quotes",
            "Capture buildout and vendor quotes so the workspace can carry cleaner cost assumptions forward.",
        )

        quote_cols = [
            "Category (GC/Equipment/Signage/Arch/Permits)",
            "Vendor",
            "Quote Amount",
            "Scope Included",
            "Exclusions",
            "Contingency Included (Y/N)",
            "Timeline (weeks)",
            "Status",
            "Notes",
        ]
        _table_editor("quotes", quote_cols, "Quotes")

        qdf = _normalize_df(st.session_state.get("quotes"), quote_cols)
        total_quotes = pd.to_numeric(
            qdf.get("Quote Amount", pd.Series(dtype=float)),
            errors="coerce",
        ).fillna(0).sum()

        st.session_state["total_quotes"] = float(total_quotes)

        st.markdown('<div class="rc-gap-md"></div>', unsafe_allow_html=True)
        st.markdown("### Totals")
        st.metric("Total Quotes", f"${total_quotes:,.0f}")

        quotes_note = st.text_area(
            "Quick quotes note",
            value=st.session_state.get("quotes_quick_note", ""),
            height=100,
            key="quotes_quick_note_box",
        )
        st.session_state["quotes_quick_note"] = quotes_note

        if st.button(
            "Save quotes changes",
            key="save_quotes_changes",
            use_container_width=True,
            type="primary",
        ):
            st.session_state["total_quotes"] = float(total_quotes)
            st.session_state["quotes_quick_note"] = quotes_note
            _save_workspace_message()

    with tabs[2]:
        _render_tab_intro(
            "Lease",
            "Compare lease options and select the rent structure you want carried into the model.",
        )

        lease_cols = [
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
        ]
        _table_editor("leases", lease_cols, "Lease Comparison")

        st.markdown('<div class="rc-gap-lg"></div>', unsafe_allow_html=True)

        st.markdown("### Selected Lease")
        c1, c2, c3 = st.columns(3, gap="large")
        with c1:
            sel_rent = st.number_input(
                "Selected Rent",
                min_value=0.0,
                value=float(st.session_state.get("selected_rent", 0.0)),
                key="selected_rent_input",
            )
        with c2:
            sel_nnn = st.number_input(
                "Selected NNN / CAM",
                min_value=0.0,
                value=float(st.session_state.get("selected_nnn", 0.0)),
                key="selected_nnn_input",
            )
        with c3:
            sel_ti = st.number_input(
                "Selected TI Allowance",
                min_value=0.0,
                value=float(st.session_state.get("selected_ti", 0.0)),
                key="selected_ti_input",
            )

        st.session_state["selected_rent"] = float(sel_rent)
        st.session_state["selected_nnn"] = float(sel_nnn)
        st.session_state["selected_ti"] = float(sel_ti)

        lease_note = st.text_area(
            "Quick lease note",
            value=st.session_state.get("lease_quick_note", ""),
            height=100,
            key="lease_quick_note_box",
        )
        st.session_state["lease_quick_note"] = lease_note

        if st.button(
            "Save lease changes",
            key="save_lease_changes",
            use_container_width=True,
            type="primary",
        ):
            st.session_state["selected_rent"] = float(sel_rent)
            st.session_state["selected_nnn"] = float(sel_nnn)
            st.session_state["selected_ti"] = float(sel_ti)
            st.session_state["lease_quick_note"] = lease_note
            _save_workspace_message()

    with tabs[3]:
        _render_tab_intro(
            "Sources & Uses",
            "Review the auto-calculated funding picture using the current quote, lease, debt, and equity selections.",
        )

        c_override1, c_override2 = st.columns(2, gap="large")
        with c_override1:
            working_cap = st.number_input(
                "Working Capital Override",
                min_value=0.0,
                value=float(st.session_state.get("working_cap_override", 50000.0)),
                step=1000.0,
                key="working_cap_override_input",
            )
        with c_override2:
            contingency_pct = st.number_input(
                "Contingency %",
                min_value=0.0,
                max_value=1.0,
                value=float(st.session_state.get("contingency_pct_override", 0.10)),
                step=0.01,
                format="%.2f",
                key="contingency_pct_override_input",
            )

        st.session_state["working_cap_override"] = float(working_cap)
        st.session_state["contingency_pct_override"] = float(contingency_pct)

        su = calc_sources_uses(st.session_state)

        c1, c2 = st.columns(2, gap="large")
        with c1:
            st.markdown("### Uses")
            st.write(f"- Buildout / Quotes: ${su['uses_quotes']:,.0f}")
            st.write(f"- Less TI Allowance: -${su['ti']:,.0f}")
            st.write(f"- Net Buildout: ${su['net_buildout']:,.0f}")
            st.write(f"- Working Capital: ${su['working_cap']:,.0f}")
            st.write(f"- Contingency: ${su['contingency']:,.0f}")
            st.markdown(f"**Total Uses: ${su['total_uses']:,.0f}**")

        with c2:
            st.markdown("### Sources")
            st.write(f"- Debt (Selected): ${su['debt']:,.0f}")
            st.write(f"- Equity (Partners): ${su['equity']:,.0f}")
            st.markdown(f"**Total Sources: ${su['total_sources']:,.0f}**")

        st.markdown('<div class="rc-gap-md"></div>', unsafe_allow_html=True)
        st.markdown("### Funding Gap")
        gap = su["gap"]
        if gap > 0:
            st.error(f"Funding Gap: ${gap:,.0f} (additional equity or debt needed)")
        else:
            st.success(f"Fully Funded. Excess: ${abs(gap):,.0f}")

        st.session_state["su_total_uses"] = su["total_uses"]
        st.session_state["su_total_sources"] = su["total_sources"]
        st.session_state["su_gap"] = su["gap"]
        st.session_state["su_net_buildout"] = su["net_buildout"]

        su_note = st.text_area(
            "Quick Sources & Uses note",
            value=st.session_state.get("su_quick_note", ""),
            height=100,
            key="su_quick_note_box",
        )
        st.session_state["su_quick_note"] = su_note

        if st.button(
            "Save Sources & Uses changes",
            key="save_su_changes",
            use_container_width=True,
            type="primary",
        ):
            st.session_state["working_cap_override"] = float(working_cap)
            st.session_state["contingency_pct_override"] = float(contingency_pct)
            st.session_state["su_quick_note"] = su_note
            st.session_state["su_total_uses"] = su["total_uses"]
            st.session_state["su_total_sources"] = su["total_sources"]
            st.session_state["su_gap"] = su["gap"]
            st.session_state["su_net_buildout"] = su["net_buildout"]
            _save_workspace_message()

    with tabs[4]:
        _render_notes_tab()

        st.markdown('<div class="rc-gap-lg"></div>', unsafe_allow_html=True)

    if st.button(
        "Open Execution Report",
        key="deal_workspace_open_execution_report",
        use_container_width=True,
        type="primary",
    ):
        st.session_state["current_page"] = "Execution Report"
        st.rerun()

    close_shell()
