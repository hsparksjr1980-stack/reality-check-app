from dataclasses import dataclass


@dataclass
class PressureTestInputs:
    base_revenue: float
    base_margin_pct: float
    fixed_costs: float
    annual_debt_service: float
    buildout_cost: float
    cash_on_hand: float
    revenue_downside_pct: float = 0.20
    margin_compression_pct: float = 0.03
    buildout_overrun_pct: float = 0.15



def run_pressure_test(inputs: PressureTestInputs) -> dict:
    stressed_revenue = inputs.base_revenue * (1 - inputs.revenue_downside_pct)
    stressed_margin_pct = max(inputs.base_margin_pct - inputs.margin_compression_pct, 0)
    stressed_gross_profit = stressed_revenue * stressed_margin_pct
    stressed_buildout = inputs.buildout_cost * (1 + inputs.buildout_overrun_pct)
    annual_cash_after_fixed = stressed_gross_profit - inputs.fixed_costs - inputs.annual_debt_service
    ending_cash = inputs.cash_on_hand - (stressed_buildout - inputs.buildout_cost) + annual_cash_after_fixed

    if annual_cash_after_fixed < 0:
        breaks_first = "Operating cash flow"
    elif ending_cash < 0:
        breaks_first = "Liquidity cushion"
    elif stressed_buildout > inputs.buildout_cost * 1.10:
        breaks_first = "Buildout budget"
    else:
        breaks_first = "No immediate break under this scenario"

    return {
        "stressed_revenue": stressed_revenue,
        "stressed_margin_pct": stressed_margin_pct,
        "stressed_gross_profit": stressed_gross_profit,
        "stressed_buildout": stressed_buildout,
        "annual_cash_after_fixed": annual_cash_after_fixed,
        "ending_cash": ending_cash,
        "breaks_first": breaks_first,
    }
