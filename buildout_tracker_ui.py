# buildout_tracker_ui.py

from __future__ import annotations

from datetime import date

import pandas as pd
import streamlit as st

from ui_styles import (
    close_shell,
    open_shell,
    render_card,
    render_page_header,
    render_section_intro,
)


DEFAULT_BUILDOUT_TASKS = [
    {"Phase": "Buildout & Construction", "Task": "Select contractor", "Owner": "", "Status": "Not Started", "Due Date": None, "Budget": 0.0, "Actual": 0.0, "Notes": ""},
    {"Phase": "Buildout & Construction", "Task": "Finalize architecture/design", "Owner": "", "Status": "Not Started", "Due Date": None, "Budget": 0.0, "Actual": 0.0, "Notes": ""},
    {"Phase": "Buildout & Construction", "Task": "Approve final buildout budget", "Owner": "", "Status": "Not Started", "Due Date": None, "Budget": 0.0, "Actual": 0.0, "Notes": ""},
    {"Phase": "Buildout & Construction", "Task": "Track change orders", "Owner": "", "Status": "Not Started", "Due Date": None, "Budget": 0.0, "Actual": 0.0, "Notes": ""},
    {"Phase": "Buildout & Construction", "Task": "Monitor construction timeline", "Owner": "", "Status": "Not Started", "Due Date": None, "Budget": 0.0, "Actual": 0.0, "Notes": ""},
    {"Phase": "Permits & Regulatory", "Task": "Apply for business license", "Owner": "", "Status": "Not Started", "Due Date": None, "Budget": 0.0, "Actual": 0.0, "Notes": ""},
    {"Phase": "Permits & Regulatory", "Task": "Apply for health permits", "Owner": "", "Status": "Not Started", "Due Date": None, "Budget": 0.0, "Actual": 0.0, "Notes": ""},
    {"Phase": "Permits & Regulatory", "Task": "Schedule fire inspection", "Owner": "", "Status": "Not Started", "Due Date": None, "Budget": 0.0, "Actual": 0.0, "Notes": ""},
    {"Phase": "Permits & Regulatory", "Task": "Obtain certificate of occupancy", "Owner": "", "Status": "Not Started", "Due Date": None, "Budget": 0.0, "Actual": 0.0, "Notes": ""},
    {"Phase": "Permits & Regulatory", "Task": "Apply for signage permits", "Owner": "", "Status": "Not Started", "Due Date": None, "Budget": 0.0, "Actual": 0.0, "Notes": ""},
    {"Phase": "Systems & Infrastructure", "Task": "Finalize POS setup", "Owner": "", "Status": "Not Started", "Due Date": None, "Budget": 0.0, "Actual": 0.0, "Notes": ""},
    {"Phase": "Systems & Infrastructure", "Task": "Set up payment processing", "Owner": "", "Status": "Not Started", "Due Date": None, "Budget": 0.0, "Actual": 0.0, "Notes": ""},
    {"Phase": "Systems & Infrastructure", "Task": "Set up payroll", "Owner": "", "Status": "Not Started", "Due Date": None, "Budget": 0.0, "Actual": 0.0, "Notes": ""},
    {"Phase": "Systems & Infrastructure", "Task": "Set up accounting", "Owner": "", "Status": "Not Started", "Due Date": None, "Budget": 0.0, "Actual": 0.0, "Notes": ""},
    {"Phase": "Systems & Infrastructure", "Task": "Complete tax registration", "Owner": "", "Status": "Not Started", "Due Date": None, "Budget": 0.0, "Actual": 0.0, "Notes": ""},
    {"Phase": "Systems & Infrastructure", "Task": "Activate utilities", "Owner": "", "Status": "Not Started", "Due Date": None, "Budget": 0.0, "Actual": 0.0, "Notes": ""},
    {"Phase": "Equipment & Vendors", "Task": "Order equipment", "Owner": "", "Status": "Not Started", "Due Date": None, "Budget": 0.0, "Actual": 0.0, "Notes": ""},
    {"Phase": "Equipment & Vendors", "Task": "Track deliveries", "Owner": "", "Status": "Not Started", "Due Date": None, "Budget": 0.0, "Actual": 0.0, "Notes": ""},
    {"Phase": "Equipment & Vendors", "Task": "Install equipment", "Owner": "", "Status": "Not Started", "Due Date": None, "Budget": 0.0, "Actual": 0.0, "Notes": ""},
    {"Phase": "Equipment & Vendors", "Task": "Set up vendors", "Owner": "", "Status": "Not Started", "Due Date": None, "Budget": 0.0, "Actual": 0.0, "Notes": ""},
    {"Phase": "Equipment & Vendors", "Task": "Purchase initial inventory", "Owner": "", "Status": "Not Started", "Due Date": None, "Budget": 0.0, "Actual": 0.0, "Notes": ""},
    {"Phase": "Financial Tracking", "Task": "Track budget vs actual", "Owner": "", "Status": "Not Started", "Due Date": None, "Budget": 0.0, "Actual": 0.0, "Notes": ""},
    {"Phase": "Financial Tracking", "Task": "Log major deposits and payments", "Owner": "", "Status": "Not Started", "Due Date": None, "Budget": 0.0, "Actual": 0.0, "Notes": ""},
    {"Phase": "Financial Tracking", "Task": "Review cost overruns", "Owner": "", "Status": "Not Started", "Due Date": None, "Budget": 0.0, "Actual": 0.0, "Notes": ""},
    {"Phase": "Timeline & Dependencies", "Task": "Confirm opening date assumptions", "Owner": "", "Status": "Not Started", "Due Date": None, "Budget": 0.0, "Actual": 0.0, "Notes": ""},
    {"Phase": "Timeline & Dependencies", "Task": "Identify critical path items", "Owner": "", "Status": "Not Started", "Due Date": None, "Budget": 0.0, "Actual": 0.0, "Notes": ""},
    {"Phase": "Timeline & Dependencies", "Task": "Flag delays and blockers", "Owner": "", "Status": "Not Started", "Due Date": None, "Budget": 0.0, "Actual": 0.0, "Notes": ""},
]

STATUS_OPTIONS = [
    "Not Started",
    "In Progress",
    "Waiting",
    "Blocked",
    "Complete",
]

PHASE_OPTIONS = [
    "Buildout & Construction",
    "Permits & Regulatory",
    "Systems & Infrastructure",
    "Equipment & Vendors",
    "Financial Tracking",
    "Timeline & Dependencies",
]

CRITICAL_TASKS = {
    "Select contractor",
    "Finalize architecture/design",
    "Approve final buildout budget",
    "Apply for business license",
    "Apply for health permits",
    "Obtain certificate of occupancy",
    "Finalize POS setup",
    "Set up payment processing",
    "Activate utilities",
    "Order equipment",
    "Install equipment",
    "Purchase initial inventory",
    "Confirm opening date assumptions",
}

PHASE_STYLE_MAP = {
    "Buildout & Construction": {"bg": "#EEF4FF", "border": "#93C5FD", "text": "#1E3A8A"},
    "Permits & Regulatory": {"bg": "#F5F3FF", "border": "#C4B5FD", "text": "#5B21B6"},
    "Systems & Infrastructure": {"bg": "#ECFDF5", "border": "#86EFAC", "text": "#166534"},
    "Equipment & Vendors": {"bg": "#FFF7ED", "border": "#FDBA74", "text": "#9A3412"},
    "Financial Tracking": {"bg": "#FEFCE8", "border": "#FDE68A", "text": "#854D0E"},
    "Timeline & Dependencies": {"bg": "#FDF2F8", "border": "#F9A8D4", "text": "#9D174D"},
}


def _inject_local_styles() -> None:
    st.markdown(
        """
        <style>
            .bt-phase-chip {
                display: inline-block;
                padding: 0.28rem 0.62rem;
                border-radius: 999px;
                font-size: 0.72rem;
                font-weight: 700;
                letter-spacing: 0.04em;
                border: 1px solid transparent;
                margin-bottom: 0.55rem;
            }

            .bt-summary-card {
                border: 1px solid #e5e7eb;
                border-radius: 18px;
                background: #ffffff;
                box-shadow: 0 8px 24px rgba(17, 24, 39, 0.05);
                padding: 1rem;
                height: 100%;
            }

            .bt-summary-title {
                font-size: 1rem;
                font-weight: 750;
                line-height: 1.25;
                color: #111827;
                margin-bottom: 0.28rem;
            }

            .bt-summary-body {
                font-size: 0.92rem;
                line-height: 1.58;
                color: #4b5563;
            }

            .bt-risk-box {
                border-radius: 16px;
                padding: 0.95rem 1rem;
                border: 1px solid #e5e7eb;
                background: #ffffff;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def _phase_chip_html(phase: str) -> str:
    styles = PHASE_STYLE_MAP.get(
        phase,
        {"bg": "#F3F4F6", "border": "#D1D5DB", "text": "#374151"},
    )
    return (
        f'<span class="bt-phase-chip" '
        f'style="background:{styles["bg"]};border-color:{styles["border"]};color:{styles["text"]};">'
        f"{phase}</span>"
    )


def _initialize_buildout_tracker() -> None:
    if st.session_state.get("buildout_tracker_df") is None:
        st.session_state["buildout_tracker_df"] = pd.DataFrame(DEFAULT_BUILDOUT_TASKS)


def _prepare_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    working = df.copy()

    if "Due Date" in working.columns:
        working["Due Date"] = pd.to_datetime(working["Due Date"], errors="coerce").dt.date

    for col in ["Budget", "Actual"]:
        if col in working.columns:
            working[col] = pd.to_numeric(working[col], errors="coerce").fillna(0.0)

    for col in ["Phase", "Task", "Owner", "Status", "Notes"]:
        if col in working.columns:
            working[col] = working[col].fillna("")

    return working


def _calculate_summary(df: pd.DataFrame) -> dict:
    total_tasks = len(df)
    complete_tasks = len(df[df["Status"] == "Complete"])
    blocked_tasks = len(df[df["Status"] == "Blocked"])
    waiting_tasks = len(df[df["Status"] == "Waiting"])

    today = pd.Timestamp.today().normalize()
    due_dates = pd.to_datetime(df["Due Date"], errors="coerce")
    overdue_df = df[
        due_dates.notna()
        & (due_dates < today)
        & (df["Status"] != "Complete")
    ]
    overdue_tasks = len(overdue_df)

    budget_total = float(df["Budget"].sum())
    actual_total = float(df["Actual"].sum())
    variance_total = actual_total - budget_total

    readiness_score = round((complete_tasks / total_tasks) * 100) if total_tasks > 0 else 0

    critical_df = df[df["Task"].isin(CRITICAL_TASKS)]
    incomplete_critical_df = critical_df[critical_df["Status"] != "Complete"]

    return {
        "total_tasks": total_tasks,
        "complete_tasks": complete_tasks,
        "blocked_tasks": blocked_tasks,
        "waiting_tasks": waiting_tasks,
        "overdue_tasks": overdue_tasks,
        "budget_total": budget_total,
        "actual_total": actual_total,
        "variance_total": variance_total,
        "readiness_score": readiness_score,
        "overdue_df": overdue_df,
        "incomplete_critical_df": incomplete_critical_df,
    }


def _build_phase_summary(df: pd.DataFrame) -> pd.DataFrame:
    phase_summary = (
        df.groupby("Phase")
        .agg(
            Total_Tasks=("Task", "count"),
            Complete=("Status", lambda x: (x == "Complete").sum()),
            In_Progress=("Status", lambda x: (x == "In Progress").sum()),
            Waiting=("Status", lambda x: (x == "Waiting").sum()),
            Blocked=("Status", lambda x: (x == "Blocked").sum()),
            Budget=("Budget", "sum"),
            Actual=("Actual", "sum"),
        )
        .reset_index()
    )

    phase_summary["Progress %"] = (
        (phase_summary["Complete"] / phase_summary["Total_Tasks"]) * 100
    ).round(0)
    phase_summary["Variance"] = phase_summary["Actual"] - phase_summary["Budget"]

    return phase_summary


def _render_summary_cards(summary: dict) -> None:
    c1, c2, c3, c4 = st.columns(4, gap="medium")
    with c1:
        render_card(
            label="Readiness",
            title=f"{summary['readiness_score']}%",
            body="Share of total tasks marked complete.",
        )
    with c2:
        render_card(
            label="Tasks complete",
            title=f"{summary['complete_tasks']} / {summary['total_tasks']}",
            body="Completed tasks out of the current tracker total.",
        )
    with c3:
        render_card(
            label="Blocked",
            title=str(summary["blocked_tasks"]),
            body="Tasks currently blocked and likely to affect timing.",
        )
    with c4:
        render_card(
            label="Overdue",
            title=str(summary["overdue_tasks"]),
            body="Tasks past due and not yet complete.",
        )

    st.markdown('<div class="rc-gap-md"></div>', unsafe_allow_html=True)

    c5, c6, c7 = st.columns(3, gap="medium")
    with c5:
        render_card(
            label="Budget",
            title=f"${summary['budget_total']:,.0f}",
            body="Total budget currently assigned across tracked tasks.",
        )
    with c6:
        render_card(
            label="Actual",
            title=f"${summary['actual_total']:,.0f}",
            body="Actual spend recorded so far.",
        )
    with c7:
        variance_label = "Over budget" if summary["variance_total"] > 0 else "Variance"
        render_card(
            label=variance_label,
            title=f"${summary['variance_total']:,.0f}",
            body="Actual less budget across all tracked items.",
        )


def _render_risk_callouts(summary: dict) -> None:
    incomplete_critical_df = summary["incomplete_critical_df"]
    overdue_df = summary["overdue_df"]

    if len(incomplete_critical_df) > 0:
        st.error("Critical launch items are still incomplete.")
        for task in incomplete_critical_df["Task"].tolist():
            st.write(f"- {task}")

    if len(overdue_df) > 0:
        st.warning("Some tasks are overdue.")
        for _, row in overdue_df[["Task", "Due Date", "Status"]].iterrows():
            st.write(f"- {row['Task']} — due {row['Due Date']} ({row['Status']})")


def _render_phase_progress_cards(phase_summary: pd.DataFrame) -> None:
    render_section_intro(
        title="Phase progress",
        body="Each phase is color coded so you can scan progress, cost, and bottlenecks more quickly.",
    )
    st.markdown('<div class="rc-gap-md"></div>', unsafe_allow_html=True)

    columns = st.columns(2, gap="large")
    for index, row in phase_summary.iterrows():
        styles = PHASE_STYLE_MAP.get(
            row["Phase"],
            {"bg": "#F3F4F6", "border": "#D1D5DB", "text": "#374151"},
        )
        with columns[index % 2]:
            st.markdown(
                f"""
                <div class="bt-summary-card" style="border-color:{styles["border"]};">
                    {_phase_chip_html(row["Phase"])}
                    <div class="bt-summary-title">{int(row["Progress %"])}% complete</div>
                    <div class="bt-summary-body">
                        {int(row["Complete"])} of {int(row["Total_Tasks"])} tasks complete<br>
                        {int(row["Blocked"])} blocked · {int(row["Waiting"])} waiting<br>
                        Budget: ${row["Budget"]:,.0f} · Actual: ${row["Actual"]:,.0f} · Variance: ${row["Variance"]:,.0f}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.markdown('<div class="rc-gap-md"></div>', unsafe_allow_html=True)


def _render_phase_summary_table(phase_summary: pd.DataFrame) -> None:
    render_section_intro(
        title="Phase summary table",
        body="Use the table view for a denser operational summary across all phases.",
    )
    st.markdown('<div class="rc-gap-md"></div>', unsafe_allow_html=True)

    phase_table = phase_summary.copy()
    phase_table["Phase"] = phase_table["Phase"].map(
        lambda value: value if pd.notna(value) else ""
    )
    st.dataframe(phase_table, use_container_width=True, hide_index=True)


def _render_filtered_views(df: pd.DataFrame) -> None:
    render_section_intro(
        title="Filtered views",
        body="Narrow the tracker to open items, critical tasks, or specific phases and statuses.",
    )
    st.markdown('<div class="rc-gap-md"></div>', unsafe_allow_html=True)

    f1, f2, f3, f4 = st.columns(4, gap="medium")
    with f1:
        show_only_open = st.checkbox("Open items only", value=False, key="bt_filter_open")
    with f2:
        show_only_critical = st.checkbox("Critical items only", value=False, key="bt_filter_critical")
    with f3:
        phase_filter = st.multiselect(
            "Filter by phase",
            options=sorted(df["Phase"].dropna().unique().tolist()),
            default=[],
            key="bt_filter_phase",
        )
    with f4:
        status_filter = st.multiselect(
            "Filter by status",
            options=STATUS_OPTIONS,
            default=[],
            key="bt_filter_status",
        )

    filtered = df.copy()

    if show_only_open:
        filtered = filtered[filtered["Status"] != "Complete"]

    if show_only_critical:
        filtered = filtered[filtered["Task"].isin(CRITICAL_TASKS)]

    if phase_filter:
        filtered = filtered[filtered["Phase"].isin(phase_filter)]

    if status_filter:
        filtered = filtered[filtered["Status"].isin(status_filter)]

    display_df = filtered.copy()
    display_df.insert(
        0,
        "Phase Color",
        display_df["Phase"].map(lambda phase: phase),
    )

    st.dataframe(display_df, use_container_width=True, hide_index=True)


def _render_readiness_notes() -> None:
    render_section_intro(
        title="Launch readiness notes",
        body="Use this section to capture what still needs to be true before opening.",
    )
    st.markdown('<div class="rc-gap-md"></div>', unsafe_allow_html=True)

    st.text_area(
        "What still needs to be true before opening?",
        value=st.session_state.get("launch_readiness_notes", ""),
        height=140,
        key="launch_readiness_notes",
        placeholder=(
            "Examples: certificate of occupancy still pending, signage permit not approved, "
            "equipment delivery date not confirmed, payroll account not live."
        ),
    )


def _render_guidance(summary: dict) -> None:
    render_section_intro(
        title="Execution guidance",
        body="These prompts help keep the tracker tied to the actual opening risk, not just task completion.",
    )
    st.markdown('<div class="rc-gap-md"></div>', unsafe_allow_html=True)

    g1, g2 = st.columns(2, gap="large")

    with g1:
        st.markdown("### Recommended reality check questions")
        st.write("- What is on the critical path that could move the opening date?")
        st.write("- Which permits or approvals are still outside your control?")
        st.write("- Which vendor or equipment items have long lead times?")
        st.write("- Where are actual costs already above budget?")
        st.write("- What has to be complete before you can train, stock, and open?")

    with g2:
        st.markdown("### Pressure test")
        st.write("- If the opening date slips by 30–60 days, what breaks first?")
        st.write("- If buildout costs rise another 10–15%, do you still have enough liquidity to finish correctly?")
        st.write("- If one critical vendor delivery misses its date, what downstream tasks are affected?")

    st.markdown('<div class="rc-gap-md"></div>', unsafe_allow_html=True)

    if summary["readiness_score"] >= 85 and len(summary["incomplete_critical_df"]) == 0:
        st.success("Launch tracker shows strong readiness. Critical items appear substantially covered.")
    elif summary["readiness_score"] >= 60:
        st.warning("Launch tracker shows partial readiness. Review critical incomplete items and overdue tasks.")
    else:
        st.error("Launch tracker shows low readiness. The execution plan still has meaningful gaps.")


def render_buildout_tracker() -> None:
    _inject_local_styles()
    _initialize_buildout_tracker()

    df = _prepare_dataframe(st.session_state["buildout_tracker_df"])

    open_shell()

    render_page_header(
        eyebrow="Execution — Buildout & Launch Tracker",
        title="Track the work required to get open.",
        subtitle=(
            "Use this tracker to manage construction, permits, systems, vendors, budget, and launch readiness "
            "with a clearer operational view."
        ),
        wide=True,
    )

    st.markdown('<div class="rc-gap-lg"></div>', unsafe_allow_html=True)

    render_section_intro(
        title="Launch settings",
        body="Set the main launch context first so the tracker reflects the current opening plan.",
    )
    st.markdown('<div class="rc-gap-md"></div>', unsafe_allow_html=True)

    top1, top2, top3 = st.columns(3, gap="large")
    with top1:
        st.date_input(
            "Target Opening Date",
            value=st.session_state.get("target_open_date", date.today()),
            key="target_open_date",
        )
    with top2:
        st.text_input(
            "Launch Owner",
            value=st.session_state.get("launch_owner", ""),
            key="launch_owner",
            placeholder="Who is driving the opening process?",
        )
    with top3:
        launch_status_options = ["Planning", "In Progress", "At Risk", "Ready to Launch", "Opened"]
        current_launch_status = st.session_state.get("launch_status", "Planning")
        st.selectbox(
            "Launch Status",
            launch_status_options,
            index=launch_status_options.index(current_launch_status) if current_launch_status in launch_status_options else 0,
            key="launch_status",
        )

    st.markdown('<div class="rc-gap-lg"></div>', unsafe_allow_html=True)

    render_section_intro(
        title="Tracker",
        body="Keep the same data detail, but use the editor below as the working source of truth for execution.",
    )
    st.markdown('<div class="rc-gap-md"></div>', unsafe_allow_html=True)

    edited_df = st.data_editor(
        df,
        use_container_width=True,
        num_rows="dynamic",
        hide_index=True,
        column_config={
            "Phase": st.column_config.SelectboxColumn(
                "Phase",
                options=PHASE_OPTIONS,
                required=True,
            ),
            "Task": st.column_config.TextColumn("Task", required=True, width="medium"),
            "Owner": st.column_config.TextColumn("Owner"),
            "Status": st.column_config.SelectboxColumn(
                "Status",
                options=STATUS_OPTIONS,
                required=True,
            ),
            "Due Date": st.column_config.DateColumn("Due Date"),
            "Budget": st.column_config.NumberColumn("Budget", min_value=0.0, step=100.0, format="$%.2f"),
            "Actual": st.column_config.NumberColumn("Actual", min_value=0.0, step=100.0, format="$%.2f"),
            "Notes": st.column_config.TextColumn("Notes", width="large"),
        },
        key="buildout_tracker_editor",
    )

    edited_df = _prepare_dataframe(pd.DataFrame(edited_df))
    st.session_state["buildout_tracker_df"] = edited_df

    st.markdown('<div class="rc-gap-md"></div>', unsafe_allow_html=True)

    if st.button(
        "Save tracker changes",
        key="buildout_tracker_save",
        use_container_width=True,
        type="primary",
    ):
        st.session_state["buildout_tracker_df"] = edited_df
        st.success("Buildout tracker changes saved.")

    summary = _calculate_summary(edited_df)
    phase_summary = _build_phase_summary(edited_df)

    st.markdown('<div class="rc-gap-lg"></div>', unsafe_allow_html=True)

    render_section_intro(
        title="Dashboard",
        body="Use the summary below to understand readiness, cost movement, and the main launch risks.",
    )
    st.markdown('<div class="rc-gap-md"></div>', unsafe_allow_html=True)

    _render_summary_cards(summary)
    st.markdown('<div class="rc-gap-md"></div>', unsafe_allow_html=True)
    _render_risk_callouts(summary)

    st.markdown('<div class="rc-gap-lg"></div>', unsafe_allow_html=True)

    _render_phase_progress_cards(phase_summary)

    st.markdown('<div class="rc-gap-lg"></div>', unsafe_allow_html=True)

    _render_phase_summary_table(phase_summary)

    st.markdown('<div class="rc-gap-lg"></div>', unsafe_allow_html=True)

    _render_filtered_views(edited_df)

    st.markdown('<div class="rc-gap-lg"></div>', unsafe_allow_html=True)

    _render_readiness_notes()

    st.markdown('<div class="rc-gap-lg"></div>', unsafe_allow_html=True)

    _render_guidance(summary)

    st.markdown('<div class="rc-gap-lg"></div>', unsafe_allow_html=True)

    if st.button(
        "Open Execution Report",
        key="buildout_tracker_open_execution_report",
        use_container_width=True,
        type="primary",
    ):
        st.session_state["current_page"] = "Execution Report"
        st.rerun()

    close_shell()
