import pandas as pd
import numpy as np


def calculate_forecast(df: pd.DataFrame, dataset_type: str):
    if dataset_type == "business":
        return business_forecast(df)
    if dataset_type == "transaction":
        return transaction_forecast(df)
    return {"revenue": 0, "expenses": 0, "profit": 0, "margin": 0}


def business_forecast(df: pd.DataFrame):
    if "month" not in df.columns:
        return {"revenue": 0, "expenses": 0, "profit": 0, "margin": 0}

    monthly = (
        df.groupby("month")
          .agg(
              revenue=("revenue_usd", "sum"),
              expenses=("opex_usd", "sum")
          )
          .sort_index()
    )

    if monthly.empty:
        return {"revenue": 0, "expenses": 0, "profit": 0, "margin": 0}

    monthly["profit"] = monthly["revenue"] - monthly["expenses"]
    return linear_forecast(monthly)

def transaction_forecast(df: pd.DataFrame):
    if "Date" not in df.columns or "Type" not in df.columns or "Amount" not in df.columns:
        return {"revenue": 0, "expenses": 0, "profit": 0, "margin": 0}

    working = df.copy()
    working["Date"] = pd.to_datetime(working["Date"], errors="coerce")
    working = working.dropna(subset=["Date"])
    if working.empty:
        return {"revenue": 0, "expenses": 0, "profit": 0, "margin": 0}

    working["Month"] = working["Date"].dt.to_period("M")

    revenue = (
        working[working["Type"] == "Income"]
        .groupby("Month")["Amount"].sum()
    )
    expenses = (
        working[working["Type"] == "Expense"]
        .groupby("Month")["Amount"].sum()
    )

    monthly = pd.DataFrame({"revenue": revenue, "expenses": expenses}).fillna(0)
    if monthly.empty:
        return {"revenue": 0, "expenses": 0, "profit": 0, "margin": 0}

    monthly["profit"] = monthly["revenue"] - monthly["expenses"]
    return linear_forecast(monthly)

def linear_forecast(monthly):

    forecast = {}

    for column in [

        "revenue",

        "expenses",

        "profit"

    ]:

        values = monthly[column].values

        x = np.arange(len(values))

        slope, intercept = np.polyfit(x, values, 1)

        next_month = intercept + slope * len(values)

        forecast[column] = next_month

    forecast["margin"] = (

        forecast["profit"] /

        forecast["revenue"] * 100

        if forecast["revenue"] > 0

        else 0

    )

    return forecast       