DATASET_HANDLERS = {
    "transaction": {
        "validator": validate_transaction,
        "analyzer": analyze_transactions,
        "dashboard": transaction_dashboard,
    },
    "business": {
        "validator": validate_business,
        "analyzer": analyze_business,
        "dashboard": business_dashboard,
    },
}