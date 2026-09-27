from pathlib import Path
from typing import Optional

import pandas as pd

from core.workbook import create_workbook, save_workbook
from dashboard.dashboard import create_dashboard_sheet
from dashboard.rawdata import create_raw_data_sheet
from dashboard.insights import create_insights_sheet
from dashboard.metrics import create_metrics_sheet


def export_to_excel(
    results: dict,
    df: pd.DataFrame,
    output_path: Optional[str] = None
) -> str:
    """
    Build the existing custom workbook architecture and save it to disk.
    Returns the actual file path used for the generated Excel report.
    """
    project_root = Path(__file__).resolve().parents[1]

    if output_path is None:
        out_path = project_root / "Polished_Executive_Report.xlsx"
    else:
        out_path = Path(output_path)
        if not out_path.is_absolute():
            out_path = project_root / out_path

    if out_path.is_dir():
        out_path = out_path / "Polished_Executive_Report.xlsx"

    out_path = out_path.resolve()
    workbook = create_workbook()

    create_dashboard_sheet(workbook, results, len(df))
    create_metrics_sheet(workbook, results)
    create_raw_data_sheet(workbook, df)

    insights = results.get("insights", [])
    if isinstance(insights, list):
        create_insights_sheet(workbook, insights)

    saved_path = save_workbook(workbook, str(out_path))
    return str(saved_path)
