from .rules import (
    check_profit_margin,
    check_largest_expense,
    check_expense_ratio,
    check_cashflow_stress,
)


def generate_insights(metrics):

    insights = []

    # Rules shared by all datasets
    insights.extend(check_profit_margin(metrics))

    dataset_type = metrics.get("dataset_type")

    if dataset_type == "transaction":
        insights.extend(check_largest_expense(metrics))

    elif dataset_type == "business":
        insights.extend(check_expense_ratio(metrics))
        insights.extend(check_cashflow_stress(metrics))

    return insights