import os
import pandas as pd
from core.loader import load_data
from core.validator import validate_data
from core.metrics import calculate_metrics
from core.exporter import export_to_excel

from Insights.health import calculate_health_score
from Insights.analyzer import generate_insights
from Insights.executive_summary import generate_executive_summary
from core.forecast import calculate_forecast


def main():

 Input_folder = "input_data"
    Output_folder = "generated_reports"
    os.makedirs(Input_folder, exist_ok=True)
    os.makedirs(Output_folder, exist_ok=True)

    files = [f for f in os.listdir(Input_folder) if f.endswith(".csv")]
    if not files:
        print("No CSV files found in input folder. Please drop a CSV file into the folder.")
        return
    input_path = os.path.join(Input_folder, files[0])


    # Load uploaded dataset
    df = pd.read_csv(input_path)

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

    output_filename = f"Executive_Report_{files[0].replace('.csv','.xlsx')}"
    output_path = os.path.join(Output_folder, output_filename)
    export_to_excel(results, df, output_path)

    print(f"\nDone! Your report is waiting in: {output_path}")

    print(f"Report generated successfully: {output_path}")

if __name__ == "__main__":
    main()