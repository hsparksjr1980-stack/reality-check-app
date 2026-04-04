import streamlit as st
import pandas as pd
from datetime import date


DEFAULT_BUILDOUT_TASKS = [
    # Buildout & Construction
    {"Phase": "Buildout & Construction", "Task": "Select contractor", "Owner": "", "Status": "Not Started", "Due Date": None, "Budget": 0.0, "Actual": 0.0, "Notes": ""},
    {"Phase": "Buildout & Construction", "Task": "Finalize architecture/design", "Owner": "", "Status": "Not Started", "Due Date": None, "Budget": 0.0, "Actual": 0.0, "Notes": ""},
    {"Phase": "Buildout & Construction", "Task": "Approve final buildout budget", "Owner": "", "Status": "Not Started", "Due Date": None, "Budget": 0.0, "Actual": 0.0, "Notes": ""},
    {"Phase": "Buildout & Construction", "Task": "Track change orders", "Owner": "", "Status": "Not Started", "Due Date": None, "Budget": 0.0, "Actual": 0.0, "Notes": ""},
    {"Phase": "Buildout & Construction", "Task": "Monitor construction timeline", "Owner": "", "Status": "Not Started", "Due Date": None, "Budget": 0.0, "Actual": 0.0, "Notes": ""},

    # Permits & Regulatory
    {"Phase": "Permits & Regulatory", "Task": "Apply for business license", "Owner": "", "Status": "Not Started", "Due Date": None, "Budget": 0.0, "Actual": 0.0, "Notes": ""},
    {"Phase": "Permits & Regulatory", "Task": "Apply for health permits", "Owner": "", "Status": "Not Started", "Due Date": None, "Budget": 0.0, "Actual": 0.0, "Notes": ""},
    {"Phase": "Permits & Regulatory", "Task": "Schedule fire inspection", "Owner": "", "Status": "Not Started", "Due Date": None, "Budget": 0.0, "Actual": 0.0, "Notes": ""},
    {"Phase": "Permits & Regulatory", "Task": "Obtain certificate of occupancy", "Owner": "", "Status": "Not Started", "Due Date": None, "Budget": 0.0, "Actual": 0.0, "Notes": ""},
    {"Phase": "Permits & Regulatory", "Task": "Apply for signage permits", "Owner": "", "Status": "Not Started", "Due Date": None, "Budget": 0.0, "Actual": 0.0, "Notes": ""},

    # Systems & Infrastructure
    {"Phase": "Systems & Infrastructure", "Task": "Finalize POS setup", "Owner": "", "Status": "Not Started", "Due Date": None, "Budget": 0.0, "Actual": 0.0, "Notes": ""},
    {"Phase": "Systems & Infrastructure", "Task": "Set up payment processing", "Owner": "", "Status": "Not Started", "Due Date": None, "Budget": 0.0, "Actual": 0.0, "Notes": ""},
    {"Phase": "Systems & Infrastructure", "Task": "Set up payroll", "Owner": "", "Status": "Not Started", "Due Date": None, "Budget": 0.0, "Actual": 0.0, "Notes": ""},
    {"Phase": "Systems & Infrastructure", "Task": "Set up accounting", "Owner": "", "Status": "Not Started", "Due Date": None, "Budget": 0.0, "Actual": 0.0, "Notes": ""},
    {"Phase": "Systems & Infrastructure", "Task": "Complete tax registration", "Owner": "", "Status": "Not Started", "Due Date": None, "Budget": 0.0, "Actual": 0.0, "Notes": ""},
    {"Phase": "Systems & Infrastructure", "Task": "Activate utilities", "Owner": "", "Status": "Not Started", "Due Date": None, "Budget": 0.0, "Actual": 0.0, "Notes": ""},

    # Equipment & Vendors
    {"Phase": "Equipment & Vendors", "Task": "Order equipment", "Owner": "", "Status": "Not Started", "Due Date": None, "Budget": 0.0, "Actual": 0.0, "Notes": ""},
    {"Phase": "Equipment & Vendors", "Task": "Track deliveries", "Owner": "", "Status": "Not Started", "Due Date": None, "Budget": 0.0, "Actual": 0.0, "Notes": ""},
    {"Phase": "Equipment & Vendors", "Task": "Install equipment", "Owner": "", "Status": "Not Started", "Due Date": None, "Budget": 0.0, "Actual": 0.0, "Notes": ""},
    {"Phase": "Equipment & Vendors", "Task": "Set up vendors", "Owner": "", "Status": "Not Started", "Due Date": None, "Budget": 0.0, "Actual": 0.0, "Notes": ""},
    {"Phase": "Equipment & Vendors", "Task": "Purchase initial inventory", "Owner": "", "Status": "Not Started", "Due Date": None, "Budget": 0.0, "Actual": 0.0, "Notes": ""},

    # Financial Tracking
    {"Phase": "Financial Tracking", "Task": "Track budget vs actual", "Owner": "", "Status": "Not Started", "Due Date": None, "Budget": 0.0, "Actual": 0.0, "Notes": ""},
    {"Phase": "Financial Tracking", "Task": "Log major deposits and payments", "Owner": "", "Status": "Not Started", "Due Date": None, "Budget": 0.0, "Actual": 0.0, "Notes": ""},
    {"Phase": "Financial Tracking", "Task": "Review cost overruns", "Owner": "", "Status": "Not Started", "Due Date": None, "Budget": 0.0, "Actual": 0.0, "Notes": ""},

    # Timeline & Dependencies
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


def _initialize_buildout_tracker() -> None:
    if st.session_state.get("buildout_tracker_df") is None:
        df = pd.DataFrame(DEFAULT_BUILDOUT_TASKS)
        st.session_state["buildout_tracker_df"] = df


def _prepare_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    if "Due Date" in df.columns:
        df["Due Date"] = pd.to_datetime(df["Due Date"], errors="coerce").dt.date

    for col in ["Budget", "Actual"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0.0)

    return df


def _calculate_summary(df: pd.DataFrame) -> dict:
    total_tasks = len(df)
    complete_tasks = len(df[df["Status"] == "Complete"])
    blocked_tasks = len(df[df["Status"] == "Blocked"])
    waiting_tasks = len(df[df["Status"] == "Waiting"])

    today = pd.Timestamp.today().normalize()
    due_dates = pd.to_datetime(df["Due Date"], errors="coerce")

    overdue_df = df[
        due_dates.notna() &
        (due_dates < today) &
        (df["Status"] != "Complete")
]
    overdue_tasks = len(overdue_df)

    budget_total = float(df["Budget"].sum())
    actual_total = float(df["Actual"].sum())
    variance_total = actual_total - budget_total

    readiness_score = 0
    if total_tasks > 0:
        readiness_score = round((complete_tasks / total_tasks) * 100)

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


def _render_summary_cards(summary: dict) -> None:
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Readiness Score", f"{summary['readiness_score']}%")
    c2.metric("Tasks Complete", f"{summary['complete_tasks']} / {summary['total_tasks']}")
    c3.metric("Blocked", summary["blocked_tasks"])
    c4.metric("Overdue", summary["overdue_tasks"])

    c5, c6, c7 = st.columns(3)
    c5.metric("Budget", f"${summary['budget_total']:,.0f}")
    c6.metric("Actual", f"${summary['actual_total']:,.0f}")
    c7.metric("Variance", f"${summary['variance_total']:,.0f}")


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


def _render_phase_summary(df: pd.DataFrame) -> None:
    phase_summary = (
        df.groupby("Phase")
        .agg(
            Total_Tasks=("Task", "count"),
            Complete=("Status", lambda x: (x == "Complete").sum()),
            Blocked=("Status", lambda x: (x == "Blocked").sum()),
            Waiting=("Status", lambda x: (x == "Waiting").sum()),
            Budget=("Budget", "sum"),
            Actual=("Actual", "sum"),
        )
        .reset_index()
    )

    phase_summary["Progress %"] = (
        (phase_summary["Complete"] / phase_summary["Total_Tasks"]) * 100
    ).round(0)

    phase_summary["Variance"] = phase_summary["Actual"] - phase_summary["Budget"]

    st.markdown("### Phase Summary")
    st.dataframe(phase_summary, use_container_width=True, hide_index=True)


def _render_filtered_views(df: pd.DataFrame) -> None:
    st.markdown("### Filtered Views")

    view_col1, view_col2 = st.columns(2)

    with view_col1:
        show_only_open = st.checkbox("Show only open items", value=False)
        show_only_critical = st.checkbox("Show only critical items", value=False)

    with view_col2:
        phase_filter = st.multiselect(
            "Filter by phase",
            options=sorted(df["Phase"].dropna().unique().tolist()),
            default=[],
        )
        status_filter = st.multiselect(
            "Filter by status",
            options=STATUS_OPTIONS,
            default=[],
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

    st.dataframe(filtered, use_container_width=True, hide_index=True)


def render_buildout_tracker():
    st.title("Buildout & Launch Tracker")
    st.caption("Track the execution side of the deal: construction, permits, systems, vendors, budget, and launch readiness.")

    _initialize_buildout_tracker()

    df = _prepare_dataframe(st.session_state["buildout_tracker_df"])

    st.markdown("### Launch Settings")
    top1, top2, top3 = st.columns(3)
    with top1:
        target_open_date = st.date_input(
            "Target Opening Date",
            value=st.session_state.get("target_open_date", date.today()),
            key="target_open_date",
        )
    with top2:
        launch_owner = st.text_input(
            "Launch Owner",
            value=st.session_state.get("launch_owner", ""),
            key="launch_owner",
        )
    with top3:
        launch_status = st.selectbox(
            "Launch Status",
            ["Planning", "In Progress", "At Risk", "Ready to Launch", "Opened"],
            index=["Planning", "In Progress", "At Risk", "Ready to Launch", "Opened"].index(
                st.session_state.get("launch_status", "Planning")
            ) if st.session_state.get("launch_status", "Planning") in ["Planning", "In Progress", "At Risk", "Ready to Launch", "Opened"] else 0,
            key="launch_status",
        )

    st.markdown("### Tracker")
    edited_df = st.data_editor(
        df,
        use_container_width=True,
        num_rows="dynamic",
        hide_index=True,
        column_config={
            "Phase": st.column_config.SelectboxColumn(
                "Phase",
                options=[
                    "Buildout & Construction",
                    "Permits & Regulatory",
                    "Systems & Infrastructure",
                    "Equipment & Vendors",
                    "Financial Tracking",
                    "Timeline & Dependencies",
                ],
                required=True,
            ),
            "Task": st.column_config.TextColumn("Task", required=True),
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

    summary = _calculate_summary(edited_df)

    st.markdown("### Dashboard")
    _render_summary_cards(summary)
    _render_risk_callouts(summary)

    _render_phase_summary(edited_df)
    _render_filtered_views(edited_df)

    st.markdown("### Launch Readiness Notes")
    readiness_notes = st.text_area(
        "What still needs to be true before opening?",
        value=st.session_state.get("launch_readiness_notes", ""),
        height=120,
        key="launch_readiness_notes",
        placeholder="Examples: CO still pending, signage permit not approved, espresso machine delivery date not confirmed, payroll account not live.",
    )

    st.markdown("### Recommended Reality Check Questions")
    st.write("- What is on the critical path that could move the opening date?")
    st.write("- Which permits or approvals are still outside your control?")
    st.write("- Which vendor or equipment items have long lead times?")
    st.write("- Where are actual costs already above budget?")
    st.write("- What has to be complete before you can train, stock, and open?")

    st.markdown("### Pressure Test")
    st.write("If the opening date slips by 30–60 days, what breaks first?")
    st.write("If buildout costs rise another 10–15%, do you still have enough liquidity to finish correctly?")
    st.write("If one critical vendor delivery misses its date, what downstream tasks are affected?")

    if summary["readiness_score"] >= 85 and len(summary["incomplete_critical_df"]) == 0:
        st.success("Launch tracker shows strong readiness. Critical items appear substantially covered.")
    elif summary["readiness_score"] >= 60:
        st.warning("Launch tracker shows partial readiness. Review critical incomplete items and overdue tasks.")
    else:
        st.error("Launch tracker shows low readiness. The execution plan still has meaningful gaps.")
