import statistics


def calculate_health_score(metrics: dict) -> dict:
    """
    Calculate an overall Business Health Score.

    The score is based on:
        - Profitability: 30 points
        - Expense Control: 20 points
        - Activity: 15 points
        - Revenue Stability: 20 points
        - Data Quality: 15 points

    Returns:
        {
            "score": int,
            "status": str,
            "breakdown": dict
        }
    """

    breakdown = {}

    margin = float(metrics.get("profit_margin", 0) or 0)
    if margin >= 30:
        profit_score = 30
    elif margin >= 20:
        profit_score = 24
    elif margin >= 10:
        profit_score = 18
    elif margin >= 5:
        profit_score = 12
    else:
        profit_score = 5

    breakdown["Profitability"] = profit_score

    expense_ratio = metrics.get("expense_ratio")
    if expense_ratio is None:
        revenue = float(metrics.get("total_revenue", 0) or 0)
        expenses = float(metrics.get("total_expenses", 0) or 0)
        if revenue > 0:
            expense_ratio = (expenses / revenue) * 100
        else:
            expense_ratio = 100

    expense_ratio = float(expense_ratio)
    if expense_ratio <= 50:
        expense_score = 20
    elif expense_ratio <= 70:
        expense_score = 15
    elif expense_ratio <= 85:
        expense_score = 10
    else:
        expense_score = 5

    breakdown["Expense Control"] = expense_score

    transactions = int(metrics.get("transaction_count", metrics.get("records_processed", 0)) or 0)
    if transactions >= 1000:
        activity_score = 15
    elif transactions >= 500:
        activity_score = 12
    elif transactions >= 250:
        activity_score = 10
    elif transactions >= 100:
        activity_score = 7
    else:
        activity_score = 5

    breakdown["Activity"] = activity_score

    monthly = metrics.get("monthly_revenue", [])
    if len(monthly) > 1:
        try:
            monthly_values = [float(value) for value in monthly if value is not None]
            mean = statistics.mean(monthly_values)
            stdev = statistics.pstdev(monthly_values)
            cv = stdev / abs(mean) if mean != 0 else float("inf")
        except (TypeError, ValueError, statistics.StatisticsError):
            cv = float("inf")

        if cv < 0.15:
            stability_score = 20
        elif cv < 0.30:
            stability_score = 16
        elif cv < 0.45:
            stability_score = 12
        else:
            stability_score = 8
    else:
        stability_score = 10

    breakdown["Revenue Stability"] = stability_score

    quality_score = 15
    breakdown["Data Quality"] = quality_score

    total = int(sum(breakdown.values()))
    if total >= 90:
        status = "Excellent"
    elif total >= 75:
        status = "Healthy"
    elif total >= 60:
        status = "Stable"
    elif total >= 40:
        status = "Needs Attention"
    else:
        status = "Critical"

    return {
        "score": total,
        "status": status,
        "breakdown": breakdown,
    }

