from core.workbook import create_workbook, save_workbook
from dashboard.dashboard import create_dashboard_sheet
from dashboard.rawdata import create_raw_data_sheet
from dashboard.insights import create_insights_sheet
from dashboard.metrics import create_metrics_sheet


def export_to_excel(results, df):
    workbook = create_workbook()

    create_dashboard_sheet(workbook, results, len(df))
    create_metrics_sheet(workbook, results)
    create_raw_data_sheet(workbook, df)
    create_insights_sheet(workbook, results.get("insights", []))

    output_path = save_workbook(workbook)

    print("\n====================================")
    print(" Insight Dash Report Created")
    print("====================================")
    print(output_path)

    return output_path