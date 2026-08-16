from openpyxl.chart import BarChart, Reference
from openpyxl.chart.label import DataLabelList
from openpyxl.styles import Font, PatternFill


def create_profit_waterfall_chart(data_ws, results, chart_ws=None, chart_cell="E18"):

    # ---------------------------------
    # Chart Data
    # ---------------------------------

    start_row = 50

    data_ws[f"H{start_row}"] = "Category"
    data_ws[f"I{start_row}"] = "Base"
    data_ws[f"J{start_row}"] = "Value"


    revenue = results["total_revenue"]
    expenses = results["waterfall_expenses"]
    profit = results["waterfall_profit"]


    data = [
        ("Revenue", 0, revenue),

        # Expenses start at revenue level
        ("Expenses", profit, expenses),

        # Profit starts at zero
        ("Net Profit", 0, profit),
    ]


    for index, row in enumerate(data, start=start_row + 1):

        data_ws[f"H{index}"] = row[0]
        data_ws[f"I{index}"] = row[1]
        data_ws[f"J{index}"] = row[2]

        data_ws[f"J{index}"].number_format = "$#,##0"


    # Header styling

    for cell in ["H50", "I50", "J50"]:
        data_ws[cell].font = Font(bold=True)


    # ---------------------------------
    # Create stacked column chart
    # ---------------------------------

    chart = BarChart()

    chart.type = "col"

    chart.grouping = "stacked"

    chart.overlap = 100


    chart.title = "Revenue to Net Profit"

    chart.y_axis.title = "USD"


    base = Reference(
        data_ws,
        min_col=9,
        min_row=start_row,
        max_row=start_row + len(data)
    )


    values = Reference(
        data_ws,
        min_col=10,
        min_row=start_row,
        max_row=start_row + len(data)
    )


    categories = Reference(
        data_ws,
        min_col=8,
        min_row=start_row + 1,
        max_row=start_row + len(data)
    )


    chart.add_data(
        base,
        titles_from_data=True
    )

    chart.add_data(
        values,
        titles_from_data=True
    )


    chart.set_categories(categories)


    # Hide the base series

    chart.series[0].graphicalProperties.noFill = True


    # Add values

    chart.dataLabels = DataLabelList()
    chart.dataLabels.showVal = True


    chart.legend = None

    chart.height = 9
    chart.width = 15

    target_ws = chart_ws if chart_ws is not None else data_ws
    target_ws.add_chart(
        chart,
        chart_cell
    )


    return data_ws