def check_profit_margin(metrics):

    insights = []

    margin = metrics["profit_margin"]

    if margin >= 30:

        insights.append({

            "type": "success",

            "title": "Strong Profitability",

            "message": (
                f"Profit margin is {margin:.1f}%, "
                "which indicates strong financial performance."
            )

        })

    elif margin < 10:

        insights.append({
            "type": "warning",
            "title": "Low Profit Margin",
            "message": (
                f"Profit margin is {margin:.1f}%, which is below recommended levels."
            ),
            "recommendation": "Review pricing strategy and operating expenses.",
            "metric": float(margin),
        })

    return insights
def check_largest_expense(metrics):

    insights = []

    category = metrics["largest_expense_category"]

    amount = metrics["largest_expense_amount"]

    insights.append({

        "type": "info",

        "title": "Largest Expense",

        "message": (
            f"{category} is currently the largest expense "
            f"at ${amount:,.2f}."
        )

    })

    return insights

def check_expense_ratio(metrics):

    insights = []

    ratio = metrics["expense_ratio"]

    if ratio > 80:
        insights.append({
            "type": "warning",
            "title": "High Operating Expenses",
            "message": f"Expenses consume {ratio:.1f}% of revenue.",
            "recommendation": "Review operating costs and improve efficiency."
        })

    elif ratio < 60:
        insights.append({
            "type": "success",
            "title": "Healthy Cost Structure",
            "message": f"Expenses are only {ratio:.1f}% of revenue."
        })

    return insights

def check_cashflow_stress(metrics):

    insights = []

    stress = metrics.get("cashflow_stress_rate")

    if stress is None:
        return insights

    if stress > 0.50:
        insights.append({
            "type": "warning",
            "title": "Possible Cashflow Stress",
            "message": "Cashflow stress risk is elevated.",
            "recommendation": "Review operating costs, vendor contracts, and staffing efficiency."
        })

    return insights