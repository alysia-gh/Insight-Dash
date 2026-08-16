def format_currency(ws):

    for row in ws.iter_rows():

        for cell in row:

            if isinstance(
                cell.value,
                (int,float)
            ):

                cell.number_format = (
                    '$#,##0'
                )