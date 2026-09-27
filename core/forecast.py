import numpy as np
import pandas as pd


DEFAULT_FORECAST = {
    "revenue": 0.0,
    "expenses": 0.0,
    "profit": 0.0,
    "margin": 0.0,
    "period": "Next Month",
    "months_used": 0,
    "months_forecast": 1,
    "forecast_quality": "Insufficient Data",
    "historical_start": None,
    "historical_end": None,
}


FORECAST_PERIODS = {
    "Next Month": 1,
    "Next Quarter": 3,
    "Next 6 Months": 6,
    "Next Year": 12,
}


def calculate_forecast(
    df: pd.DataFrame,
    dataset_type: str,
    forecast_period: str = "Next Month",
) -> dict:
    """
    Calculate a forward financial forecast.

    Supports:
        - transaction datasets
        - business datasets

    Forecast method:
        Linear trend based on historical monthly results.

    forecast_period:
        Next Month
        Next Quarter
        Next 6 Months
        Next Year
    """

    if forecast_period not in FORECAST_PERIODS:
        forecast_period = "Next Month"

    if dataset_type == "business":
        return business_forecast(
            df,
            forecast_period,
        )

    if dataset_type == "transaction":
        return transaction_forecast(
            df,
            forecast_period,
        )

    return {
        **DEFAULT_FORECAST,
        "period": forecast_period,
    }


# ============================================================
# BUSINESS FORECAST
# ============================================================


def business_forecast(
    df: pd.DataFrame,
    forecast_period: str = "Next Month",
) -> dict:
    """
    Forecast business revenue, expenses, and profit
    using monthly business financial data.
    """

    if "month" not in df.columns:
        return {
            **DEFAULT_FORECAST,
            "period": forecast_period,
        }

    required_columns = [
        "revenue_usd",
        "opex_usd",
    ]

    if not all(column in df.columns for column in required_columns):
        return {
            **DEFAULT_FORECAST,
            "period": forecast_period,
        }

    working = df.copy()
    working["month"] = pd.to_datetime(working["month"], errors="coerce").dt.to_period("M")
    working = working.dropna(subset=["month"])

    if working.empty:
        return {
            **DEFAULT_FORECAST,
            "period": forecast_period,
        }

    working["revenue_usd"] = pd.to_numeric(working["revenue_usd"], errors="coerce").fillna(0)
    working["opex_usd"] = pd.to_numeric(working["opex_usd"], errors="coerce").fillna(0)

    monthly = (
        working.groupby("month")
        .agg(
            revenue=("revenue_usd", "sum"),
            expenses=("opex_usd", "sum"),
        )
        .sort_index()
    )

    if monthly.empty:
        return {
            **DEFAULT_FORECAST,
            "period": forecast_period,
        }

    monthly["profit"] = monthly["revenue"] - monthly["expenses"]
    return linear_forecast(monthly, forecast_period)


# ============================================================
# TRANSACTION FORECAST
# ============================================================


def transaction_forecast(
    df: pd.DataFrame,
    forecast_period: str = "Next Month",
) -> dict:
    """
    Forecast revenue, expenses, and profit
    from a transaction ledger.
    """

    required_columns = [
        "Date",
        "Type",
        "Amount",
    ]

    if not all(column in df.columns for column in required_columns):
        return {
            **DEFAULT_FORECAST,
            "period": forecast_period,
        }

    working = df.copy()
    working["Date"] = pd.to_datetime(working["Date"], errors="coerce")
    working["Amount"] = pd.to_numeric(working["Amount"], errors="coerce")
    working["Type"] = working["Type"].astype(str).str.strip().str.title()
    working = working.dropna(subset=["Date", "Amount"])

    if working.empty:
        return {
            **DEFAULT_FORECAST,
            "period": forecast_period,
        }

    working["Month"] = working["Date"].dt.to_period("M")

    revenue = working[working["Type"] == "Income"].groupby("Month")["Amount"].sum()
    expenses = working[working["Type"] == "Expense"].groupby("Month")["Amount"].sum()
    monthly = pd.DataFrame({"revenue": revenue, "expenses": expenses}).fillna(0).sort_index()

    if monthly.empty:
        return {
            **DEFAULT_FORECAST,
            "period": forecast_period,
        }

    monthly["profit"] = monthly["revenue"] - monthly["expenses"]
    return linear_forecast(monthly, forecast_period)


# ============================================================
# LINEAR FORECAST ENGINE
# ============================================================

def linear_forecast(
    monthly: pd.DataFrame,
    forecast_period: str = "Next Month",
) -> dict:
    """
    Generate a simple linear trend forecast.

    The model uses historical monthly observations
    to estimate the requested future period.

    This is intentionally transparent and lightweight
    for the V2 release.
    """

    if monthly.empty:
        return {
            **DEFAULT_FORECAST,
            "period": forecast_period,
        }

    months_ahead = FORECAST_PERIODS.get(forecast_period, 1)
    number_of_months = len(monthly)

    if number_of_months < 2:
        forecast_quality = "Insufficient Data"
    elif number_of_months < 4:
        forecast_quality = "Limited History"
    elif number_of_months < 6:
        forecast_quality = "Moderate History"
    else:
        forecast_quality = "Strong History"

    x = np.arange(number_of_months, dtype=float)
    future_x = np.arange(number_of_months, number_of_months + months_ahead, dtype=float)

    projected = {}

    for column in ["revenue", "expenses"]:
        values = pd.to_numeric(monthly[column], errors="coerce").fillna(0).to_numpy()

        if len(values) == 1:
            projected_values = np.repeat(values[0], months_ahead)
        else:
            slope, intercept = np.polyfit(x, values, 1)
            projected_values = intercept + slope * future_x

        projected_values = np.maximum(projected_values, 0)
        projected[column] = float(projected_values.sum())

    projected["profit"] = float(projected["revenue"] - projected["expenses"])
    projected["margin"] = (
        (projected["profit"] / projected["revenue"]) * 100 if projected["revenue"] > 0 else 0
    )

    projected["period"] = forecast_period
    projected["months_forecast"] = months_ahead
    projected["months_used"] = number_of_months
    projected["forecast_quality"] = forecast_quality

    if hasattr(monthly.index, "min") and not monthly.empty:
        projected["historical_start"] = str(monthly.index.min())
        projected["historical_end"] = str(monthly.index.max())
    else:
        projected["historical_start"] = None
        projected["historical_end"] = None

    return projected

