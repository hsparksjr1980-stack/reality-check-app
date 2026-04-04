# Missing Foundation Pack

These files add the missing structural layer between the current page-based app and the PRD-driven product.

## New / Expanded Foundation Files

- `app_state.py` — central session-state initialization and reset handling
- `page_config.py` — single source of truth for pages, tiers, and phase labels
- `phase_gate.py` — controls page unlock rules and flow gating
- `paywall_logic.py` — central Pro access and decision-lock behavior
- `guardrails_engine.py` — stores and evaluates required deal guardrails
- `pressure_test_engine.py` — basic downside / “what breaks first” scenario engine
- `decision_engine.py` — normalizes verdicts into one master decision packet
- `buildout_tracker_logic.py` — buildout task template, summaries, blocker checks
- `buildout_tracker_ui.py` — Pro tracker page for buildout and launch execution
- `plans_support_content.py` — structured tier / consulting / add-on content
- `plans_support_ui.py` — real Plans & Support page instead of placeholder text
- `report_templates.py` — starter report generator for productized outputs

## Updated Integration Files

- `app.py` — adds initialization, gating, Plans page, and Buildout Tracker page
- `nav_ui.py` — shows locked vs unlocked pages and prevents skipping ahead
- `final_decision_ui.py` — locks the decision and ties it to the Pro path

## What this pack does not replace yet

- Your existing scoring logic in phase files
- Real payments / Stripe integration
- Real database persistence
- PDF export flow
- Authentication beyond current session approach

## Recommended add order

1. `page_config.py`
2. `app_state.py`
3. `phase_gate.py`
4. `paywall_logic.py`
5. `guardrails_engine.py`
6. `decision_engine.py`
7. `plans_support_content.py`
8. `plans_support_ui.py`
9. `buildout_tracker_logic.py`
10. `buildout_tracker_ui.py`
11. Replace `nav_ui.py`
12. Replace `final_decision_ui.py`
13. Replace `app.py`
