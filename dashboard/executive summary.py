def generate_executive_summary(metrics):

    revenue = metrics["total_revenue"]
    profit = metrics["net_profit"]
    margin = metrics["profit_margin"]

    summary = (
        f"Revenue totaled ${revenue:,.0f}. "
        f"The business generated ${profit:,.0f} in net profit "
        f"with a profit margin of {margin:.1f}%."
    )

    if metrics["expense_ratio"] > 80:
        summary += (
            " Operating expenses are elevated and should be monitored."
        )

    return summary