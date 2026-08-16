from openpyxl.styles import Font


def create_raw_data_sheet(workbook, df):

    ws = workbook.create_sheet("Raw Data")

    # Headers
    for col_num, column in enumerate(df.columns, start=1):

        cell = ws.cell(row=1, column=col_num)

        cell.value = column

        cell.font = Font(bold=True)

    # Data
    for row in df.itertuples(index=False):

        ws.append(row)

    return ws