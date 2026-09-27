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

BUSINESS_NUMERIC_COLUMNS = [
    "employees",
    "revenue_usd",
    "opex_usd",
    "accounts_receivable_days",
    "inventory_days",
    "loan_balance_usd",
    "owner_injections_usd",
    "cashflow_stress_next_month"
]


def _row_numbers_with_blank_values(df, columns):
    rows = []
    for column in columns:
        if column not in df.columns:
            continue
        series = df[column]
        mask = series.isna() | series.astype(str).str.strip().eq("")
        rows.extend(series.index[mask].tolist())
    return sorted(set(rows))


def _describe_bad_rows(indices, limit=10):
    if not indices:
        return ""
    preview = sorted(set(indices))[:limit]
    suffix = "" if len(preview) <= limit else ", ..."
    return f" Rows: {preview}{suffix}."


def _validate_dataframe_structure(df):
    if df is None:
        raise ValueError("Input data is missing. Please upload a CSV or DataFrame with rows.")

    if not isinstance(df, pd.DataFrame):
        raise ValueError("Input data must be a pandas DataFrame.")

    if df.empty:
        raise ValueError("Dataset is empty. Please upload a CSV with at least one row of data.")

    column_names = list(df.columns)
    blank_columns = [
        i for i, name in enumerate(column_names)
        if name is None or (isinstance(name, str) and not name.strip())
    ]
    if blank_columns:
        raise ValueError(
            "Dataset contains blank column names at positions "
            f"{blank_columns}. Please rename the columns before uploading."
        )

    seen = {}
    duplicate_columns = []
    for idx, name in enumerate(column_names):
        if name in seen:
            duplicate_columns.append(name)
        else:
            seen[name] = idx
    if duplicate_columns:
        dup_list = sorted(set(duplicate_columns))
        raise ValueError(
            "Dataset contains duplicate column names: "
            f"{dup_list}. Please remove duplicate headers before processing."
        )

    blank_rows = df.index[
        df.apply(
            lambda row: (row.isna() | row.astype(str).str.strip().eq(""))
            .all(),
            axis=1,
        )
    ]
    if not blank_rows.empty:
        bad_rows = sorted(blank_rows.tolist())[:10]
        raise ValueError(
            "Dataset contains completely blank rows. "
            f"Remove the blank row(s) at index {bad_rows}."
        )


def detect_dataset_type(df):
    cols = set(df.columns)

    if TRANSACTION_COLUMNS.issubset(cols):
        return "transaction"

    if BUSINESS_COLUMNS.issubset(cols):
        return "business"

    return "unknown"


def validate_transaction(df):
    _validate_dataframe_structure(df)

    missing = TRANSACTION_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(
            "Missing required transaction columns: "
            f"{sorted(missing)}. Expected columns are: Date, Description, Category, Amount, Type."
        )

    missing_value_rows = _row_numbers_with_blank_values(df, [
        "Date",
        "Description",
        "Category",
        "Amount",
        "Type"
    ])
    if missing_value_rows:
        raise ValueError(
            "Missing required values in transaction data"
            f"{_describe_bad_rows(missing_value_rows)}"
        )

    date_series = pd.to_datetime(df["Date"], errors="coerce")
    invalid_date_rows = sorted(df.index[date_series.isna()].tolist())
    if invalid_date_rows:
        raise ValueError(
            "Transaction Date values are invalid or blank. "
            f"Please use a valid date format in row(s): {invalid_date_rows[:10]}."
        )

    amount_series = pd.to_numeric(df["Amount"], errors="coerce")
    invalid_amount_rows = sorted(df.index[amount_series.isna()].tolist())
    if invalid_amount_rows:
        raise ValueError(
            "Transaction Amount values must be numeric. "
            f"Please fix row(s): {invalid_amount_rows[:10]}."
        )

    valid_types = {"Income", "Expense"}
    normalized_types = df["Type"].astype(str).str.strip().str.title()
    invalid_type_rows = sorted(df.index[~normalized_types.isin(valid_types)].tolist())
    if invalid_type_rows:
        raise ValueError(
            "Transaction Type values must be 'Income' or 'Expense' (case-insensitive). "
            f"Please fix row(s): {invalid_type_rows[:10]}."
        )

    duplicate_rows = df.duplicated(subset=["Date", "Description", "Category", "Amount", "Type"], keep=False)
    if duplicate_rows.any():
        rows = sorted(df.index[duplicate_rows].tolist())
        raise ValueError(
            "Duplicate transactions detected. "
            f"Exact duplicate rows were found at index {rows[:10]}. Please remove duplicates before continuing."
        )


def validate_business(df):
    _validate_dataframe_structure(df)

    missing = BUSINESS_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(
            "Missing required business columns: "
            f"{sorted(missing)}. Expected columns are: {sorted(BUSINESS_COLUMNS)}."
        )

    blank_value_rows = _row_numbers_with_blank_values(df, list(BUSINESS_COLUMNS))
    if blank_value_rows:
        raise ValueError(
            "Business data contains blank values in required fields"
            f"{_describe_bad_rows(blank_value_rows)}"
        )

    for column in BUSINESS_NUMERIC_COLUMNS:
        if column not in df.columns:
            continue
        converted = pd.to_numeric(df[column], errors="coerce")
        invalid_rows = sorted(df.index[converted.isna()].tolist())
        if invalid_rows:
            raise ValueError(
                f"Business column '{column}' must contain numeric values. "
                f"Please fix row(s): {invalid_rows[:10]}."
            )


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