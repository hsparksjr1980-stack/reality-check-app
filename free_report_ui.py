# free_report_ui.py

from __future__ import annotations

import io
import os
from datetime import datetime

import streamlit as st
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen import canvas

from ui_styles import close_shell, open_shell, render_page_header, render_section_intro


def _safe_score(val):
    return "—" if val is None else f"{float(val):.1f}"


def _score_band(score):
    if score is None:
        return "neutral"
    if score >= 78:
        return "good"
    if score >= 58:
        return "caution"
    return "bad"


def _money(x):
    return f"${x:,.0f}"


def _get_logo_path():
    base = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base, "logo.png")


def _get_data():
    days = st.session_state.get("days_custom", 365)

    avg_ticket = st.session_state.get("avg_ticket", 0.0)
    tx_per_day = st.session_state.get("tx_per_day", 0.0)

    annual_revenue = avg_ticket * tx_per_day * days
    monthly_revenue = annual_revenue / 12 if annual_revenue else 0.0

    wage = st.session_state.get("wage", 0.0)
    staff_per_hour = st.session_state.get("staff_per_hour", 0.0)
    hours_open_daily = st.session_state.get("hours_open_daily", 0.0)
    payroll_tax_pct = st.session_state.get("payroll_tax_pct", 0.0) / 100

    labor_hours_per_day = staff_per_hour * hours_open_daily
    monthly_labor = wage * labor_hours_per_day * (days / 12)
    monthly_payroll_tax = monthly_labor * payroll_tax_pct

    base_rent = st.session_state.get("base_rent", 0.0)
    cam = st.session_state.get("cam", 0.0)
    monthly_occupancy = base_rent + cam

    electric = st.session_state.get("electric", 0.0)
    gas = st.session_state.get("gas", 0.0)
    water = st.session_state.get("water", 0.0)
    sewer = st.session_state.get("sewer", 0.0)
    trash = st.session_state.get("trash", 0.0)
    internet = st.session_state.get("internet", 0.0)
    phone = st.session_state.get("phone", 0.0)
    workers_comp = st.session_state.get("workers_comp", 0.0)
    property_ins = st.session_state.get("property_ins", 0.0)
    tech = st.session_state.get("tech", 0.0)
    repairs = st.session_state.get("repairs", 0.0)
    admin_misc = st.session_state.get("admin_misc", 0.0)
    owner_comp = st.session_state.get("owner_comp", 0.0)

    monthly_other = (
        electric
        + gas
        + water
        + sewer
        + trash
        + internet
        + phone
        + workers_comp
        + property_ins
        + tech
        + repairs
        + admin_misc
        + owner_comp
    )

    actual_cogs_pct = st.session_state.get("actual_cogs_pct", 0.0) / 100
    actual_royalty_pct = st.session_state.get("actual_royalty_pct", 0.0) / 100
    actual_marketing_pct = st.session_state.get("actual_marketing_pct", 0.0) / 100
    merchant_pct = st.session_state.get("merchant_pct", 0.0) / 100
    leakage_pct = st.session_state.get("leakage_pct", 0.0) / 100

    your_year1 = {
        "Revenue": annual_revenue,
        "COGS": monthly_revenue * actual_cogs_pct * 12,
        "Labor": (monthly_labor + monthly_payroll_tax) * 12,
        "Occupancy": monthly_occupancy * 12,
        "Royalty": monthly_revenue * actual_royalty_pct * 12,
        "Marketing": monthly_revenue * actual_marketing_pct * 12,
        "Other": (
            monthly_other
            + (monthly_revenue * merchant_pct)
            + (monthly_revenue * leakage_pct)
        )
        * 12,
    }
    your_year1["EBITDA"] = (
        your_year1["Revenue"]
        - your_year1["COGS"]
        - your_year1["Labor"]
        - your_year1["Occupancy"]
        - your_year1["Royalty"]
        - your_year1["Marketing"]
        - your_year1["Other"]
    )

    fdd_revenue = st.session_state.get("fdd_revenue", 0.0)
    fdd_cogs_pct = st.session_state.get("fdd_cogs_pct", 0.0) / 100
    fdd_labor_pct = st.session_state.get("fdd_labor_pct", 0.0) / 100
    fdd_occupancy_pct = st.session_state.get("fdd_occupancy_pct", 0.0) / 100
    fdd_royalty_pct = st.session_state.get("fdd_royalty_pct", 0.0) / 100
    fdd_marketing_pct = st.session_state.get("fdd_marketing_pct", 0.0) / 100
    fdd_other_pct = st.session_state.get("fdd_other_pct", 0.0) / 100

    fdd_year1 = {
        "Revenue": fdd_revenue,
        "COGS": fdd_revenue * fdd_cogs_pct,
        "Labor": fdd_revenue * fdd_labor_pct,
        "Occupancy": fdd_revenue * fdd_occupancy_pct,
        "Royalty": fdd_revenue * fdd_royalty_pct,
        "Marketing": fdd_revenue * fdd_marketing_pct,
        "Other": fdd_revenue * fdd_other_pct,
    }
    fdd_year1["EBITDA"] = (
        fdd_year1["Revenue"]
        - fdd_year1["COGS"]
        - fdd_year1["Labor"]
        - fdd_year1["Occupancy"]
        - fdd_year1["Royalty"]
        - fdd_year1["Marketing"]
        - fdd_year1["Other"]
    )

    return {
        "name": st.session_state.get("full_name", ""),
        "franchise": st.session_state.get("franchise_name", ""),
        "date": datetime.now().strftime("%Y-%m-%d"),
        "scores": {
            "Reality Check": st.session_state.get("readiness_score"),
            "Concept Validation": st.session_state.get("concept_score"),
            "Financial Model": st.session_state.get("financial_score"),
        },
        "fdd_year1": fdd_year1,
        "your_year1": your_year1,
    }


def _create_pdf(data):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=LETTER)

    width, height = LETTER
    y = height - 50

    c.setFillColor(HexColor("#DDDDDD"))
    c.setFont("Helvetica-Bold", 40)
    c.saveState()
    c.translate(width / 2, height / 2)
    c.rotate(30)
    c.drawCentredString(0, 0, "FREE REPORT")
    c.restoreState()

    logo_path = _get_logo_path()
    if os.path.exists(logo_path):
        try:
            c.drawImage(
                logo_path,
                50,
                y - 5,
                width=140,
                height=40,
                preserveAspectRatio=True,
                mask="auto",
            )
        except Exception:
            pass

    c.setFillColor(HexColor("#2E6BE6"))
    c.setFont("Helvetica-Bold", 18)
    c.drawRightString(width - 50, y, "Free Report")

    y -= 30
    c.setFillColor(HexColor("#444444"))
    c.setFont("Helvetica", 10)
    c.drawString(50, y, f"Prepared for: {data['name'] or '—'}")
    y -= 15
    c.drawString(50, y, f"Concept: {data['franchise'] or '—'}")
    y -= 15
    c.drawString(50, y, f"Date: {data['date']}")
    y -= 25

    c.setFillColor(HexColor("#000000"))
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Score Summary")
    y -= 20

    for k, v in data["scores"].items():
        c.setFont("Helvetica", 10)
        c.drawString(50, y, f"{k}: {_safe_score(v)}")
        y -= 15

    y -= 15
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Basic P&L vs FDD")
    y -= 18

    c.setFont("Helvetica-Bold", 9)
    c.drawString(50, y, "Line Item")
    c.drawString(180, y, "FDD P&L")
    c.drawString(300, y, "Your Assumptions")
    c.drawString(460, y, "Difference")
    y -= 14

    c.setFont("Helvetica", 9)
    for line in [
        "Revenue",
        "COGS",
        "Labor",
        "Occupancy",
        "Royalty",
        "Marketing",
        "Other",
        "EBITDA",
    ]:
        fdd_val = data["fdd_year1"].get(line, 0.0)
        your_val = data["your_year1"].get(line, 0.0)
        diff = your_val - fdd_val

        c.drawString(50, y, line)
        c.drawRightString(270, y, _money(fdd_val))
        c.drawRightString(430, y, _money(your_val))
        c.drawRightString(560, y, _money(diff))
        y -= 14

    c.save()
    pdf = buffer.getvalue()
    buffer.close()
    return pdf


def _inject_styles():
    st.markdown(
        """
        <style>
        .fr-card {
            border: 1px solid #e5e7eb;
            border-radius: 20px;
            padding: 1rem;
            background: #ffffff;
            box-shadow: 0 8px 24px rgba(17, 24, 39, 0.06);
        }
        .fr-label {
            font-size: 0.72rem;
            font-weight: 700;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            color: #6b7280;
            margin-bottom: 0.35rem;
        }
        .fr-score {
            font-size: 1.5rem;
            font-weight: 800;
            line-height: 1.1;
            color: #111827;
            margin-bottom: 0.2rem;
        }
        .fr-note {
            font-size: 0.92rem;
            line-height: 1.55;
            color: #4b5563;
        }
        .fr-good {
            border-color: rgba(22, 163, 74, 0.22);
            background: linear-gradient(180deg, rgba(22, 163, 74, 0.06), #ffffff);
        }
        .fr-caution {
            border-color: rgba(217, 119, 6, 0.22);
            background: linear-gradient(180deg, rgba(217, 119, 6, 0.06), #ffffff);
        }
        .fr-bad {
            border-color: rgba(220, 38, 38, 0.22);
            background: linear-gradient(180deg, rgba(220, 38, 38, 0.06), #ffffff);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_free_report():
    _inject_styles()
    data = _get_data()

    open_shell()

    render_page_header(
        eyebrow="Output — Free Report",
        title="Review an early summary of your assessment so far.",
        subtitle=(
            "This report gives you a preliminary view of current scoring and a basic "
            "comparison between your model assumptions and the FDD-style unit economics."
        ),
        wide=True,
    )

    st.markdown('<div class="rc-gap-lg"></div>', unsafe_allow_html=True)

    logo_path = _get_logo_path()
    if os.path.exists(logo_path):
        st.image(logo_path, width=180)
        st.markdown('<div class="rc-gap-md"></div>', unsafe_allow_html=True)

    render_section_intro(
        title="Score summary",
        body="These scores reflect your current inputs and should be treated as directional, not final.",
    )

    st.markdown('<div class="rc-gap-md"></div>', unsafe_allow_html=True)

    cols = st.columns(3, gap="medium")
    for col, (label, score) in zip(cols, data["scores"].items()):
        band = _score_band(score)
        band_class = {
            "good": "fr-good",
            "caution": "fr-caution",
            "bad": "fr-bad",
        }.get(band, "")

        with col:
            st.markdown(
                f"""
                <div class="fr-card {band_class}">
                    <div class="fr-label">{label}</div>
                    <div class="fr-score">{_safe_score(score)}</div>
                    <div class="fr-note">Current directional signal based on available inputs.</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown('<div class="rc-gap-lg"></div>', unsafe_allow_html=True)

    render_section_intro(
        title="What this means",
        body=(
            "This report reflects your current alignment across personal readiness, "
            "concept quality, and whether the economics may work under your present assumptions."
        ),
    )

    st.markdown('<div class="rc-gap-md"></div>', unsafe_allow_html=True)

    st.info("This is not a final decision. It is an early signal based on the work completed so far.")

    st.markdown('<div class="rc-gap-lg"></div>', unsafe_allow_html=True)

    render_section_intro(
        title="Basic P&L vs. FDD",
        body="This is a simple comparison between the FDD-style unit economics and the assumptions in your current model.",
    )

    st.markdown('<div class="rc-gap-md"></div>', unsafe_allow_html=True)

    rows = []
    for line in [
        "Revenue",
        "COGS",
        "Labor",
        "Occupancy",
        "Royalty",
        "Marketing",
        "Other",
        "EBITDA",
    ]:
        fdd_val = data["fdd_year1"].get(line, 0.0)
        your_val = data["your_year1"].get(line, 0.0)
        rows.append(
            {
                "Line Item": line,
                "FDD P&L": _money(fdd_val),
                "Your Assumptions": _money(your_val),
                "Difference": _money(your_val - fdd_val),
            }
        )

    st.table(rows)

    st.markdown('<div class="rc-gap-lg"></div>', unsafe_allow_html=True)

    pdf = _create_pdf(data)

    st.download_button(
        "Download Free Report (PDF)",
        pdf,
        file_name="free_report.pdf",
        mime="application/pdf",
        use_container_width=True,
        type="primary",
    )

    st.markdown('<div class="rc-gap-md"></div>', unsafe_allow_html=True)

    if st.button("Continue", use_container_width=True, type="primary"):
        st.session_state["current_page"] = "Plans & Support"
        st.rerun()

    close_shell()
