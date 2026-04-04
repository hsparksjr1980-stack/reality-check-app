from decision_engine import build_decision_packet



def build_stress_test_report_text(pressure_test_result: dict) -> str:
    packet = build_decision_packet()
    lines = [
        "Reality Check — Deal Stress Test Report",
        "",
        f"Master verdict: {packet['master_verdict']}",
        f"Decision action: {packet['decision_action'] or 'Not locked'}",
        "",
        "Top risk flags:",
    ]
    lines.extend([f"- {flag}" for flag in packet["risk_flags"]] or ["- No major risk flags captured yet."])
    lines.extend([
        "",
        "Pressure test output:",
        f"- Stressed revenue: ${pressure_test_result['stressed_revenue']:,.0f}",
        f"- Stressed margin: {pressure_test_result['stressed_margin_pct']*100:.1f}%",
        f"- Stressed buildout: ${pressure_test_result['stressed_buildout']:,.0f}",
        f"- Annual cash after fixed costs: ${pressure_test_result['annual_cash_after_fixed']:,.0f}",
        f"- Ending cash: ${pressure_test_result['ending_cash']:,.0f}",
        f"- What breaks first: {pressure_test_result['breaks_first']}",
    ])
    return "\n".join(lines)
