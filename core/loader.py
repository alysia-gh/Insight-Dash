import os
import pandas as pd


def load_data(file_path: str) -> pd.DataFrame:
    """
    Load data from a CSV or Excel file into a pandas DataFrame.
    """

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file '{file_path}' does not exist.")

    file_extension = os.path.splitext(file_path)[1].lower()

    if file_extension == ".csv":
        df = pd.read_csv(file_path)

    elif file_extension in [".xlsx", ".xls"]:
        df = pd.read_excel(file_path, engine="openpyxl")

    else:
        raise ValueError(f"Unsupported file format: {file_extension}")

    return df