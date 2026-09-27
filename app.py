from pathlib import Path

import pandas as pd
import streamlit as st

from core.validator import validate_data
from core.metrics import calculate_metrics
from core.forecast import calculate_forecast
from core.exporter import export_to_excel
from Insights.health import calculate_health_score
from Insights.analyzer import generate_insights
from Insights.executive_summary import generate_executive_summary


st.set_page_config(
    page_title="Insight-Dash",
    page_icon=None,
    layout="wide",
)


def main():
    st.title("Insight Dash")
    st.subheader("Executive Financial Intelligence")
    st.write(
        "Insight Dash transforms business financial data into actionable insights, forecasts, health scoring, and an executive Excel report for smarter decision-making."
    )

    with st.sidebar:
        st.header("Report Settings")
        company_name = st.text_input("Company Name", value="")
        currency = st.selectbox("Currency", ["USD", "EUR", "GBP"], index=0)
        forecast_period = st.selectbox("Forecast Period", ["Next Month", "Next Quarter", "Next 6 Months", "Next Year"], index=0)

        st.markdown("---")
        st.caption("Optional report content")
        include_summary = st.checkbox("Executive summary", value=True)
        include_forecast = st.checkbox("Forecast view", value=True)
        include_health = st.checkbox("Health score", value=True)
        include_raw_data = st.checkbox("Raw data preview", value=True)

    st.markdown("---")
    st.subheader("Upload Business Data")
    st.write("Upload a CSV file containing your small business financial data. CSV is supported for this version.")

    uploaded_file = st.file_uploader(
        "Choose a CSV file",
        type=["csv"],
        help="CSV is supported for this version. Select a valid transaction or business dataset before running the analysis.",
    )
    base_dir = Path(__file__).resolve().parent

    if uploaded_file is not None:
        st.info(f"Selected file: {uploaded_file.name}")

    analyze_button = st.button("Analyze Business", type="primary", disabled=uploaded_file is None)

    if analyze_button and uploaded_file is not None:
        df = pd.read_csv(uploaded_file)

        try:
            with st.status("Preparing analysis...", expanded=True) as status:
                progress = st.progress(0)
                progress.progress(10)

                dataset_type = validate_data(df)
                progress.progress(30)
                st.info(f"Detected dataset type: {dataset_type}")

                results = calculate_metrics(df, dataset_type)
                progress.progress(55)
                results["forecast"] = calculate_forecast(
                    df, 
                    dataset_type,
                    forecast_period,
                )

                health = calculate_health_score(results)
                results["health_score"] = health["score"]
                results["health_status"] = health["status"]
                results["health_breakdown"] = health["breakdown"]

                results["insights"] = generate_insights(results)
                results["executive_summary"] = generate_executive_summary(results)
                progress.progress(85)

                st.success(f"Analysis complete for {uploaded_file.name}.")
                st.write(f"Detected dataset type: {dataset_type}")
                st.write(f"Records analyzed: {len(df):,}")

                status.update(label="Analysis complete.", state="complete")

            tab1, tab2, tab3 = st.tabs(["Executive Summary", "Forecast View", "Raw Data Preview"])

            with tab1:
                st.subheader("Executive Health Status")
                col1, col2 = st.columns(2)
                col1.metric("Business Health Score", f"{results['health_score']}/100")
                col2.metric("Status", results["health_status"])
                st.write("---")

            with tab2:
                st.subheader("Statistical Forecast Analytics")
                st.write(results["forecast"])

            with tab3:
                st.subheader("Uploaded Transformed Dataset View")
                st.dataframe(df.head(20))

            st.write("---")
            st.subheader("Download Executive Deliverable")

            try:
                output_file = export_to_excel(
                    results,
                    df,
                    str(base_dir / "Polished_Executive_Report.xlsx"),
                )

                with open(output_file, "rb") as f:
                    excel_bytes = f.read()

                st.download_button(
                    label="Download Polished Excel Dashboard",
                    data=excel_bytes,
                    file_name="Polished_Executive_Report.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                )
                st.success(f"Report saved to: {output_file}")
            except Exception as exc:
                st.error(f"Failed to create report: {exc}")

        except ValueError as exc:
            st.error(
                "Your CSV could not be validated. Please check the file format and required columns before running the analysis. "
                f"Details: {exc}"
            )


if __name__ == "__main__":
    main()