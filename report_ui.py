# report_ui.py

from __future__ import annotations

import io
import os
from datetime import datetime

import streamlit as st
from reportlab.lib.colors import HexColor, black, grey
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas

from decision_engine import build_decision_packet
from ui_styles import (
    close_shell,
    open_shell,
    render_card,
    render_page_header,
    render_section_intro,
)


def _safe_score(value):
    return "—" if value is None else f"{float(value):.1f}"


def _score_value(value):
    return None if value is None else float(value)


def _score_band(score):
    if score is None:
        return "neutral"
    if score >= 78:
        return "good"
    if score >= 58:
        return "caution"
    return "bad"


def _band_colors(score):
    band = _score_band(score)
    if band == "good":
        return {
            "border": "#3cb371",
            "bg": "rgba(60,179,113,.10)",
            "hex_bg": HexColor("#EAF7F0"),
        }
    if band == "caution":
        return {
            "border": "#ffc107",
            "bg": "rgba(255,193,7,.10)",
            "hex_bg": HexColor("#FFF8E1"),
        }
    if band == "bad":
        return {
            "border": "#dc3545",
            "bg": "rgba(220,53,69,.10)",
            "hex_bg": HexColor("#FCEBEC"),
        }
    return {
        "border": "#888888",
        "bg": "rgba(140,140,140,.08)",
        "hex_bg": HexColor("#F3F3F3"),
    }


def _get_logo_path():
    base = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base, "logo.png")


def _build_executive_summary(report_data: dict) -> str:
    return (
        f"This evaluation resulted in a {report_data['verdict']}. "
        f"The overall score of {report_data['overall_score_display']} reflects a combination of "
        f"readiness, concept fit, financial assumptions, post-discovery validation, and pressure testing. "
        f"The recorded decision at this stage is: {report_data['final_choice']}. "
        f"This summary should be treated as a directional assessment rather than a guarantee of outcome. "
        f"The purpose is to help clarify whether the opportunity appears grounded enough to move forward, "
        f"or whether the current facts suggest a more cautious path."
    )


def _get_report_data() -> dict:
    packet = build_decision_packet()

    readiness = st.session_state.get("readiness_score")
    concept = st.session_state.get("concept_score")
    financial = st.session_state.get("financial_score")
    post = st.session_state.get("post_discovery_score")
    pressure = st.session_state.get("pressure_test_score")

    overall_raw = packet.get("final_score", packet.get("weighted_score"))
    verdict = packet.get("master_verdict", packet.get("recommendation", "Decision Summary"))

    move_forward = st.session_state.get("move_forward", False)
    walk_away = st.session_state.get("walk_away", False)

    final_choice = "Not recorded"
    if move_forward:
        final_choice = "Yes — Moving Forward"
    elif walk_away:
        final_choice = "No — Walking Away"

    strengths = packet.get("strengths", [])
    if not strengths:
        strengths = []

        if readiness is not None and readiness >= 58:
            strengths.append("Reality Check suggests some degree of personal and operational readiness.")
        if concept is not None and concept >= 58:
            strengths.append("Concept Validation suggests the business model may fit reasonably well.")
        if financial is not None and financial >= 58:
            strengths.append("Financial Model suggests the economics may work under the current assumptions.")
        if post is not None and post >= 58:
            strengths.append("Post-Discovery suggests more of the deal is grounded in facts rather than early assumptions.")
        if pressure is not None and pressure >= 58:
            strengths.append("Pressure Test suggests the deal may hold up under stress better than a fragile deal would.")

    risks = []
    for item in packet.get("key_risks", []):
        if item not in risks:
            risks.append(item)
    for item in packet.get("conditions", []):
        if item not in risks:
            risks.append(item)
    for item in packet.get("risks", []):
        if item not in risks:
            risks.append(item)

    if not risks:
        if readiness is not None and readiness < 58:
            risks.append("Reality Check suggests the ownership, time, or risk profile may not align cleanly with the business demands.")
        if concept is not None and concept < 58:
            risks.append("Concept Validation suggests the concept may not fit as cleanly as it first appears.")
        if financial is not None and financial < 58:
            risks.append("Financial Model suggests the numbers may be too thin under the current assumptions.")
        if post is not None and post < 58:
            risks.append("Post-Discovery suggests too many unknowns or weak conditions remain.")
        if pressure is not None and pressure < 58:
            risks.append("Pressure Test suggests the deal may break down when assumptions are stressed.")

    data = {
        "full_name": st.session_state.get("full_name", ""),
        "email": st.session_state.get("email", ""),
        "city_state": st.session_state.get("city_state", ""),
        "franchise_name": st.session_state.get("franchise_name", ""),
        "units_considered": st.session_state.get("units_considered", ""),
        "ownership_style": st.session_state.get("ownership_style", ""),
        "verdict": verdict,
        "final_choice": final_choice,
        "overall_score_display": _safe_score(overall_raw),
        "overall_score_value": _score_value(overall_raw),
        "scores": {
            "Reality Check": {
                "display": _safe_score(readiness),
                "value": _score_value(readiness),
            },
            "Concept Validation": {
                "display": _safe_score(concept),
                "value": _score_value(concept),
            },
            "Financial Model": {
                "display": _safe_score(financial),
                "value": _score_value(financial),
            },
            "Post-Discovery": {
                "display": _safe_score(post),
                "value": _score_value(post),
            },
            "Pressure Test": {
                "display": _safe_score(pressure),
                "value": _score_value(pressure),
            },
        },
        "strengths": strengths[:8],
        "risks": risks[:10],
        "premium_access": st.session_state.get("premium_access", False),
        "move_forward": move_forward,
        "walk_away": walk_away,
        "report_date": datetime.now().strftime("%Y-%m-%d"),
        "pro_sections": {},
    }

    if data["premium_access"]:
        data["pro_sections"] = {
            "deal_model": {
                "Target Monthly Revenue": st.session_state.get("fm_target_monthly_revenue"),
                "COGS %": st.session_state.get("fm_cogs_pct"),
                "Labor %": st.session_state.get("fm_labor_pct"),
                "Royalty %": st.session_state.get("fm_royalty_pct"),
                "Marketing %": st.session_state.get("fm_marketing_pct"),
                "Other Fixed Costs": st.session_state.get("fm_other_fixed"),
                "Ramp Months": st.session_state.get("fm_ramp_months"),
            },
            "stress_test": {
                "Buildout Too High": st.session_state.get("flag_buildout_too_high"),
                "Rent Too High": st.session_state.get("flag_rent_too_high"),
                "No Margin For Error": st.session_state.get("flag_no_margin_for_error"),
                "Major Unknowns Remaining": st.session_state.get("flag_major_unknowns_remaining"),
                "Unverified Unit Economics": st.session_state.get("flag_unverified_unit_economics"),
            },
        }

    return data


def _draw_wrapped_text(c, text, x, y, max_width, font_name="Helvetica", font_size=10, leading=14):
    words = text.split()
    line = ""
    for word in words:
        test_line = f"{line} {word}".strip()
        if stringWidth(test_line, font_name, font_size) <= max_width:
            line = test_line
        else:
            c.drawString(x, y, line)
            y -= leading
            line = word
    if line:
        c.drawString(x, y, line)
        y -= leading
    return y


def _draw_section_title(c, title, x, y, width):
    c.setStrokeColor(HexColor("#E6E6E6"))
    c.line(x, y + 6, x + width, y + 6)
    c.setFillColor(HexColor("#2E6BE6"))
    c.setFont("Helvetica-Bold", 12)
    c.drawString(x, y - 6, title)
    c.setFillColor(black)
    return y - 24


def _draw_bullets(c, items, x, y, max_width, font_size=10):
    c.setFont("Helvetica", font_size)
    c.setFillColor(black)
    if not items:
        c.drawString(x, y, "- None")
        return y - 14

    for item in items:
        y = _draw_wrapped_text(c, f"- {item}", x, y, max_width, "Helvetica", font_size, 14)
        if y < 72:
            c.showPage()
            y = 720
            c.setFont("Helvetica", font_size)
            c.setFillColor(black)
    return y


def _draw_score_box(c, x, y, w, h, label, value, score):
    colors = _band_colors(score)
    c.setFillColor(colors["hex_bg"])
    c.setStrokeColor(HexColor(colors["border"]))
    c.roundRect(x, y - h, w, h, 8, fill=1, stroke=1)

    c.setFillColor(grey)
    c.setFont("Helvetica", 8)
    c.drawString(x + 8, y - 14, label.upper())

    c.setFillColor(black)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(x + 8, y - 30, str(value))


def _add_free_watermark(c, width, height):
    c.saveState()
    c.setFillColor(HexColor("#DDDDDD"))
    c.setFont("Helvetica-Bold", 40)
    c.translate(width / 2, height / 2)
    c.rotate(35)
    c.drawCentredString(0, 0, "FREE VERSION")
    c.restoreState()


def _create_pdf(report_data: dict) -> bytes:
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=LETTER)
    width, height = LETTER

    left = 50
    right = 50
    usable_width = width - left - right
    y = height - 48

    if not report_data["premium_access"]:
        _add_free_watermark(c, width, height)

    logo_path = _get_logo_path()
    if os.path.exists(logo_path):
        try:
            logo = ImageReader(logo_path)
            c.drawImage(
                logo,
                left,
                y - 8,
                width=140,
                height=40,
                preserveAspectRatio=True,
                mask="auto",
            )
        except Exception:
            pass

    c.setFont("Helvetica-Bold", 18)
    c.setFillColor(black)
    c.drawRightString(width - right, y, "Reality Check")

    y -= 22

    c.setFont("Helvetica", 10)
    c.setFillColor(grey)
    c.drawRightString(width - right, y, f"Prepared on {report_data['report_date']}")

    y -= 18

    c.setStrokeColor(HexColor("#2E6BE6"))
    c.setLineWidth(2)
    c.line(left, y, width - right, y)

    y -= 20

    c.setFillColor(HexColor("#F7F9FC"))
    c.setStrokeColor(HexColor("#E3E8F0"))
    c.roundRect(left, y - 60, usable_width, 56, 10, fill=1, stroke=1)

    c.setFillColor(black)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(left + 12, y - 18, f"Concept: {report_data['franchise_name'] or '—'}")
    c.drawString(left + 12, y - 34, f"Client: {report_data['full_name'] or '—'}")
    c.drawString(left + 300, y - 18, f"Units: {report_data['units_considered'] or '—'}")
    c.drawString(left + 300, y - 34, f"Ownership: {report_data['ownership_style'] or '—'}")

    y -= 76

    y = _draw_section_title(c, "Decision Summary", left, y, usable_width)
    c.setFont("Helvetica", 10)
    c.setFillColor(black)
    c.drawString(left, y, f"Final Verdict: {report_data['verdict']}")
    y -= 14
    c.drawString(left, y, f"Final Choice: {report_data['final_choice']}")
    y -= 14
    c.drawString(left, y, f"Overall Score: {report_data['overall_score_display']}")
    y -= 24

    y = _draw_section_title(c, "Score Summary", left, y, usable_width)
    box_w = (usable_width - 20) / 3
    box_h = 42

    score_items = list(report_data["scores"].items()) + [
        (
            "Overall",
            {
                "display": report_data["overall_score_display"],
                "value": report_data["overall_score_value"],
            },
        )
    ]

    row1 = score_items[:3]
    row2 = score_items[3:6]
    x_positions = [left, left + box_w + 10, left + (box_w + 10) * 2]

    for x, (label, item) in zip(x_positions, row1):
        _draw_score_box(c, x, y, box_w, box_h, label, item["display"], item["value"])
    y -= 56

    for x, (label, item) in zip(x_positions, row2):
        _draw_score_box(c, x, y, box_w, box_h, label, item["display"], item["value"])
    y -= 64

    y = _draw_section_title(c, "What Looks Stronger", left, y, usable_width)
    y = _draw_bullets(c, report_data["strengths"], left, y, usable_width)
    y -= 12

    if y < 180:
        c.showPage()
        y = height - 48
        if not report_data["premium_access"]:
            _add_free_watermark(c, width, height)

    y = _draw_section_title(c, "What May Need Work", left, y, usable_width)
    y = _draw_bullets(c, report_data["risks"], left, y, usable_width)
    y -= 12

    if report_data["premium_access"]:
        if y < 220:
            c.showPage()
            y = height - 48

        y = _draw_section_title(c, "Executive Summary", left, y, usable_width)
        executive_summary = _build_executive_summary(report_data)
        y = _draw_wrapped_text(
            c,
            executive_summary,
            left,
            y,
            usable_width,
            font_name="Helvetica",
            font_size=10,
            leading=14,
        )
        y -= 16

        if y < 200:
            c.showPage()
            y = height - 48

        y = _draw_section_title(c, "Pro Section — Deal Model", left, y, usable_width)
        c.setFont("Helvetica", 10)
        c.setFillColor(black)
        for label, value in report_data["pro_sections"]["deal_model"].items():
            c.drawString(left, y, f"{label}: {value if value is not None else '—'}")
            y -= 14
            if y < 72:
                c.showPage()
                y = height - 48
                c.setFont("Helvetica", 10)

        y -= 12
        if y < 180:
            c.showPage()
            y = height - 48

        y = _draw_section_title(c, "Pro Section — Stress Test", left, y, usable_width)
        for label, value in report_data["pro_sections"]["stress_test"].items():
            display = "Yes" if value is True else "No" if value is False else "—"
            c.drawString(left, y, f"{label}: {display}")
            y -= 14
            if y < 72:
                c.showPage()
                y = height - 48
                c.setFont("Helvetica", 10)
    else:
        if y < 160:
            c.showPage()
            y = height - 48
            _add_free_watermark(c, width, height)

        y = _draw_section_title(c, "Upgrade Note", left, y, usable_width)
        y = _draw_wrapped_text(
            c,
            "This free report includes the summary view. Pro unlocks an executive summary, extended deal model detail, and stress test detail in the exported report.",
            left,
            y,
            usable_width,
            font_name="Helvetica",
            font_size=10,
            leading=14,
        )

    c.setFont("Helvetica", 8)
    c.setFillColor(grey)
    c.drawCentredString(width / 2, 20, "Reality Check — Franchise Decision System")

    c.save()
    pdf = buffer.getvalue()
    buffer.close()
    return pdf


def _inject_local_styles():
    st.markdown(
        """
        <style>
            .rr-score-card {
                border: 1px solid #e5e7eb;
                border-radius: 18px;
                background: #ffffff;
                box-shadow: 0 8px 24px rgba(17, 24, 39, 0.06);
                padding: 1rem;
                height: 100%;
            }

            .rr-score-label {
                font-size: 0.72rem;
                font-weight: 700;
                letter-spacing: 0.08em;
                text-transform: uppercase;
                color: #6b7280;
                margin-bottom: 0.25rem;
            }

            .rr-score-value {
                font-size: 1.35rem;
                font-weight: 800;
                line-height: 1.1;
                color: #111827;
            }

            .rr-score-good {
                border-color: rgba(60, 179, 113, 0.30);
                background: linear-gradient(180deg, rgba(60, 179, 113, 0.07), #ffffff);
            }

            .rr-score-caution {
                border-color: rgba(255, 193, 7, 0.34);
                background: linear-gradient(180deg, rgba(255, 193, 7, 0.08), #ffffff);
            }

            .rr-score-bad {
                border-color: rgba(220, 53, 69, 0.26);
                background: linear-gradient(180deg, rgba(220, 53, 69, 0.06), #ffffff);
            }

            .rr-action-card {
                background: #ffffff;
                border: 1px solid #e5e7eb;
                border-radius: 18px;
                box-shadow: 0 8px 24px rgba(17, 24, 39, 0.05);
                padding: 1rem;
                min-height: 112px;
            }

            .rr-action-title {
                font-size: 1rem;
                font-weight: 750;
                line-height: 1.3;
                color: #111827;
                margin-bottom: 0.3rem;
            }

            .rr-action-body {
                font-size: 0.92rem;
                line-height: 1.58;
                color: #4b5563;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def _render_score_summary(report_data: dict) -> None:
    score_items = list(report_data["scores"].items()) + [
        (
            "Overall",
            {
                "display": report_data["overall_score_display"],
                "value": report_data["overall_score_value"],
            },
        )
    ]

    row1 = st.columns(3, gap="medium")
    for col, (label, item) in zip(row1, score_items[:3]):
        band = _score_band(item["value"])
        band_class = f"rr-score-{band}" if band != "neutral" else ""
        with col:
            st.markdown(
                f"""
                <div class="rr-score-card {band_class}">
                    <div class="rr-score-label">{label}</div>
                    <div class="rr-score-value">{item["display"]}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown('<div class="rc-gap-md"></div>', unsafe_allow_html=True)

    row2 = st.columns(3, gap="medium")
    for col, (label, item) in zip(row2, score_items[3:6]):
        band = _score_band(item["value"])
        band_class = f"rr-score-{band}" if band != "neutral" else ""
        with col:
            st.markdown(
                f"""
                <div class="rr-score-card {band_class}">
                    <div class="rr-score-label">{label}</div>
                    <div class="rr-score-value">{item["display"]}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )


def render_report_screen():
    _inject_local_styles()
    report_data = _get_report_data()
    pdf_bytes = _create_pdf(report_data)

    open_shell()

    render_page_header(
        eyebrow="Output — Report",
        title="Generate a clean summary of the evaluation.",
        subtitle=(
            "This report brings together the current score rollup, final posture, and key areas "
            "that appear stronger or may still need work."
        ),
        wide=True,
    )

    st.markdown('<div class="rc-gap-lg"></div>', unsafe_allow_html=True)

    logo_path = _get_logo_path()
    if os.path.exists(logo_path):
        st.image(logo_path, width=180)
        st.markdown('<div class="rc-gap-md"></div>', unsafe_allow_html=True)

    summary_col_1, summary_col_2, summary_col_3 = st.columns(3, gap="medium")
    with summary_col_1:
        render_card(
            label="Overall score",
            title=report_data["overall_score_display"],
            body="Directional rollup of the current evaluation work.",
        )
    with summary_col_2:
        render_card(
            label="Final verdict",
            title=report_data["verdict"],
            body="Current recommendation based on the recorded analysis.",
        )
    with summary_col_3:
        render_card(
            label="Decision",
            title=report_data["final_choice"],
            body="Recorded decision status from the final decision step.",
        )

    st.markdown('<div class="rc-gap-lg"></div>', unsafe_allow_html=True)

    render_section_intro(
        title="Score summary",
        body="Use the score summary as a directional read. The value is in the pattern across sections, not just the number itself.",
    )

    st.markdown('<div class="rc-gap-md"></div>', unsafe_allow_html=True)

    _render_score_summary(report_data)

    st.markdown('<div class="rc-gap-lg"></div>', unsafe_allow_html=True)

    if report_data["premium_access"]:
        render_section_intro(
            title="Executive summary",
            body="A more consolidated read on the current evaluation and decision posture.",
        )
        st.markdown('<div class="rc-gap-md"></div>', unsafe_allow_html=True)
        st.write(_build_executive_summary(report_data))
    else:
        st.warning(
            "This free report includes the summary version. Pro unlocks an executive summary, extended deal model detail, and stress test detail in the PDF."
        )

    st.markdown('<div class="rc-gap-lg"></div>', unsafe_allow_html=True)

    stronger_col, weaker_col = st.columns(2, gap="large")

    with stronger_col:
        render_section_intro(
            title="What looks stronger",
            body="These are the factors currently supporting the opportunity more positively.",
        )
        st.markdown('<div class="rc-gap-sm"></div>', unsafe_allow_html=True)
        if report_data["strengths"]:
            for item in report_data["strengths"]:
                st.write(f"- {item}")
        else:
            st.write("- None")

    with weaker_col:
        render_section_intro(
            title="What may need work",
            body="These are the factors that may still need tighter scrutiny or better conditions.",
        )
        st.markdown('<div class="rc-gap-sm"></div>', unsafe_allow_html=True)
        if report_data["risks"]:
            for item in report_data["risks"]:
                st.write(f"- {item}")
        else:
            st.write("- None")

    if report_data["premium_access"]:
        st.markdown('<div class="rc-gap-lg"></div>', unsafe_allow_html=True)

        pro_col_1, pro_col_2 = st.columns(2, gap="large")

        with pro_col_1:
            render_section_intro(
                title="Pro detail — Deal Model",
                body="Current deal model inputs included in the report packet.",
            )
            st.markdown('<div class="rc-gap-sm"></div>', unsafe_allow_html=True)
            for label, value in report_data["pro_sections"]["deal_model"].items():
                st.write(f"- **{label}:** {value if value is not None else '—'}")

        with pro_col_2:
            render_section_intro(
                title="Pro detail — Stress Test",
                body="Current stress flags included in the report packet.",
            )
            st.markdown('<div class="rc-gap-sm"></div>', unsafe_allow_html=True)
            for label, value in report_data["pro_sections"]["stress_test"].items():
                display = "Yes" if value is True else "No" if value is False else "—"
                st.write(f"- **{label}:** {display}")

    st.markdown('<div class="rc-gap-lg"></div>', unsafe_allow_html=True)

    if report_data["move_forward"]:
        render_section_intro(
            title="Next step",
            body="You chose to move forward. Continue into the execution tools when you are ready.",
        )
        st.markdown('<div class="rc-gap-md"></div>', unsafe_allow_html=True)

        if st.button(
            "Continue to Deal Workspace",
            key="report_continue_to_deal_workspace",
            use_container_width=True,
            type="primary",
        ):
            st.session_state["current_page"] = "Deal Workspace"
            st.rerun()

        st.markdown('<div class="rc-gap-lg"></div>', unsafe_allow_html=True)

    render_section_intro(
        title="Report actions",
        body="Download the PDF now, or use the save and email placeholders for the live product workflow.",
    )

    st.markdown('<div class="rc-gap-md"></div>', unsafe_allow_html=True)

    action_col_1, action_col_2, action_col_3 = st.columns(3, gap="large")

    with action_col_1:
        st.download_button(
            label="Download as PDF",
            data=pdf_bytes,
            file_name="reality_check_report.pdf",
            mime="application/pdf",
            use_container_width=True,
            type="primary",
        )

    with action_col_2:
        st.markdown(
            """
            <div class="rr-action-card">
                <div class="rr-action-title">Save Report</div>
                <div class="rr-action-body">
                    Create a saved report record for later retrieval in the live version.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown('<div class="rc-gap-sm"></div>', unsafe_allow_html=True)
        report_name = st.text_input(
            "Report name",
            value=f"{report_data.get('franchise_name', 'Reality Check Report')} - {report_data.get('report_date', '')}",
            key="report_save_name",
        )
        if st.button(
            "Save This Report",
            key="save_report_placeholder",
            use_container_width=True,
        ):
            st.success(f'Placeholder only: "{report_name}" would be saved in the live version.')

    with action_col_3:
        st.markdown(
            """
            <div class="rr-action-card">
                <div class="rr-action-title">Email PDF</div>
                <div class="rr-action-body">
                    Send this report directly to a recipient in the live version.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown('<div class="rc-gap-sm"></div>', unsafe_allow_html=True)
        email_to = st.text_input(
            "Send report to",
            value=report_data.get("email", ""),
            placeholder="name@example.com",
            key="report_email_to",
        )
        if st.button(
            "Send Report by Email",
            key="email_report_placeholder",
            use_container_width=True,
        ):
            st.info(f'Placeholder only: the PDF would be emailed to "{email_to or "recipient"}" in the live version.')

    close_shell()
