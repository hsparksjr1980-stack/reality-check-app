from __future__ import annotations

import pandas as pd
import streamlit as st


DEFAULT_BUILDOUT_ROWS = [
    ("Buildout & Construction", "Select contractor", "Not started", "", "", "", ""),
    ("Buildout & Construction", "Approve plans", "Not started", "", "", "", "Select contractor"),
    ("Permits & Regulatory", "Apply for business license", "Not started", "", "", "", "Approve plans"),
    ("Permits & Regulatory", "Health permit", "Not started", "", "", "", "Approve plans"),
    ("Permits & Regulatory", "Fire inspection", "Not started", "", "", "", "Approve plans"),
    ("Permits & Regulatory", "Certificate of occupancy", "Not started", "", "", "", "Fire inspection"),
    ("Systems & Infrastructure", "POS setup", "Not started", "", "", "", "Approve plans"),
    ("Systems & Infrastructure", "Payroll setup", "Not started", "", "", "", ""),
    ("Equipment & Vendors", "Order equipment", "Not started", "", "", "", "Approve plans"),
    ("Equipment & Vendors", "Install equipment", "Not started", "", "", "", "Order equipment"),
    ("Financial Tracking", "Initial budget loaded", "Not started", "", "", "", ""),
    ("Timeline & Dependencies", "Opening readiness review", "Not started", "", "", "", "Certificate of occupancy"),
]

COLUMNS = [
    "Workstream",
    "Task",
    "Status",
    "Owner",
    "Start Date",
    "Due Date",
    "Notes",
    "Depends On",
]



def get_buildout_tracker_df() -> pd.DataFrame:
    existing = st.session_state.get("buildout_tracker_df")
    if isinstance(existing, pd.DataFrame):
        return existing

    df = pd.DataFrame(DEFAULT_BUILDOUT_ROWS, columns=COLUMNS)
    st.session_state["buildout_tracker_df"] = df
    return df



def save_buildout_tracker_df(df: pd.DataFrame) -> None:
    st.session_state["buildout_tracker_df"] = df



def summarize_buildout_tracker(df: pd.DataFrame) -> dict:
    status_counts = df["Status"].fillna("Not started").value_counts().to_dict()
    return {
        "total_tasks": len(df),
        "done": status_counts.get("Done", 0),
        "in_progress": status_counts.get("In progress", 0),
        "not_started": status_counts.get("Not started", 0),
        "blocked": status_counts.get("Blocked", 0),
    }



def find_blockers(df: pd.DataFrame) -> list[str]:
    blockers: list[str] = []
    task_status = dict(zip(df["Task"], df["Status"]))

    for _, row in df.iterrows():
        dependency = str(row.get("Depends On", "")).strip()
        if not dependency:
            continue
        if task_status.get(dependency) != "Done" and row.get("Status") in ["In progress", "Blocked"]:
            blockers.append(f"{row['Task']} depends on {dependency}, which is not done yet.")

    return blockers
