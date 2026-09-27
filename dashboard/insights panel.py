def create_insights_panel(ws, insights):
    row = 25

    for insight in insights:
        ws[f"A{row}"] = insight.get("title", "Insight")
        ws[f"B{row}"] = insight.get("message", "")
        row += 2

    return ws