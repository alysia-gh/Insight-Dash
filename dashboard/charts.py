import pandas as pd

from dashboard.chart_style import (
    COLORS,
    compact_currency,
    compact_percent,
    create_figure,
    clean_axis,
    format_month_labels,
    save_figure_to_bytes,
    value_formatter,
)
from dashboard.chart_images import insert_chart_image


def create_financial_performance_chart(data_ws, results, chart_ws=None, chart_cell="A1"):
    trends = results.get("trends", {})
    monthly = trends.get("monthly")
    if monthly is None or monthly.empty:
        return

    chart_data = monthly[["revenue", "expenses", "profit"]].fillna(0)
    categories = format_month_labels(chart_data.index)

    fig, ax = create_figure(figsize=(10, 4), dpi=170)
    x = pd.RangeIndex(len(categories))
    width = 0.25

    ax.bar(x - width, chart_data["revenue"], width=width, color=COLORS["primary"], label="Revenue")
    ax.bar(x, chart_data["expenses"], width=width, color=COLORS["danger"], label="Expenses")
    ax.bar(x + width, chart_data["profit"], width=width, color=COLORS["success"], label="Net Profit")

    ax.set_title("Financial Performance Overview")
    ax.set_xticks(x)
    ax.set_xticklabels(categories, rotation=45, ha="right")
    ax.set_ylabel("USD")
    ax.yaxis.set_major_formatter(value_formatter(currency=True))
    ax.legend(frameon=False, loc="upper right")
    clean_axis(ax, grid=True, show_x=True, show_y=True)
    fig.tight_layout(pad=1.2)

    image_buffer = save_figure_to_bytes(fig)
    target_ws = chart_ws if chart_ws is not None else data_ws
    insert_chart_image(target_ws, image_buffer, chart_cell)


def create_profitability_trend_chart(data_ws, results, chart_ws=None, chart_cell="L1"):
    trends = results.get("trends", {})
    monthly = trends.get("monthly")
    if monthly is None or monthly.empty:
        return

    categories = format_month_labels(monthly.index)
    values = monthly["margin"].fillna(0)

    fig, ax = create_figure(figsize=(8, 4), dpi=170)
    x = pd.RangeIndex(len(categories))
    ax.plot(x, values, marker="o", color=COLORS["secondary"], linewidth=2)
    ax.fill_between(x, values, alpha=0.08, color=COLORS["secondary"])

    ax.set_title("Profitability Trend")
    ax.set_ylabel("Profit Margin")
    ax.set_xticks(x)
    ax.set_xticklabels(categories, rotation=45, ha="right")
    ax.yaxis.set_major_formatter(value_formatter(percent=True))
    clean_axis(ax, grid=True, show_x=True, show_y=True)
    fig.tight_layout(pad=1.2)

    image_buffer = save_figure_to_bytes(fig)
    target_ws = chart_ws if chart_ws is not None else data_ws
    insert_chart_image(target_ws, image_buffer, chart_cell)


def create_expense_analysis_chart(data_ws, results, chart_ws=None, chart_cell="A20"):
    expense_by_category = results.get("expense_by_category")
    if expense_by_category is None or expense_by_category.empty:
        return

    chart_data = expense_by_category.sort_values(ascending=True)
    categories = [str(category) for category in chart_data.index]
    values = chart_data.values

    fig, ax = create_figure(figsize=(9, 4), dpi=170)
    ax.barh(categories, values, color=COLORS["warning"])

    ax.set_title("Expense Analysis")
    ax.set_xlabel("USD")
    ax.xaxis.set_major_formatter(value_formatter(currency=True))
    clean_axis(ax, grid=True, show_x=True, show_y=True)
    fig.tight_layout(pad=1.2)

    image_buffer = save_figure_to_bytes(fig)
    target_ws = chart_ws if chart_ws is not None else data_ws
    insert_chart_image(target_ws, image_buffer, chart_cell)


def create_forecast_comparison_chart(data_ws, results, chart_ws=None, chart_cell="L20"):
    forecast = results.get("forecast", {})
    actual = {
        "Revenue": results.get("total_revenue", 0),
        "Expenses": results.get("total_expenses", 0),
        "Profit": results.get("net_profit", 0),
    }
    projected = {
        "Revenue": forecast.get("revenue", 0),
        "Expenses": forecast.get("expenses", 0),
        "Profit": forecast.get("profit", 0),
    }

    categories = list(actual.keys())
    actual_values = [actual[key] for key in categories]
    projected_values = [projected[key] for key in categories]

    x = pd.RangeIndex(len(categories))
    width = 0.35

    fig, ax = create_figure(figsize=(9, 4), dpi=170)
    ax.bar(x - width / 2, actual_values, width=width, color=COLORS["primary"], label="Actual")
    ax.bar(x + width / 2, projected_values, width=width, color=COLORS["secondary"], alpha=0.8, label="Forecast")

    ax.set_title("Forecast vs Actual Performance")
    ax.set_xticks(x)
    ax.set_xticklabels(categories)
    ax.set_ylabel("USD")
    ax.yaxis.set_major_formatter(value_formatter(currency=True))
    ax.legend(frameon=False)
    clean_axis(ax, grid=True, show_x=True, show_y=True)
    fig.tight_layout(pad=1.2)

    image_buffer = save_figure_to_bytes(fig)
    target_ws = chart_ws if chart_ws is not None else data_ws
    insert_chart_image(target_ws, image_buffer, chart_cell)


def create_health_score_kpi(data_ws, results, chart_ws=None, chart_cell="J38"):
    score = results.get("health_score", 0)
    status = results.get("health_status", "Unknown")

    fig, ax = create_figure(figsize=(4, 3), dpi=170)
    ax.text(
        0.5,
        0.62,
        f"{score:.0f}",
        ha="center",
        va="center",
        fontsize=42,
        fontweight="bold",
        color=COLORS["success"] if score >= 70 else COLORS["warning"] if score >= 40 else COLORS["danger"],
    )
    ax.text(
        0.5,
        0.25,
        status,
        ha="center",
        va="center",
        fontsize=14,
        color=COLORS["text"],
    )
    ax.set_title("Business Health")
    ax.set_xticks([])
    ax.set_yticks([])
    clean_axis(ax, grid=False, show_x=False, show_y=False)
    fig.tight_layout(pad=1.2)

    image_buffer = save_figure_to_bytes(fig)
    target_ws = chart_ws if chart_ws is not None else data_ws
    insert_chart_image(target_ws, image_buffer, chart_cell)
