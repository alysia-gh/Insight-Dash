from core.loader import load_data
from core.validator import validate_data
from core.metrics import calculate_metrics
from core.exporter import export_to_excel

from Insights.health import calculate_health_score
from Insights.analyzer import generate_insights
from Insights.executive_summary import generate_executive_summary
from core.forecast import calculate_forecast

def main():

    # Load uploaded dataset
    df = load_data("sample_data/small_business_cashflow.csv")

    # Detect and validate dataset type
    dataset_type = validate_data(df)

    print(f"Detected dataset: {dataset_type}")

    # Automatically calculate correct metrics
    
    results = calculate_metrics(df, dataset_type)

    results["forecast"] = calculate_forecast(
        df,
     dataset_type
    )

    print(results["forecast"])

    print(results.keys())

    print("\nCalculating health score...")

    health = calculate_health_score(results)

    results["health_score"] = health["score"]
    results["health_status"] = health["status"]
    results["health_breakdown"] = health["breakdown"]

    print("\nGenerating insights...")

    results["insights"] = generate_insights(results)

    results["executive_summary"] = generate_executive_summary(results)

    print("\nExporting results...")

    export_to_excel(results, df)

    print("\nDone!")


if __name__ == "__main__":
    main()