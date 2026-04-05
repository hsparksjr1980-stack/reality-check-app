# page_config.py

from __future__ import annotations

from dataclasses import dataclass
from typing import Final


@dataclass(frozen=True)
class PageConfig:
    name: str
    section: str
    access: str = "standard"
    show_in_sidebar: bool = True


_PAGE_CONFIGS: Final[list[PageConfig]] = [
    PageConfig("Overview", "Phase 1 — Self & Idea"),
    PageConfig("Reality Check", "Phase 1 — Self & Idea"),
    PageConfig("Concept Validation", "Phase 1 — Self & Idea"),
    PageConfig("Opportunity Fit & Recommendations", "Phase 1 — Self & Idea"),
    PageConfig("Financial Model", "Phase 1 — Self & Idea"),
    PageConfig("Free Report", "Output"),
    PageConfig("Plans & Support", "Commercial"),
    PageConfig("Post-Discovery", "Phase 2 — Pre-Commitment"),
    PageConfig("Final Decision", "Phase 3 — Decision"),
    PageConfig("Report", "Output"),
    PageConfig("Paywall", "Commercial", "standard", False),
    PageConfig("Deal Workspace", "Phase 4 — Execution", "pro"),
    PageConfig("Deal Model", "Phase 4 — Execution", "pro"),
    PageConfig("Buildout & Launch Tracker", "Phase 4 — Execution", "pro"),
    PageConfig("Execution Report", "Phase 4 — Execution", "pro"),
]

DEFAULT_PAGE: Final[str] = "Overview"

PAGES: Final[list[str]] = [page.name for page in _PAGE_CONFIGS]
SIDEBAR_PAGES: Final[list[str]] = [page.name for page in _PAGE_CONFIGS if page.show_in_sidebar]
PAGE_CONFIG_MAP: Final[dict[str, PageConfig]] = {page.name: page for page in _PAGE_CONFIGS}

FREE_PAGES: Final[set[str]] = {
    page.name for page in _PAGE_CONFIGS if page.access != "pro"
}

PRO_PAGES: Final[set[str]] = {
    page.name for page in _PAGE_CONFIGS if page.access == "pro"
}

SECTION_LABELS: Final[dict[str, str]] = {
    page.name: page.section for page in _PAGE_CONFIGS
}


def get_page_config(page_name: str) -> PageConfig:
    return PAGE_CONFIG_MAP[page_name]


def is_free_page(page_name: str) -> bool:
    return page_name in FREE_PAGES


def is_pro_page(page_name: str) -> bool:
    return page_name in PRO_PAGES


def get_section_label(page_name: str) -> str:
    return SECTION_LABELS[page_name]


def validate_page_config() -> None:
    page_names = [page.name for page in _PAGE_CONFIGS]

    if not _PAGE_CONFIGS:
        raise ValueError("Page configuration cannot be empty.")

    if DEFAULT_PAGE not in page_names:
        raise ValueError(f'DEFAULT_PAGE "{DEFAULT_PAGE}" is not defined in page configuration.')

    if len(page_names) != len(set(page_names)):
        duplicates = sorted({name for name in page_names if page_names.count(name) > 1})
        raise ValueError(f"Duplicate page names found: {duplicates}")

    invalid_access = sorted({page.access for page in _PAGE_CONFIGS if page.access not in {"standard", "pro"}})
    if invalid_access:
        raise ValueError(f"Invalid page access types found: {invalid_access}")


validate_page_config()
