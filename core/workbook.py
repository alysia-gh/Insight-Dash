import os
from datetime import datetime
from openpyxl import Workbook


def create_workbook():
    """Create a new workbook without the default sheet."""
    workbook = Workbook()
    workbook.remove(workbook.active)
    return workbook


def generate_output_path():
    os.makedirs("reports", exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    return os.path.join(
        "reports",
        f"Insight_Dash_Report_{timestamp}.xlsx"
    )


def save_workbook(workbook):

    output_path = generate_output_path()

    workbook.save(output_path)

    return output_path
    workbook.active = 0