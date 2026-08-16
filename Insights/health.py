import statistics


def calculate_health_score(metrics: dict) -> dict:
    """
    Calculates an overall Business Health Score.
    Returns:
        {
            "score": 87,
            "status": "Healthy",
            "breakdown": {...}
        }
    """

    breakdown = {}

    # ------------------------
    # Profit Margin (30 pts)
    # ------------------------

    margin = metrics["profit_margin"]

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

    # ------------------------
    # Expense Control (20 pts)
    # ------------------------

    expense_ratio = metrics["expense_ratio"]

    if expense_ratio <= 50:
        expense_score = 20
    elif expense_ratio <= 70:
        expense_score = 15
    elif expense_ratio <= 85:
        expense_score = 10
    else:
        expense_score = 5

    breakdown["Expense Control"] = expense_score

    # ------------------------
    # Transaction Activity (15 pts)
    # ------------------------

    transactions = metrics["transaction_count"]

    if transactions >= 1000:
        transaction_score = 15
    elif transactions >= 500:
        transaction_score = 12
    elif transactions >= 250:
        transaction_score = 10
    elif transactions >= 100:
        transaction_score = 7
    else:
        transaction_score = 5

    breakdown["Activity"] = transaction_score

    # ------------------------
    # Revenue Stability (20 pts)
    # ------------------------

    monthly = metrics.get("monthly_revenue", [])

    if len(monthly) > 1:
        try:
            mean = statistics.mean(monthly)
            # population stdev to reflect full months
            stdev = statistics.pstdev(monthly)
            cv = stdev / mean if mean else float("inf")
        except Exception:
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

    # ------------------------
    # Data Quality (15 pts)
    # ------------------------

    quality_score = 15

    breakdown["Data Quality"] = quality_score

    # ------------------------
    # Final Score
    # ------------------------

    total = sum(breakdown.values())

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