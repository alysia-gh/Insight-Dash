def create_insights_panel(ws, insights):
row = 25

for insight in results["insights"]:

    ws[f"A{row}"] = insight["title"]

    ws[f"B{row}"] = insight["message"]

    row += 2