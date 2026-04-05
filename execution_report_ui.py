# execution_report_ui.py

from __future__ import annotations

import io
import os
from datetime import datetime
from typing import Any

import pandas as pd
import streamlit as st
from reportlab.lib.colors import HexColor, black, grey
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.colors import HexColor

from ui_styles import (
    close_shell,
    open_shell,
    render_card,
    render_page_header,
    render_section_intro,
)


def _money(value: Any) -> str:
    try:
        return f"${float(value):,.0f}"
    except (TypeError, ValueError):
        return "—"


def _pct(value: Any) -> str:
    try:
        return f"{float(value) * 100:,.1f}%"
    except (TypeError, ValueError):
        return "—"


def _safe_text(value: Any) -> str:
    if value is None:
        return "—"
    text = str(value).strip()
    return text if text else "—"


def _safe_df(value: Any, columns: list[str] | None = None) -> pd.DataFrame:
    if isinstance(value, pd.DataFrame):
        df = value.copy()
    else:
        df = pd.DataFrame()

    if columns is None:
        return df

    for column in columns:
        if column not in df.columns:
            df[column] = ""

    return df[columns]


def _get_logo_path() -> str:
    base = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base, "logo.png")


def _truncate_df(df: pd.DataFrame, max_rows: int = 12) -> pd.DataFrame:
    if len(df) <= max_rows:
        return df
    return df.head(max_rows).copy()


def _format_table_df(df: pd.DataFrame) -> pd.DataFrame:
    formatted = df.copy()

    for col in formatted.columns:
        if pd.api.types.is_numeric_dtype(formatted[col]):
            formatted[col] = formatted[col].map(
                lambda x: f"{x:,.2f}" if pd.notna(x) else "—"
            )
        else:
            formatted[col] = formatted[col].fillna("").astype(str).replace("", "—")

    return formatted


def _get_monthly_pnls() -> dict[int, pd.DataFrame]:
    monthly = st.session_state.get("deal_model_monthly_pnls", {})
    if not isinstance(monthly, dict):
        return {}

    normalized: dict[int, pd.DataFrame] = {}
    for key, value in monthly.items():
        try:
            year_num = int(key)
        except (TypeError, ValueError):
            continue
        if isinstance(value, pd.DataFrame):
            normalized[year_num] = value.copy()

    return normalized


def _get_report_payload() -> dict[str, Any]:
    workspace_notes_cols = [
        "Priority",
        "Category",
        "Related Section",
        "Note / Follow-Up",
        "Owner",
        "Status",
    ]

    funding_debt_cols = [
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

    funding_equity_cols = [
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

    quotes_cols = [
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

    leases_cols = [
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

    payload = {
        "report_date": datetime.now().strftime("%Y-%m-%d"),
        "full_name": _safe_text(st.session_state.get("full_name")),
        "email": _safe_text(st.session_state.get("email")),
        "franchise_name": _safe_text(st.session_state.get("franchise_name")),
        "city_state": _safe_text(st.session_state.get("city_state")),
        "units_considered": _safe_text(st.session_state.get("units_considered")),
        "ownership_style": _safe_text(st.session_state.get("ownership_style")),
        "selected_loan": float(st.session_state.get("selected_loan", 0.0)),
        "selected_rate": float(st.session_state.get("selected_rate", 0.0)),
        "selected_term": float(st.session_state.get("selected_term", 0.0)),
        "selected_rent": float(st.session_state.get("selected_rent", 0.0)),
        "selected_nnn": float(st.session_state.get("selected_nnn", 0.0)),
        "selected_ti": float(st.session_state.get("selected_ti", 0.0)),
        "su_total_uses": float(st.session_state.get("su_total_uses", 0.0)),
        "su_total_sources": float(st.session_state.get("su_total_sources", 0.0)),
        "su_gap": float(st.session_state.get("su_gap", 0.0)),
        "su_net_buildout": float(st.session_state.get("su_net_buildout", 0.0)),
        "funding_quick_note": _safe_text(st.session_state.get("funding_quick_note")),
        "quotes_quick_note": _safe_text(st.session_state.get("quotes_quick_note")),
        "lease_quick_note": _safe_text(st.session_state.get("lease_quick_note")),
        "su_quick_note": _safe_text(st.session_state.get("su_quick_note")),
        "workspace_general_notes": _safe_text(st.session_state.get("workspace_general_notes")),
        "funding_debt": _safe_df(st.session_state.get("funding_debt"), funding_debt_cols),
        "funding_equity": _safe_df(st.session_state.get("funding_equity"), funding_equity_cols),
        "quotes": _safe_df(st.session_state.get("quotes"), quotes_cols),
        "leases": _safe_df(st.session_state.get("leases"), leases_cols),
        "workspace_notes": _safe_df(st.session_state.get("workspace_notes"), workspace_notes_cols),
        "buildout_tracker_df": _safe_df(st.session_state.get("buildout_tracker_df")),
        "target_open_date": _safe_text(st.session_state.get("target_open_date")),
        "launch_owner": _safe_text(st.session_state.get("launch_owner")),
        "launch_status": _safe_text(st.session_state.get("launch_status")),
        "launch_readiness_notes": _safe_text(st.session_state.get("launch_readiness_notes")),
        "deal_model_pnl": _safe_df(st.session_state.get("deal_model_pnl")),
        "deal_model_bs": _safe_df(st.session_state.get("deal_model_bs")),
        "deal_model_df": _safe_df(st.session_state.get("deal_model_df")),
        "deal_model_monthly_pnls": _get_monthly_pnls(),
        "deal_model_roi": st.session_state.get("deal_model_roi"),
        "deal_model_payback": st.session_state.get("deal_model_payback"),
        "deal_model_break_even_month": st.session_state.get("deal_model_break_even_month"),
        "deal_model_lowest_cash": st.session_state.get("deal_model_lowest_cash"),
        "deal_model_lowest_cash_month": st.session_state.get("deal_model_lowest_cash_month"),
        "deal_model_dscr": st.session_state.get("deal_model_dscr"),
        "deal_model_equity_at_risk": st.session_state.get("deal_model_equity_at_risk"),
        "deal_model_stabilized_monthly_net": st.session_state.get("deal_model_stabilized_monthly_net"),
        "financial_verdict": _safe_text(st.session_state.get("financial_verdict")),
    }

    return payload


def _draw_wrapped_text(
    pdf: canvas.Canvas,
    text: str,
    x: float,
    y: float,
    max_width: float,
    *,
    font_name: str = "Helvetica",
    font_size: int = 10,
    leading: int = 14,
) -> float:
    words = text.split()
    line = ""

    for word in words:
        trial = f"{line} {word}".strip()
        if stringWidth(trial, font_name, font_size) <= max_width:
            line = trial
        else:
            pdf.drawString(x, y, line)
            y -= leading
            line = word

    if line:
        pdf.drawString(x, y, line)
        y -= leading

    return y


def _new_page(pdf: canvas.Canvas, page_width: float, page_height: float) -> float:
    pdf.showPage()
    logo_path = _get_logo_path()

    if os.path.exists(logo_path):
        try:
            logo = ImageReader(logo_path)
            pdf.drawImage(
                logo,
                50,
                page_height - 55,
                width=140,
                height=40,
                preserveAspectRatio=True,
                mask="auto",
            )
        except Exception:
            pass

    pdf.setFont("Helvetica-Bold", 16)
    pdf.setFillColor(black)
    pdf.drawRightString(page_width - 50, page_height - 35, "Execution Report")
    pdf.setStrokeColor(HexColor("#E5E7EB"))
    pdf.line(50, page_height - 65, page_width - 50, page_height - 65)
    return page_height - 85


def _ensure_space(
    pdf: canvas.Canvas,
    y: float,
    needed: float,
    page_width: float,
    page_height: float,
) -> float:
    if y - needed < 60:
        return _new_page(pdf, page_width, page_height)
    return y


def _draw_section_title(
    pdf: canvas.Canvas,
    title: str,
    x: float,
    y: float,
    width: float,
) -> float:
    pdf.setStrokeColor(HexColor("#E5E7EB"))
    pdf.line(x, y + 6, x + width, y + 6)
    pdf.setFillColor(HexColor("#2E6BE6"))
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(x, y - 6, title)
    pdf.setFillColor(black)
    return y - 24


def _draw_key_value_lines(
    pdf: canvas.Canvas,
    items: list[tuple[str, str]],
    x: float,
    y: float,
    line_height: int = 14,
) -> float:
    pdf.setFont("Helvetica", 10)
    pdf.setFillColor(black)
    for label, value in items:
        pdf.drawString(x, y, f"{label}: {value}")
        y -= line_height
    return y


def _draw_table(
    pdf: canvas.Canvas,
    df: pd.DataFrame,
    x: float,
    y: float,
    page_width: float,
    page_height: float,
    *,
    title: str | None = None,
    max_rows: int = 12,
) -> float:
    if title:
        y = _ensure_space(pdf, y, 40, page_width, page_height)
        y = _draw_section_title(pdf, title, x, y, page_width - 100)

    working = _truncate_df(df, max_rows=max_rows)
    if working.empty:
        pdf.setFont("Helvetica", 10)
        pdf.drawString(x, y, "No data available.")
        return y - 16

    display = _format_table_df(working)
    columns = list(display.columns)
    row_height = 16
    table_width = page_width - 100
    col_width = table_width / max(len(columns), 1)

    y = _ensure_space(pdf, y, (len(display) + 3) * row_height, page_width, page_height)

    pdf.setFillColor(HexColor("#F3F4F6"))
    pdf.rect(x, y - row_height + 2, table_width, row_height, fill=1, stroke=0)

    pdf.setFillColor(black)
    pdf.setFont("Helvetica-Bold", 8)

    for idx, column in enumerate(columns):
        cell_x = x + (idx * col_width) + 2
        pdf.drawString(cell_x, y - 10, str(column)[:22])

    y -= row_height
    pdf.setFont("Helvetica", 8)

    for _, row in display.iterrows():
        y = _ensure_space(pdf, y, row_height + 8, page_width, page_height)
        for idx, column in enumerate(columns):
            cell_x = x + (idx * col_width) + 2
            pdf.drawString(cell_x, y - 10, str(row[column])[:22])
        y -= row_height

    if len(df) > len(working):
        pdf.setFont("Helvetica-Oblique", 8)
        pdf.setFillColor(grey)
        pdf.drawString(x, y, f"Showing first {len(working)} rows of {len(df)}.")
        y -= 14

    pdf.setFillColor(black)
    return y - 6


def _create_pdf(payload: dict[str, Any]) -> bytes:
    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=LETTER)
    page_width, page_height = LETTER
    left = 50
    usable_width = page_width - 100

    y = _new_page(pdf, page_width, page_height)

    pdf.setFont("Helvetica-Bold", 18)
    pdf.setFillColor(black)
    pdf.drawString(left, y, payload["franchise_name"])
    y -= 18

    pdf.setFont("Helvetica", 10)
    pdf.setFillColor(grey)
    pdf.drawString(left, y, f"Prepared for {payload['full_name']} on {payload['report_date']}")
    y -= 24

    y = _draw_section_title(pdf, "Deal Snapshot", left, y, usable_width)
    y = _draw_key_value_lines(
        pdf,
        [
            ("Client", payload["full_name"]),
            ("Email", payload["email"]),
            ("Location", payload["city_state"]),
            ("Units", payload["units_considered"]),
            ("Ownership Style", payload["ownership_style"]),
            ("Financial Verdict", payload["financial_verdict"]),
        ],
        left,
        y,
    )
    y -= 10

    y = _draw_section_title(pdf, "Selected Structure", left, y, usable_width)
    y = _draw_key_value_lines(
        pdf,
        [
            ("Selected Loan", _money(payload["selected_loan"])),
            ("Selected Rate", f"{payload['selected_rate']:.2f}%"),
            ("Selected Term", f"{payload['selected_term']:.1f} years"),
            ("Selected Rent", _money(payload["selected_rent"])),
            ("Selected NNN / CAM", _money(payload["selected_nnn"])),
            ("Selected TI", _money(payload["selected_ti"])),
            ("Total Uses", _money(payload["su_total_uses"])),
            ("Total Sources", _money(payload["su_total_sources"])),
            ("Funding Gap", _money(payload["su_gap"])),
            ("Net Buildout", _money(payload["su_net_buildout"])),
        ],
        left,
        y,
    )
    y -= 10

    y = _draw_section_title(pdf, "Deal Model Metrics", left, y, usable_width)
    y = _draw_key_value_lines(
        pdf,
        [
            ("ROI", _pct(payload["deal_model_roi"])),
            ("Payback", _safe_text(payload["deal_model_payback"])),
            ("Break-even Month", _safe_text(payload["deal_model_break_even_month"])),
            ("Lowest Cash", _money(payload["deal_model_lowest_cash"])),
            ("Lowest Cash Month", _safe_text(payload["deal_model_lowest_cash_month"])),
            ("DSCR", _safe_text(payload["deal_model_dscr"])),
            ("Equity at Risk", _money(payload["deal_model_equity_at_risk"])),
            ("Stabilized Monthly Net", _money(payload["deal_model_stabilized_monthly_net"])),
        ],
        left,
        y,
    )
    y -= 10

    y = _draw_table(
        pdf,
        payload["deal_model_pnl"],
        left,
        y,
        page_width,
        page_height,
        title="3-Year Annual Forecast",
        max_rows=20,
    )

    y = _draw_table(
        pdf,
        payload["deal_model_bs"],
        left,
        y,
        page_width,
        page_height,
        title="Balance Sheet Summary",
        max_rows=20,
    )

    y = _draw_table(
        pdf,
        payload["funding_debt"],
        left,
        y,
        page_width,
        page_height,
        title="Funding — Debt",
        max_rows=10,
    )

    y = _draw_table(
        pdf,
        payload["funding_equity"],
        left,
        y,
        page_width,
        page_height,
        title="Funding — Equity",
        max_rows=10,
    )

    y = _draw_table(
        pdf,
        payload["quotes"],
        left,
        y,
        page_width,
        page_height,
        title="Quotes",
        max_rows=10,
    )

    y = _draw_table(
        pdf,
        payload["leases"],
        left,
        y,
        page_width,
        page_height,
        title="Lease Comparison",
        max_rows=10,
    )

    y = _draw_table(
        pdf,
        payload["workspace_notes"],
        left,
        y,
        page_width,
        page_height,
        title="Workspace Notes",
        max_rows=10,
    )

    y = _ensure_space(pdf, y, 120, page_width, page_height)
    y = _draw_section_title(pdf, "Buildout & Launch Snapshot", left, y, usable_width)
    y = _draw_key_value_lines(
        pdf,
        [
            ("Target Open Date", payload["target_open_date"]),
            ("Launch Owner", payload["launch_owner"]),
            ("Launch Status", payload["launch_status"]),
        ],
        left,
        y,
    )
    y -= 8
    pdf.setFont("Helvetica-Bold", 10)
    pdf.drawString(left, y, "Launch Readiness Notes")
    y -= 14
    pdf.setFont("Helvetica", 10)
    y = _draw_wrapped_text(
        pdf,
        payload["launch_readiness_notes"],
        left,
        y,
        usable_width,
    )
    y -= 10

    y = _draw_table(
        pdf,
        payload["buildout_tracker_df"],
        left,
        y,
        page_width,
        page_height,
        title="Buildout & Launch Tracker",
        max_rows=20,
    )

    monthly_pnls = payload["deal_model_monthly_pnls"]
    for year in sorted(monthly_pnls.keys()):
        y = _draw_table(
            pdf,
            monthly_pnls[year],
            left,
            y,
            page_width,
            page_height,
            title=f"Year {year} Monthly Forecast",
            max_rows=20,
        )

    notes = [
        ("Funding Note", payload["funding_quick_note"]),
        ("Quotes Note", payload["quotes_quick_note"]),
        ("Lease Note", payload["lease_quick_note"]),
        ("Sources & Uses Note", payload["su_quick_note"]),
        ("General Workspace Notes", payload["workspace_general_notes"]),
    ]

    y = _ensure_space(pdf, y, 160, page_width, page_height)
    y = _draw_section_title(pdf, "Execution Notes", left, y, usable_width)
    pdf.setFont("Helvetica", 10)
    pdf.setFillColor(black)

    for label, text in notes:
        y = _ensure_space(pdf, y, 40, page_width, page_height)
        pdf.setFont("Helvetica-Bold", 10)
        pdf.drawString(left, y, label)
        y -= 14
        pdf.setFont("Helvetica", 10)
        y = _draw_wrapped_text(pdf, text, left, y, usable_width)

    pdf.setFont("Helvetica", 8)
    pdf.setFillColor(grey)
    pdf.drawCentredString(page_width / 2, 20, "Reality Check — Execution Report")

    pdf.save()
    pdf_bytes = buffer.getvalue()
    buffer.close()
    return pdf_bytes


def render_execution_report() -> None:
    payload = _get_report_payload()
    pdf_bytes = _create_pdf(payload)

    open_shell()

    render_page_header(
        eyebrow="Execution — Report",
        title="Generate a PDF for the deal workspace and model.",
        subtitle=(
            "This report combines funding structure, lease selections, sources and uses, "
            "workspace notes, buildout tracking, model metrics, and the 3-year forecast."
        ),
        wide=True,
    )

    st.markdown('<div class="rc-gap-lg"></div>', unsafe_allow_html=True)

    summary_col_1, summary_col_2, summary_col_3, summary_col_4 = st.columns(4, gap="medium")
    with summary_col_1:
        render_card(
            label="Funding gap",
            title=_money(payload["su_gap"]),
            body="Current gap between total sources and total uses.",
        )
    with summary_col_2:
        render_card(
            label="ROI",
            title=_pct(payload["deal_model_roi"]),
            body="Projected return on invested equity.",
        )
    with summary_col_3:
        render_card(
            label="Break-even",
            title=_safe_text(payload["deal_model_break_even_month"]),
            body="Break-even timing from the current deal model.",
        )
    with summary_col_4:
        render_card(
            label="Verdict",
            title=payload["financial_verdict"],
            body="Current directional read from the deal model.",
        )

    st.markdown('<div class="rc-gap-lg"></div>', unsafe_allow_html=True)

    render_section_intro(
        title="3-Year Annual Forecast",
        body="This section summarizes the annual P&L forecast across the full 3-year model.",
    )
    st.markdown('<div class="rc-gap-md"></div>', unsafe_allow_html=True)
    if payload["deal_model_pnl"].empty:
        st.info("No 3-year annual forecast is available yet. Build the deal model first.")
    else:
        st.dataframe(payload["deal_model_pnl"], use_container_width=True, hide_index=True)

    st.markdown('<div class="rc-gap-lg"></div>', unsafe_allow_html=True)

    render_section_intro(
        title="Monthly Forecast Detail",
        body="These views show the year-by-year monthly forecast when it has been built.",
    )
    st.markdown('<div class="rc-gap-md"></div>', unsafe_allow_html=True)

    monthly_pnls = payload["deal_model_monthly_pnls"]
    if not monthly_pnls:
        st.info("No monthly forecast detail is available yet. Build the deal model first.")
    else:
        for year in sorted(monthly_pnls.keys()):
            st.markdown(f"### Year {year}")
            st.dataframe(monthly_pnls[year], use_container_width=True, hide_index=True)
            st.markdown('<div class="rc-gap-md"></div>', unsafe_allow_html=True)

    st.markdown('<div class="rc-gap-lg"></div>', unsafe_allow_html=True)

    render_section_intro(
        title="Workspace Detail",
        body="These sections pull the current execution data directly from the workspace, model, and launch tracker.",
    )
    st.markdown('<div class="rc-gap-md"></div>', unsafe_allow_html=True)

    tab_funding, tab_quotes, tab_lease, tab_buildout, tab_notes = st.tabs(
        ["Funding", "Quotes", "Lease", "Buildout", "Notes"]
    )

    with tab_funding:
        st.markdown("### Debt")
        st.dataframe(payload["funding_debt"], use_container_width=True, hide_index=True)
        st.markdown('<div class="rc-gap-md"></div>', unsafe_allow_html=True)
        st.markdown("### Equity")
        st.dataframe(payload["funding_equity"], use_container_width=True, hide_index=True)

    with tab_quotes:
        st.dataframe(payload["quotes"], use_container_width=True, hide_index=True)

    with tab_lease:
        st.dataframe(payload["leases"], use_container_width=True, hide_index=True)

    with tab_buildout:
        st.markdown("### Launch Snapshot")
        c1, c2, c3 = st.columns(3, gap="medium")
        with c1:
            render_card(
                label="Target open date",
                title=payload["target_open_date"],
                body="Current target opening date from the launch tracker.",
            )
        with c2:
            render_card(
                label="Launch owner",
                title=payload["launch_owner"],
                body="Primary owner of the launch process.",
            )
        with c3:
            render_card(
                label="Launch status",
                title=payload["launch_status"],
                body="Current launch status from the tracker.",
            )

        st.markdown('<div class="rc-gap-md"></div>', unsafe_allow_html=True)
        st.markdown("### Launch Readiness Notes")
        st.write(payload["launch_readiness_notes"])

        st.markdown('<div class="rc-gap-md"></div>', unsafe_allow_html=True)
        st.markdown("### Buildout & Launch Tracker")
        if payload["buildout_tracker_df"].empty:
            st.info("No buildout tracker data is available yet.")
        else:
            st.dataframe(
                payload["buildout_tracker_df"],
                use_container_width=True,
                hide_index=True,
            )

    with tab_notes:
        st.markdown("### Workspace Notes")
        st.dataframe(payload["workspace_notes"], use_container_width=True, hide_index=True)
        st.markdown('<div class="rc-gap-md"></div>', unsafe_allow_html=True)
        st.markdown("### General Notes")
        st.write(payload["workspace_general_notes"])

    st.markdown('<div class="rc-gap-lg"></div>', unsafe_allow_html=True)

    st.download_button(
        "Download Execution Report (PDF)",
        data=pdf_bytes,
        file_name="execution_report.pdf",
        mime="application/pdf",
        use_container_width=True,
        type="primary",
    )

    close_shell()
