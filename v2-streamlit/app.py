from pathlib import Path
import sys

import pandas as pd
import streamlit as st

PROJECT_ROOT = Path(**file**).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
sys.path.insert(0, str(PROJECT_ROOT))

from core.validator import validate_data
from core.metrics import calculate_metrics
from core.forecast import calculate_forecast
from core.exporter import export_to_excel

from Insights.health import calculate_health_score
from Insights.analyzer import generate_insights
from Insights.executive_summary import generate_executive_summary

# =========================================================

# PAGE CONFIGURATION

# =========================================================

st.set_page_config(
page_title="Insight-Dash",
page_icon=None,
layout="wide",
)

# =========================================================

# HEALTH SCORE STYLE

# =========================================================

def get_health_style(score):
if score >= 75:
return "green"

```
if score >= 60:
    return "orange"

return "red"
```

# =========================================================

# EXECUTIVE OVERVIEW

# =========================================================

def render_overview(results):

```
st.header("Executive Overview")

st.caption(
    "Your business at a glance."
)

# -----------------------------------------------------
# KPI CARDS
# -----------------------------------------------------

metric_cols = st.columns(4)

metric_cols[0].metric(
    "Revenue",
    f"${results.get('total_revenue', 0):,.2f}",
)

metric_cols[1].metric(
    "Expenses",
    f"${results.get('total_expenses', 0):,.2f}",
)

metric_cols[2].metric(
    "Net Profit",
    f"${results.get('net_profit', 0):,.2f}",
)

metric_cols[3].metric(
    "Business Health Score",
    f"{results.get('health_score', 0)}/100",
)

# -----------------------------------------------------
# HEALTH STATUS
# -----------------------------------------------------

health_score = float(
    results.get(
        "health_score",
        0,
    )
)

health_status = results.get(
    "health_status",
    "Unknown",
)

health_color = get_health_style(
    health_score
)

st.markdown("---")

st.subheader(
    "Health Status"
)

col1, col2 = st.columns(
    [2, 1]
)

with col1:

    st.markdown(
        f"""
        <div style="
            padding: 0.75rem 1rem;
            border-radius: 0.5rem;
            background: #F8FAFC;
            border: 1px solid #E2E8F0;
        ">
            <strong>Score:</strong>
            <span style="
                color: {health_color};
                font-size: 1.6rem;
                font-weight: 700;
            ">
                {health_score:.0f}/100
            </span>
            <br>
            <strong>Status:</strong>
            <span style="color: {health_color};">
                {health_status}
            </span>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col2:

    st.markdown(
        f"""
        <div style="
            padding: 0.75rem 1rem;
            border-radius: 0.5rem;
            background: #F8FAFC;
            border: 1px solid #E2E8F0;
        ">
            <strong>Assessment</strong><br>
            <span style="color: {health_color};">
                {health_status}
            </span>
        </div>
        """,
        unsafe_allow_html=True,
    )

# -----------------------------------------------------
# EXECUTIVE SUMMARY
# -----------------------------------------------------

st.markdown("---")

st.subheader(
    "Executive Summary"
)

summary = results.get(
    "executive_summary",
    "No executive summary available.",
)

st.info(
    summary
)

# -----------------------------------------------------
# FINANCIAL PERFORMANCE
# -----------------------------------------------------

st.markdown("---")

st.subheader(
    "Financial Performance"
)

expense_by_category = results.get(
    "expense_by_category"
)

if (
    isinstance(
        expense_by_category,
        pd.Series,
    )
    and not expense_by_category.empty
):

    chart_df = (
        expense_by_category
        .reset_index()
    )

    chart_df.columns = [
        "Category",
        "Amount",
    ]

    st.bar_chart(
        chart_df.set_index(
            "Category"
        )
    )

else:

    st.write(
        "Financial performance detail "
        "is not available for the uploaded dataset."
    )
```

# =========================================================

# FORECAST VIEW

# =========================================================

def render_forecast(results):

```
st.header(
    "Statistical Forecast Analytics"
)

forecast = results.get(
    "forecast",
    {},
)

if not forecast:

    st.info(
        "No forecast data is available "
        "for this dataset."
    )

    return

# -----------------------------------------------------
# FORECAST SUMMARY
# -----------------------------------------------------

st.caption(
    f"{forecast.get('period', 'Next Month')} "
    f"financial forecast based on "
    f"{forecast.get('months_used', 0)} "
    f"historical month(s)."
)

forecast_cols = st.columns(4)

forecast_cols[0].metric(
    "Forecast Revenue",
    f"${forecast.get('revenue', 0):,.2f}",
)

forecast_cols[1].metric(
    "Forecast Expenses",
    f"${forecast.get('expenses', 0):,.2f}",
)

forecast_cols[2].metric(
    "Forecast Profit",
    f"${forecast.get('profit', 0):,.2f}",
)

forecast_cols[3].metric(
    "Forecast Margin",
    f"{forecast.get('margin', 0):.1f}%",
)

# -----------------------------------------------------
# FORECAST DATA QUALITY
# -----------------------------------------------------

st.markdown("---")

st.subheader(
    "Forecast Data Quality"
)

st.write(
    f"**History used:** "
    f"{forecast.get('months_used', 0)} months"
)

st.write(
    f"**Forecast horizon:** "
    f"{forecast.get('months_forecast', 1)} month(s)"
)

quality = forecast.get(
    "forecast_quality",
    "Unknown",
)

st.write(
    f"**Data quality:** {quality}"
)

if quality == "Insufficient Data":

    st.warning(
        "Limited historical data is available. "
        "The forecast should be treated as a directional "
        "estimate rather than a reliable prediction."
    )

elif quality == "Limited History":

    st.info(
        "The forecast is based on a limited amount "
        "of historical data. Additional months of data "
        "may improve the reliability of the trend."
    )

elif quality == "Moderate History":

    st.info(
        "The forecast is based on a moderate amount "
        "of historical data and should be interpreted "
        "as a directional planning estimate."
    )

# -----------------------------------------------------
# HISTORICAL PERIOD
# -----------------------------------------------------

historical_start = forecast.get(
    "historical_start"
)

historical_end = forecast.get(
    "historical_end"
)

if historical_start and historical_end:

    st.write(
        f"**Historical period:** "
        f"{historical_start} to {historical_end}"
    )

# -----------------------------------------------------
# FORECAST METHOD
# -----------------------------------------------------

st.markdown("---")

st.subheader(
    "Forecast Method"
)

st.write(
    "Insight Dash uses a transparent linear trend model "
    "based on historical monthly revenue, expenses, and "
    "profit. The forecast is intended to provide "
    "directional planning insight rather than a guaranteed "
    "financial prediction."
)
```

# =========================================================

# HEALTH & INSIGHTS

# =========================================================

def render_health_insights(results):

```
st.header(
    "Business Health & Insights"
)

# -----------------------------------------------------
# HEALTH SCORE
# -----------------------------------------------------

health_score = results.get(
    "health_score",
    0,
)

health_status = results.get(
    "health_status",
    "Unknown",
)

health_col1, health_col2 = st.columns(2)

health_col1.metric(
    "Business Health Score",
    f"{health_score}/100",
)

health_col2.metric(
    "Status",
    health_status,
)

# -----------------------------------------------------
# HEALTH BREAKDOWN
# -----------------------------------------------------

st.markdown("---")

st.subheader(
    "Health Breakdown"
)

breakdown = results.get(
    "health_breakdown",
    {},
)

if breakdown:

    breakdown_df = pd.DataFrame(
        {
            "Category": list(
                breakdown.keys()
            ),
            "Score": list(
                breakdown.values()
            ),
        }
    )

    st.dataframe(
        breakdown_df,
        hide_index=True,
        use_container_width=True,
    )

else:

    st.info(
        "No health breakdown is available."
    )

# -----------------------------------------------------
# INSIGHTS
# -----------------------------------------------------

st.markdown("---")

st.subheader(
    "Key Business Insights"
)

insights = results.get(
    "insights",
    [],
)

if isinstance(
    insights,
    list,
) and insights:

    for insight in insights:

        if not isinstance(
            insight,
            dict,
        ):
            continue

        insight_type = str(
            insight.get(
                "type",
                "info",
            )
        ).lower()

        title = insight.get(
            "title",
            "Business Insight",
        )

        message = insight.get(
            "message",
            "",
        )

        recommendation = insight.get(
            "recommendation"
        )

        if insight_type == "warning":

            st.warning(
                f"**{title}**\n\n{message}"
            )

        elif insight_type == "success":

            st.success(
                f"**{title}**\n\n{message}"
            )

        else:

            st.info(
                f"**{title}**\n\n{message}"
            )

        if recommendation:

            st.caption(
                f"Recommendation: "
                f"{recommendation}"
            )

else:

    st.info(
        "No additional insights were generated."
    )
```

# =========================================================

# RAW DATA

# =========================================================

def render_raw_data(df):

```
st.header(
    "Uploaded Dataset Preview"
)

st.dataframe(
    df.head(20),
    use_container_width=True,
)

st.caption(
    f"Showing the first 20 rows of "
    f"{len(df):,} analyzed records."
)
```

# =========================================================

# EXCEL EXPORT

# =========================================================

def render_excel_download(
results,
df,
base_dir,
):

```
st.markdown("---")

st.subheader(
    "Download Executive Deliverable"
)

try:

    output_file = export_to_excel(
        results,
        df,
        str(
            base_dir
            / "Polished_Executive_Report.xlsx"
        ),
    )

    with open(
        output_file,
        "rb",
    ) as f:

        excel_bytes = f.read()

    st.download_button(
        label=(
            "Download Polished Excel Dashboard"
        ),
        data=excel_bytes,
        file_name=(
            "Polished_Executive_Report.xlsx"
        ),
        mime=(
            "application/vnd.openxmlformats-officedocument."
            "spreadsheetml.sheet"
        ),
    )

    st.success(
        f"Report saved to: {output_file}"
    )

except Exception as exc:

    st.error(
        f"Failed to create report: {exc}"
    )
```

# =========================================================

# MAIN APPLICATION

# =========================================================

def main():

```
st.title(
    "Insight Dash"
)

st.subheader(
    "Executive Financial Intelligence"
)

st.write(
    "Insight Dash transforms business financial data "
    "into actionable insights, forecasts, health scoring, "
    "and an executive Excel report for smarter "
    "decision-making."
)

# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:

    st.header(
        "Report Settings"
    )

    company_name = st.text_input(
        "Company Name",
        value="",
    )

    currency = st.selectbox(
        "Currency",
        [
            "USD",
            "EUR",
            "GBP",
        ],
        index=0,
    )

    forecast_period = st.selectbox(
        "Forecast Period",
        [
            "Next Month",
            "Next Quarter",
            "Next 6 Months",
            "Next Year",
        ],
        index=0,
    )

    st.markdown("---")

    st.caption(
        "Optional report content"
    )

    include_summary = st.checkbox(
        "Executive summary",
        value=True,
    )

    include_forecast = st.checkbox(
        "Forecast view",
        value=True,
    )

    include_health = st.checkbox(
        "Health score",
        value=True,
    )

    include_raw_data = st.checkbox(
        "Raw data preview",
        value=True,
    )

# =====================================================
# FILE UPLOAD
# =====================================================

st.markdown("---")

st.subheader(
    "Upload Business Data"
)

st.write(
    "Upload a CSV file containing your small business "
    "financial data. CSV is supported for this version."
)

uploaded_file = st.file_uploader(
    "Choose a CSV file",
    type=["csv"],
    help=(
        "CSV is supported for this version. "
        "Select a valid transaction or business dataset "
        "before running the analysis."
    ),
)

base_dir = PROJECT_ROOT

if uploaded_file is not None:

    st.info(
        f"Selected file: {uploaded_file.name}"
    )

analyze_button = st.button(
    "Analyze Business",
    type="primary",
    disabled=uploaded_file is None,
)

# =====================================================
# ANALYSIS PIPELINE
# =====================================================

if (
    analyze_button
    and uploaded_file is not None
):

    try:

        df = pd.read_csv(
            uploaded_file
        )

        with st.status(
            "Preparing analysis...",
            expanded=True,
        ) as status:

            progress = st.progress(0)

            # -------------------------------------------------
            # VALIDATE
            # -------------------------------------------------

            dataset_type = validate_data(
                df
            )

            progress.progress(20)

            st.info(
                f"Detected dataset type: "
                f"{dataset_type}"
            )

            # -------------------------------------------------
            # METRICS
            # -------------------------------------------------

            results = calculate_metrics(
                df,
                dataset_type,
            )

            progress.progress(40)

            # -------------------------------------------------
            # FORECAST
            # -------------------------------------------------

            results["forecast"] = (
                calculate_forecast(
                    df,
                    dataset_type,
                    forecast_period,
                )
            )

            progress.progress(55)

            # -------------------------------------------------
            # HEALTH SCORE
            # -------------------------------------------------

            health = calculate_health_score(
                results
            )

            results["health_score"] = (
                health["score"]
            )

            results["health_status"] = (
                health["status"]
            )

            results["health_breakdown"] = (
                health["breakdown"]
            )

            progress.progress(65)

            # -------------------------------------------------
            # INSIGHTS
            # -------------------------------------------------

            results["insights"] = (
                generate_insights(
                    results
                )
            )

            progress.progress(75)

            # -------------------------------------------------
            # EXECUTIVE SUMMARY
            # -------------------------------------------------

            results["executive_summary"] = (
                generate_executive_summary(
                    results
                )
            )

            progress.progress(90)

            st.success(
                f"Analysis complete for "
                f"{uploaded_file.name}."
            )

            st.write(
                f"Detected dataset type: "
                f"{dataset_type}"
            )

            st.write(
                f"Records analyzed: "
                f"{len(df):,}"
            )

            progress.progress(100)

            status.update(
                label="Analysis complete.",
                state="complete",
            )

        # =================================================
        # SAVE RESULTS
        # =================================================

        st.session_state[
            "analysis_results"
        ] = results

        st.session_state[
            "analysis_df"
        ] = df

    except pd.errors.EmptyDataError:

        st.error(
            "The uploaded CSV is empty. "
            "Please upload a CSV containing "
            "business data."
        )

        return

    except pd.errors.ParserError:

        st.error(
            "The uploaded CSV could not be read. "
            "Please check that the file is a valid CSV."
        )

        return

    except ValueError as exc:

        st.error(
            "Your CSV could not be validated. "
            "Please check the file format and required "
            f"columns before running the analysis. Details: {exc}"
        )

        return

    except Exception as exc:

        st.error(
            "Insight Dash encountered an unexpected "
            f"error while processing the file: {exc}"
        )

        return

# =====================================================
# DISPLAY STORED RESULTS
# =====================================================

if (
    "analysis_results"
    not in st.session_state
    or "analysis_df"
    not in st.session_state
):

    st.info(
        "Upload a CSV file to generate an executive "
        "business overview, health score, forecasts, "
        "and an Excel report."
    )

    return

results = st.session_state[
    "analysis_results"
]

df = st.session_state[
    "analysis_df"
]

# =====================================================
# RESULTS TABS
# =====================================================

tab_names = []

if include_summary:
    tab_names.append(
        "Executive Overview"
    )

if include_forecast:
    tab_names.append(
        "Forecast View"
    )

if include_health:
    tab_names.append(
        "Health & Insights"
    )

if include_raw_data:
    tab_names.append(
        "Raw Data Preview"
    )

if not tab_names:

    tab_names = [
        "Executive Overview"
    ]

result_tabs = st.tabs(
    tab_names
)

tab_index = 0

# =====================================================
# EXECUTIVE OVERVIEW
# =====================================================

if include_summary:

    with result_tabs[tab_index]:

        render_overview(
            results
        )

    tab_index += 1

# =====================================================
# FORECAST
# =====================================================

if include_forecast:

    with result_tabs[tab_index]:

        render_forecast(
            results
        )

    tab_index += 1

# =====================================================
# HEALTH & INSIGHTS
# =====================================================

if include_health:

    with result_tabs[tab_index]:

        render_health_insights(
            results
        )

    tab_index += 1

# =====================================================
# RAW DATA
# =====================================================

if include_raw_data:

    with result_tabs[tab_index]:

        render_raw_data(
            df
        )

# =====================================================
# EXCEL EXPORT
# =====================================================

render_excel_download(
    results,
    df,
    base_dir,
)
```

# =========================================================

# RUN APPLICATION

# =========================================================

if **name** == "**main**":
main()
