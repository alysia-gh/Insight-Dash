import pandas as pd

TRANSACTION_COLUMNS = {
    "Date",
    "Description",
    "Category",
    "Amount",
    "Type"
}

BUSINESS_COLUMNS = {
    "record_id",
    "sector",
    "employees",
    "month",
    "revenue_usd",
    "opex_usd",
    "accounts_receivable_days",
    "inventory_days",
    "loan_balance_usd",
    "owner_injections_usd",
    "cashflow_stress_next_month"
}


def detect_dataset_type(df):
    cols = set(df.columns)

    if TRANSACTION_COLUMNS.issubset(cols):
        return "transaction"

    if BUSINESS_COLUMNS.issubset(cols):
        return "business"

    return "unknown"


def validate_transaction(df):
    missing = TRANSACTION_COLUMNS - set(df.columns)

    if missing:
        raise ValueError(f"Missing columns: {list(missing)}")

    if not pd.api.types.is_numeric_dtype(df["Amount"]):
        raise ValueError("Amount column must be numeric.")

    valid_types = {"Income", "Expense"}

    if not df["Type"].isin(valid_types).all():
        raise ValueError("Type column must contain only 'Income' or 'Expense'.")


def validate_business(df):
    missing = BUSINESS_COLUMNS - set(df.columns)

    if missing:
        raise ValueError(f"Missing columns: {list(missing)}")


def validate_data(df):
    dataset_type = detect_dataset_type(df)

    if dataset_type == "transaction":
        validate_transaction(df)

    elif dataset_type == "business":
        validate_business(df)

    else:
        raise ValueError(
            "Unknown dataset format. Please upload either a transaction ledger or business metrics dataset."
        )

    return dataset_type