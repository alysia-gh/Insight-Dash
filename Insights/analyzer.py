from .rules import (
    check_profit_margin,
    check_largest_expense,
    check_expense_ratio,
    check_cashflow_stress,
    check_revenue_stability,
    check_financial_risk,
)


def generate_insights(metrics):
    """
    Generate business insights based on the detected dataset type.
    """

    insights = []

    insights.extend(check_profit_margin(metrics))
    insights.extend(check_revenue_stability(metrics))

    dataset_type = metrics.get("dataset_type")

    if dataset_type == "transaction":
        insights.extend(check_largest_expense(metrics))
        insights.extend(check_expense_ratio(metrics))
    elif dataset_type == "business":
        insights.extend(check_expense_ratio(metrics))
        insights.extend(check_cashflow_stress(metrics))
        insights.extend(check_financial_risk(metrics))

    return insights
