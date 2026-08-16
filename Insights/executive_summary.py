def generate_executive_summary(results):

    summary = []

    revenue = results.get("total_revenue", 0)
    expenses = results.get("total_expenses", 0)
    profit = results.get("net_profit", 0)
    margin = results.get("profit_margin", 0)

    summary.append(
        f"Revenue totaled ${revenue:,.2f} "
        f"with net profit of ${profit:,.2f} "
        f"and a profit margin of {margin:.1f}%."
    )

    expense_ratio = results.get("expense_ratio", 0)

    if expense_ratio > 80:
        summary.append(
            f"Operating expenses are elevated, consuming {expense_ratio:.1f}% of revenue."
        )
    elif expense_ratio < 60:
        summary.append(
            f"Expense management is strong, with expenses representing {expense_ratio:.1f}% of revenue."
        )

    health_score = results.get("health_score", 0)
    health_status = results.get("health_status", "Unknown")

    summary.append(
        f"Business health score is {health_score}/100, classified as {health_status}."
    )

    trends = results.get("trends", {})
    trend_summary = trends.get("summary", {})

    revenue_trend = trend_summary.get("revenue_trend")
    profit_trend = trend_summary.get("profit_trend")

    if revenue_trend:
        summary.append(f"Revenue trend is currently {revenue_trend.lower()}.")

    if profit_trend:
        summary.append(f"Profit trend is currently {profit_trend.lower()}.")

    forecast = results.get("forecast", {})
    if forecast:
        forecast_profit = forecast.get("profit", 0)
        summary.append(f"Forecasted profit is ${forecast_profit:,.2f}.")

    return " ".join(summary)
