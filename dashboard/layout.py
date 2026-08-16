from openpyxl.utils import get_column_letter


def apply_layout(ws):

    widths = {

        "A":18,
        "B":4,
        "C":4,
        "D":18,
        "E":4,
        "F":4,
        "G":18,
        "H":18,

    }


    for col, width in widths.items():

        ws.column_dimensions[col].width = width


    for row in range(1,60):

        ws.row_dimensions[row].height = 22
    
    ws.freeze_panes = "A10"