def check_profit_margin(metrics):
    """Generate insights from net profit margin."""

    insights = []

    margin = float(metrics.get("profit_margin", 0))

    if margin >= 30:
        insights.append({
            "type": "success",
            "title": "Strong Profitability",
            "message": (
                f"Profit margin is {margin:.1f}%, indicating strong "
                "profitability based on the current financial data."
            ),
            "recommendation": (
                "Maintain pricing discipline and monitor operating "
                "costs as the business grows."
            ),
            "metric": margin,
        })

    elif margin >= 20:
        insights.append({
            "type": "success",
            "title": "Healthy Profit Margin",
            "message": (
                f"Profit margin is {margin:.1f}%, providing a "
                "solid profitability position."
            ),
            "recommendation": (
                "Continue monitoring major expense categories "
                "and protect current margins."
            ),
            "metric": margin,
        })

    elif margin >= 10:
        insights.append({
            "type": "info",
            "title": "Moderate Profitability",
            "message": (
                f"Profit margin is {margin:.1f}%. "
                "There is room to improve profitability."
            ),
            "recommendation": (
                "Review pricing, operating expenses, and the "
                "profitability of major revenue sources."
            ),
            "metric": margin,
        })

    elif margin >= 0:
        insights.append({
            "type": "warning",
            "title": "Low Profit Margin",
            "message": (
                f"Profit margin is {margin:.1f}%, leaving limited "
                "room between revenue and operating expenses."
            ),
            "recommendation": (
                "Review pricing strategy, major expenses, and "
                "operating efficiency."
            ),
            "metric": margin,
        })

    else:
        insights.append({
            "type": "warning",
            "title": "Negative Profit Margin",
            "message": (
                f"Profit margin is {margin:.1f}%, indicating that "
                "expenses currently exceed revenue."
            ),
            "recommendation": (
                "Review the largest expense categories, pricing, "
                "and near-term cash requirements."
            ),
            "metric": margin,
        })

    return insights


def check_largest_expense(metrics):
    """Identify the largest expense category."""

    category = metrics.get(
        "largest_expense_category",
        "N/A"
    )

    amount = float(
        metrics.get(
            "largest_expense_amount",
            0
        )
    )

    if category == "N/A" or amount <= 0:
        return []

    return [{
        "type": "info",
        "title": "Largest Expense Category",
        "message": (
            f"{category} is currently the largest expense category "
            f"at ${amount:,.2f}."
        ),
        "recommendation": (
            "Review this category for cost-saving opportunities "
            "without compromising essential operations."
        ),
        "metric": amount,
    }]


def check_expense_ratio(metrics):
    """Generate insights from the expense-to-revenue ratio."""

    insights = []

    ratio = float(
        metrics.get(
            "expense_ratio",
            0
        )
    )

    if ratio > 100:
        insights.append({
            "type": "warning",
            "title": "Expenses Exceed Revenue",
            "message": (
                f"Operating expenses consume {ratio:.1f}% of revenue."
            ),
            "recommendation": (
                "Review operating costs and revenue generation "
                "to restore positive operating performance."
            ),
            "metric": ratio,
        })

    elif ratio > 85:
        insights.append({
            "type": "warning",
            "title": "High Operating Expenses",
            "message": (
                f"Operating expenses consume {ratio:.1f}% of revenue."
            ),
            "recommendation": (
                "Review major operating costs and identify "
                "opportunities to improve efficiency."
            ),
            "metric": ratio,
        })

    elif ratio > 70:
        insights.append({
            "type": "info",
            "title": "Moderate Expense Pressure",
            "message": (
                f"Operating expenses consume {ratio:.1f}% of revenue."
            ),
            "recommendation": (
                "Monitor expense growth and compare major "
                "cost categories against revenue."
            ),
            "metric": ratio,
        })

    elif ratio <= 50:
        insights.append({
            "type": "success",
            "title": "Strong Cost Structure",
            "message": (
                f"Operating expenses consume {ratio:.1f}% of revenue, "
                "leaving a relatively strong operating margin."
            ),
            "recommendation": (
                "Continue monitoring costs while protecting "
                "the current operating structure."
            ),
            "metric": ratio,
        })

    return insights


def check_cashflow_stress(metrics):
    """
    Generate insights from projected cash-flow stress.

    This function assumes the source field is represented as a
    decimal between 0 and 1.

    Example:
        0.25 = 25% stress
        0.50 = 50% stress
        0.75 = 75% stress
    """

    stress = metrics.get("cashflow_stress_rate")

    if stress is None:
        return []

    stress = float(stress)

    if stress >= 0.75:
        return [{
            "type": "warning",
            "title": "High Cash-Flow Stress",
            "message": (
                f"Projected cash-flow stress is approximately "
                f"{stress:.0%}."
            ),
            "recommendation": (
                "Review upcoming obligations, operating costs, "
                "collections, and available cash reserves."
            ),
            "metric": stress,
        }]

    if stress >= 0.50:
        return [{
            "type": "warning",
            "title": "Elevated Cash-Flow Stress",
            "message": (
                f"Projected cash-flow stress is approximately "
                f"{stress:.0%}."
            ),
            "recommendation": (
                "Monitor near-term cash requirements and "
                "outstanding receivables closely."
            ),
            "metric": stress,
        }]

    if stress >= 0.25:
        return [{
            "type": "info",
            "title": "Moderate Cash-Flow Pressure",
            "message": (
                f"Projected cash-flow stress is approximately "
                f"{stress:.0%}."
            ),
            "recommendation": (
                "Monitor upcoming expenses and expected "
                "customer collections."
            ),
            "metric": stress,
        }]

    return [{
        "type": "success",
        "title": "Low Projected Cash-Flow Stress",
        "message": (
            f"Projected cash-flow stress is approximately "
            f"{stress:.0%}."
        ),
        "recommendation": (
            "Continue monitoring cash requirements as "
            "business conditions change."
        ),
        "metric": stress,
    }]


def check_revenue_stability(metrics):
    """Generate insights from revenue variability."""

    monthly = metrics.get("monthly_revenue", [])

    if not monthly:
        return [{
            "type": "info",
            "title": "Revenue Stability Unavailable",
            "message": (
                "There is not enough monthly revenue data "
                "to evaluate revenue stability."
            ),
            "recommendation": (
                "Upload additional historical periods for a "
                "more reliable stability assessment."
            ),
        }]

    if len(monthly) < 3:
        return [{
            "type": "info",
            "title": "Limited Revenue History",
            "message": (
                f"Only {len(monthly)} revenue period(s) are available "
                "for the stability analysis."
            ),
            "recommendation": (
                "Use at least three months of historical data "
                "for a more meaningful stability assessment."
            ),
        }]

    values = [float(value) for value in monthly]

    mean_revenue = sum(values) / len(values)

    if mean_revenue <= 0:
        return []

    variance = sum(
        (value - mean_revenue) ** 2
        for value in values
    ) / len(values)

    standard_deviation = variance ** 0.5
    coefficient_of_variation = standard_deviation / mean_revenue

    if coefficient_of_variation < 0.15:
        return [{
            "type": "success",
            "title": "Stable Revenue Pattern",
            "message": (
                "Historical monthly revenue shows relatively "
                "low variability."
            ),
            "recommendation": (
                "Continue monitoring revenue concentration "
                "and recurring customer activity."
            ),
            "metric": coefficient_of_variation,
        }]

    if coefficient_of_variation < 0.30:
        return [{
            "type": "info",
            "title": "Moderate Revenue Variability",
            "message": (
                "Monthly revenue shows some variation across "
                "the available historical periods."
            ),
            "recommendation": (
                "Monitor seasonal patterns and identify "
                "drivers of month-to-month changes."
            ),
            "metric": coefficient_of_variation,
        }]

    return [{
        "type": "warning",
        "title": "High Revenue Variability",
        "message": (
            "Historical monthly revenue shows significant "
            "month-to-month variation."
        ),
        "recommendation": (
            "Investigate seasonal patterns, customer concentration, "
            "and recurring versus one-time revenue."
        ),
        "metric": coefficient_of_variation,
    }]


def check_financial_risk(metrics):
    """Generate insights from loan balance relative to revenue."""

    revenue = float(
        metrics.get(
            "total_revenue",
            0
        )
    )

    loan_balance = float(
        metrics.get(
            "loan_balance",
            0
        )
    )

    if revenue <= 0:
        return []

    debt_to_revenue = loan_balance / revenue

    if debt_to_revenue > 2:
        return [{
            "type": "warning",
            "title": "High Debt Relative to Revenue",
            "message": (
                "Loan balance is more than twice the current "
                "revenue level in the analyzed dataset."
            ),
            "recommendation": (
                "Review debt obligations, repayment schedules, "
                "and available cash resources."
            ),
            "metric": debt_to_revenue,
        }]

    if debt_to_revenue > 1:
        return [{
            "type": "warning",
            "title": "Elevated Debt Exposure",
            "message": (
                "Loan balance is greater than the analyzed "
                "revenue level."
            ),
            "recommendation": (
                "Monitor debt servicing requirements and "
                "near-term cash availability."
            ),
            "metric": debt_to_revenue,
        }]

    if debt_to_revenue <= 0.25:
        return [{
            "type": "success",
            "title": "Limited Debt Exposure",
            "message": (
                "Loan balance is relatively low compared with "
                "the analyzed revenue level."
            ),
            "recommendation": (
                "Continue monitoring debt obligations as the "
                "business grows."
            ),
            "metric": debt_to_revenue,
        }]

    return []


