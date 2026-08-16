from openpyxl.styles import Font, Alignment


def create_summary_section(ws, summary):

    ws.merge_cells(
        "A13:H16"
    )

    cell = ws["A13"]

    cell.value = (
        "Executive Summary\n\n"
        + summary
    )

    cell.font = Font(
        size=12
    )

    cell.alignment = Alignment(
        wrap_text=True,
        vertical="top"
    )

    return ws
    def generate_executive_summary(results):

    summary = []

    # -----------------------------
    # Financial Performance
    # -----------------------------

    revenue = results.get(
        "total_revenue",
        0
    )

    expenses = results.get(
        "total_expenses",
        0
    )

    profit = results.get(
        "net_profit",
        0
    )

    margin = results.get(
        "profit_margin",
        0
    )


    summary.append(
        f"Revenue totaled ${revenue:,.2f} "
        f"with net profit of ${profit:,.2f} "
        f"and a profit margin of {margin:.1f}%."
    )


    # -----------------------------
    # Expense Analysis
    # -----------------------------

    expense_ratio = results.get(
        "expense_ratio",
        0
    )

    if expense_ratio > 80:

        summary.append(
            f"Operating expenses are elevated, "
            f"consuming {expense_ratio:.1f}% "
            "of revenue."
        )

    elif expense_ratio < 60:

        summary.append(
            f"Expense management is strong, "
            f"with expenses representing "
            f"{expense_ratio:.1f}% of revenue."
        )


    # -----------------------------
    # Health Score
    # -----------------------------

    health_score = results.get(
        "health_score",
        0
    )

    health_status = results.get(
        "health_status",
        "Unknown"
    )


    summary.append(
        f"Business health score is "
        f"{health_score}/100, classified as "
        f"{health_status}."
    )


    # -----------------------------
    # Trends
    # -----------------------------

    trends = results.get(
        "trends",
        {}
    )

    trend_summary = trends.get(
        "summary",
        {}
    )


    revenue_trend = trend_summary.get(
        "revenue_trend"
    )

    profit_trend = trend_summary.get(
        "profit_trend"
    )


    if revenue_trend:

        summary.append(
            f"Revenue trend is currently "
            f"{revenue_trend.lower()}."
        )


    if profit_trend:

        summary.append(
            f"Profit trend is currently "
            f"{profit_trend.lower()}."
        )


    # -----------------------------
    # Forecast
    # -----------------------------

    forecast = results.get(
        "forecast",
        {}
    )


    if forecast:

        forecast_profit = forecast.get(
            "profit",
            0
        )

        summary.append(
            f"Forecasted profit is "
            f"${forecast_profit:,.2f}."
        )


    return " ".join(summary)