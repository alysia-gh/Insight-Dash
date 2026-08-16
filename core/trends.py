import pandas as pd


def calculate_trends(df: pd.DataFrame, dataset_type: str) -> dict:
    """Main trend router."""
    if dataset_type == "business":
        return calculate_business_trends(df)
    elif dataset_type == "transaction":
        return calculate_transaction_trends(df)
    return {"monthly": None, "summary": {}}


def calculate_business_trends(df: pd.DataFrame) -> dict:
    if "month" not in df.columns:
        return {"monthly": None, "summary": {}}

    monthly = (
        df.groupby("month")
          .agg(
              revenue=("revenue_usd", "sum"),
              expenses=("opex_usd", "sum")
          )
          .sort_index()
    )

    monthly["profit"] = monthly["revenue"] - monthly["expenses"]
    monthly["margin"] = monthly["profit"] / monthly["revenue"].replace(0, pd.NA) * 100
    monthly["revenue_growth"] = monthly["revenue"].pct_change() * 100
    monthly["expense_growth"] = monthly["expenses"].pct_change() * 100
    monthly["profit_growth"] = monthly["profit"].pct_change() * 100
    monthly["revenue_ma3"] = monthly["revenue"].rolling(3).mean()
    monthly["expense_ma3"] = monthly["expenses"].rolling(3).mean()
    monthly["profit_ma3"] = monthly["profit"].rolling(3).mean()

    summary = {
        "best_revenue_month": monthly["revenue"].idxmax() if not monthly.empty else None,
        "worst_revenue_month": monthly["revenue"].idxmin() if not monthly.empty else None,
        "best_profit_month": monthly["profit"].idxmax() if not monthly.empty else None,
        "worst_profit_month": monthly["profit"].idxmin() if not monthly.empty else None,
        "average_monthly_revenue": monthly["revenue"].mean() if not monthly.empty else 0,
        "average_monthly_profit": monthly["profit"].mean() if not monthly.empty else 0,
        "revenue_volatility": monthly["revenue"].std() if not monthly.empty else 0,
        "profit_volatility": monthly["profit"].std() if not monthly.empty else 0,
        "revenue_trend": get_trend_direction(monthly["revenue_growth"] if not monthly.empty else pd.Series([], dtype="float64")),
        "profit_trend": get_trend_direction(monthly["profit_growth"] if not monthly.empty else pd.Series([], dtype="float64")),
    }

    return {"monthly": monthly, "summary": summary}


def calculate_transaction_trends(df: pd.DataFrame) -> dict:
    if "Date" not in df.columns or "Type" not in df.columns or "Amount" not in df.columns:
        return {"monthly": None, "summary": {}}

    working = df.copy()
    working["Date"] = pd.to_datetime(working["Date"], errors="coerce")
    working = working.dropna(subset=["Date"])
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
    monthly["profit"] = monthly["revenue"] - monthly["expenses"]
    monthly["margin"] = monthly["profit"] / monthly["revenue"].replace(0, pd.NA) * 100
    monthly["revenue_growth"] = monthly["revenue"].pct_change() * 100
    monthly["expense_growth"] = monthly["expenses"].pct_change() * 100
    monthly["profit_growth"] = monthly["profit"].pct_change() * 100
    monthly["revenue_ma3"] = monthly["revenue"].rolling(3).mean()
    monthly["expense_ma3"] = monthly["expenses"].rolling(3).mean()
    monthly["profit_ma3"] = monthly["profit"].rolling(3).mean()

    summary = {
        "best_revenue_month": monthly["revenue"].idxmax() if not monthly.empty else None,
        "worst_revenue_month": monthly["revenue"].idxmin() if not monthly.empty else None,
        "best_profit_month": monthly["profit"].idxmax() if not monthly.empty else None,
        "worst_profit_month": monthly["profit"].idxmin() if not monthly.empty else None,
        "average_monthly_revenue": monthly["revenue"].mean() if not monthly.empty else 0,
        "average_monthly_profit": monthly["profit"].mean() if not monthly.empty else 0,
        "revenue_volatility": monthly["revenue"].std() if not monthly.empty else 0,
        "profit_volatility": monthly["profit"].std() if not monthly.empty else 0,
        "revenue_trend": get_trend_direction(monthly["revenue_growth"] if not monthly.empty else pd.Series([], dtype="float64")),
        "profit_trend": get_trend_direction(monthly["profit_growth"] if not monthly.empty else pd.Series([], dtype="float64")),
    }

    return {"monthly": monthly, "summary": summary}


def get_trend_direction(series):
    latest = series.dropna()
    if latest.empty:
        return "Stable"

    latest = latest.iloc[-1]
    if latest > 5:
        return "Improving"
    elif latest < -5:
        return "Declining"
    return "Stable"