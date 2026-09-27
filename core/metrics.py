import pandas as pd

from core.trends import calculate_trends
from core.validator import detect_dataset_type


def calculate_metrics(
    df: pd.DataFrame,
    dataset_type: str = None,
) -> dict:
    """
    Main metrics router.

    Handles:
        - transaction ledger datasets
        - business financial datasets
    """

    if dataset_type is None:
        dataset_type = detect_dataset_type(df)

    if dataset_type == "transaction":
        return calculate_transaction_metrics(df)

    if dataset_type == "business":
        return calculate_business_metrics(df)

    raise ValueError(
        f"Unsupported dataset type: {dataset_type}"
    )


# ============================================================
# TRANSACTION LEDGER METRICS
# ============================================================


def calculate_transaction_metrics(
    df: pd.DataFrame,
) -> dict:
    """
    Calculate financial metrics from a transaction ledger.

    Expected columns:
        Date
        Description
        Category
        Amount
        Type
    """

    print(
        f"Processing {len(df):,} transactions"
    )

    working_df = df.copy()

    # --------------------------------------------------------
    # Normalize transaction fields
    # --------------------------------------------------------

    working_df["Date"] = pd.to_datetime(
        working_df["Date"],
        errors="coerce",
    )

    working_df["Amount"] = pd.to_numeric(
        working_df["Amount"],
        errors="coerce",
    )

    working_df["Type"] = (
        working_df["Type"]
        .astype(str)
        .str.strip()
        .str.title()
    )

    # --------------------------------------------------------
    # Income / expense separation
    # --------------------------------------------------------

    income = working_df[
        working_df["Type"] == "Income"
    ]

    expenses = working_df[
        working_df["Type"] == "Expense"
    ]

    total_revenue = float(
        income["Amount"].sum()
    )

    total_expenses = float(
        expenses["Amount"].sum()
    )

    net_profit = (
        total_revenue
        - total_expenses
    )

    # --------------------------------------------------------
    # Core financial ratios
    # --------------------------------------------------------

    profit_margin = (
        (net_profit / total_revenue) * 100
        if total_revenue > 0
        else 0
    )

    expense_ratio = (
        (total_expenses / total_revenue) * 100
        if total_revenue > 0
        else 0
    )

    revenue_ratio = (
        total_revenue / total_expenses
        if total_expenses > 0
        else 0
    )

    # --------------------------------------------------------
    # Monthly financial performance
    # --------------------------------------------------------

    working_df["Month"] = (
        working_df["Date"]
        .dt.to_period("M")
    )

    monthly_revenue = (
        income.assign(
            Month=income["Date"].dt.to_period("M")
        )
        .groupby("Month")["Amount"]
        .sum()
    )

    monthly_expenses = (
        expenses.assign(
            Month=expenses["Date"].dt.to_period("M")
        )
        .groupby("Month")["Amount"]
        .sum()
    )

    monthly = pd.concat(
        [
            monthly_revenue.rename("revenue"),
            monthly_expenses.rename("expenses"),
        ],
        axis=1,
    ).fillna(0)

    monthly = monthly.sort_index()

    monthly["profit"] = (
        monthly["revenue"]
        - monthly["expenses"]
    )

    monthly_revenue_values = (
        monthly["revenue"]
        .tolist()
    )

    monthly_expense_values = (
        monthly["expenses"]
        .tolist()
    )

    monthly_profit_values = (
        monthly["profit"]
        .tolist()
    )

    # --------------------------------------------------------
    # Expense analysis
    # --------------------------------------------------------

    expense_by_category = (
        expenses
        .groupby("Category")["Amount"]
        .sum()
        .sort_values(ascending=False)
    )

    largest_expense_category = (
        expense_by_category.idxmax()
        if not expense_by_category.empty
        else "N/A"
    )

    largest_expense_amount = (
        float(expense_by_category.max())
        if not expense_by_category.empty
        else 0
    )

    # --------------------------------------------------------
    # Trends
    # --------------------------------------------------------

    trends = calculate_trends(
        working_df,
        "transaction",
    )

    # --------------------------------------------------------
    # Return metrics
    # --------------------------------------------------------

    return {
        "dataset_type": "transaction",

        # Financial performance
        "total_revenue": total_revenue,
        "total_expenses": total_expenses,
        "net_profit": net_profit,
        "profit_margin": profit_margin,
        "expense_ratio": expense_ratio,
        "revenue_ratio": revenue_ratio,

        # Transaction activity
        "transaction_count": len(working_df),
        "records_processed": len(working_df),
        "income_transactions": len(income),
        "expense_transactions": len(expenses),

        "average_transaction": (
            float(working_df["Amount"].mean())
            if not working_df.empty
            else 0
        ),

        "largest_transaction": (
            float(working_df["Amount"].max())
            if not working_df.empty
            else 0
        ),

        "smallest_transaction": (
            float(working_df["Amount"].min())
            if not working_df.empty
            else 0
        ),

        # Monthly performance
        "monthly_revenue": monthly_revenue_values,
        "monthly_expenses": monthly_expense_values,
        "monthly_profit": monthly_profit_values,

        # Expense analysis
        "expense_by_category": expense_by_category,

        "largest_expense_category": (
            largest_expense_category
        ),

        "largest_expense_amount": (
            largest_expense_amount
        ),

        # Waterfall
        "waterfall_revenue": total_revenue,
        "waterfall_expenses": -total_expenses,
        "waterfall_profit": net_profit,

        # Trend analysis
        "trends": trends,
    }


# ============================================================
# BUSINESS FINANCIAL METRICS
# ============================================================


def calculate_business_metrics(
    df: pd.DataFrame,
) -> dict:
    """
    Calculate metrics from the business financial dataset.

    Expected columns include:
        record_id
        sector
        employees
        month
        revenue_usd
        opex_usd
        accounts_receivable_days
        inventory_days
        loan_balance_usd
        owner_injections_usd
        cashflow_stress_next_month
    """

    print(
        f"Processing {len(df):,} business records"
    )

    working_df = df.copy()

    # --------------------------------------------------------
    # Normalize numeric fields
    # --------------------------------------------------------

    numeric_columns = [
        "employees",
        "revenue_usd",
        "opex_usd",
        "accounts_receivable_days",
        "inventory_days",
        "loan_balance_usd",
        "owner_injections_usd",
        "cashflow_stress_next_month",
    ]

    for column in numeric_columns:

        if column in working_df.columns:
            working_df[column] = pd.to_numeric(
                working_df[column],
                errors="coerce",
            )

    # --------------------------------------------------------
    # Normalize month
    # --------------------------------------------------------

    if "month" in working_df.columns:

        working_df["month"] = pd.to_datetime(
            working_df["month"],
            errors="coerce",
        ).dt.to_period("M")

    # --------------------------------------------------------
    # Core financial metrics
    # --------------------------------------------------------

    total_revenue = float(
        working_df["revenue_usd"].sum()
    )

    total_expenses = float(
        working_df["opex_usd"].sum()
    )

    net_profit = (
        total_revenue
        - total_expenses
    )

    profit_margin = (
        (net_profit / total_revenue) * 100
        if total_revenue > 0
        else 0
    )

    expense_ratio = (
        (total_expenses / total_revenue) * 100
        if total_revenue > 0
        else 0
    )

    revenue_ratio = (
        total_revenue / total_expenses
        if total_expenses > 0
        else 0
    )

    # --------------------------------------------------------
    # Operational averages
    # --------------------------------------------------------

    average_employees = (
        float(
            working_df["employees"].mean()
        )
        if "employees" in working_df.columns
        else 0
    )

    average_ar_days = (
        float(
            working_df[
                "accounts_receivable_days"
            ].mean()
        )
        if "accounts_receivable_days" in working_df.columns
        else 0
    )

    average_inventory_days = (
        float(
            working_df[
                "inventory_days"
            ].mean()
        )
        if "inventory_days" in working_df.columns
        else 0
    )

    average_loan_balance = (
        float(
            working_df[
                "loan_balance_usd"
            ].mean()
        )
        if "loan_balance_usd" in working_df.columns
        else 0
    )

    average_owner_injections = (
        float(
            working_df[
                "owner_injections_usd"
            ].mean()
        )
        if "owner_injections_usd" in working_df.columns
        else 0
    )

    average_cashflow_stress = (
        float(
            working_df[
                "cashflow_stress_next_month"
            ].mean()
        )
        if "cashflow_stress_next_month"
        in working_df.columns
        else 0
    )

    # --------------------------------------------------------
    # Monthly revenue
    # --------------------------------------------------------

    if "month" in working_df.columns:

        monthly_revenue_series = (
            working_df
            .groupby("month")["revenue_usd"]
            .sum()
            .sort_index()
        )

        monthly_revenue = (
            monthly_revenue_series
            .tolist()
        )

    else:

        monthly_revenue = []

    # --------------------------------------------------------
    # Sector expense analysis
    # --------------------------------------------------------

    if "sector" in working_df.columns:

        expense_by_sector = (
            working_df
            .groupby("sector")["opex_usd"]
            .sum()
            .sort_values(ascending=False)
        )

    else:

        expense_by_sector = pd.Series(
            dtype="float64"
        )

    largest_expense_sector = (
        expense_by_sector.idxmax()
        if not expense_by_sector.empty
        else "N/A"
    )

    largest_expense_sector_amount = (
        float(expense_by_sector.max())
        if not expense_by_sector.empty
        else 0
    )

    # --------------------------------------------------------
    # Trends
    # --------------------------------------------------------

    trends = calculate_trends(
        working_df,
        "business",
    )

    # --------------------------------------------------------
    # Return metrics
    # --------------------------------------------------------

    return {
        "dataset_type": "business",

        # Financial performance
        "total_revenue": total_revenue,
        "total_expenses": total_expenses,
        "net_profit": net_profit,
        "profit_margin": profit_margin,
        "expense_ratio": expense_ratio,
        "revenue_ratio": revenue_ratio,

        # Operational metrics
        "transaction_count": len(working_df),
        "records_processed": len(working_df),

        "employees": average_employees,

        "accounts_receivable_days": (
            average_ar_days
        ),

        "inventory_days": (
            average_inventory_days
        ),

        "loan_balance": (
            average_loan_balance
        ),

        "owner_injections": (
            average_owner_injections
        ),

        # Cash-flow risk
        "cashflow_stress": (
            average_cashflow_stress
        ),

        "cashflow_stress_rate": (
            average_cashflow_stress
        ),

        # Monthly analysis
        "monthly_revenue": monthly_revenue,

        # Sector analysis
        "expense_by_sector": (
            expense_by_sector
        ),

        # Backward compatibility with
        # existing dashboard components.
        "expense_by_category": (
            expense_by_sector
        ),

        "largest_expense_category": (
            largest_expense_sector
        ),

        "largest_expense_amount": (
            largest_expense_sector_amount
        ),

        # Waterfall
        "waterfall_revenue": (
            total_revenue
        ),

        "waterfall_expenses": (
            -total_expenses
        ),

        "waterfall_profit": (
            net_profit
        ),

        # Trends
        "trends": trends,
    }

