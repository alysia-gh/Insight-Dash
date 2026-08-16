def normalize_financial_data(df):

    column_map = {
        "transaction_date": "Date",
        "merchant": "Description",
        "category": "Category",
        "amount": "Amount",
        "transaction_type": "Type"
    }

    df = df.rename(columns=column_map)

    df["Date"] = pd.to_datetime(df["Date"])

    return df

COLUMN_ALIASES = {
    "transaction date": "Date",
    "posted date": "Date",
    "memo": "Description",
    "vendor": "Description",
    "revenue": "revenue_usd",
    "monthly revenue": "revenue_usd",
    "operating expense": "opex_usd",
    "staff": "employees",
}