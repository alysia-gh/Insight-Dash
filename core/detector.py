def detect_dataset_type(df):

    columns = set(df.columns)

    transaction_columns = {
        "Date",
        "Description",
        "Category",
        "Amount",
        "Type",
    }

    business_columns = {
        "sector",
        "revenue_usd",
        "opex_usd",
        "accounts_receivable_days",
        "inventory_days",
    }

    if transaction_columns.issubset(columns):
        return "transactions"

    if business_columns.issubset(columns):
        return "business"

    return "unknown"