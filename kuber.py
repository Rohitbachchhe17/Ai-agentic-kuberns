# app.py

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# -----------------------------
# PAGE CONFIG
# -----------------------------

st.set_page_config(
    page_title="AI Agent EDA Dashboard",
    page_icon="🤖",
    layout="wide"
)

# -----------------------------
# CUSTOM CSS
# -----------------------------

st.markdown("""
<style>

.main {
    background-color: #0f172a;
}

h1,h2,h3,h4 {
    color: white;
}

[data-testid="stMetric"] {
    background-color: #1e293b;
    padding: 15px;
    border-radius: 15px;
    border: 1px solid #334155;
}

.stDataFrame {
    border-radius: 12px;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------
# TITLE
# -----------------------------

st.title("🤖 AI Agent EDA Dashboard")
st.write(
    "Upload CSV or Excel files and get automatic statistics, AI insights, and interactive visualizations."
)

# -----------------------------
# SIDEBAR
# -----------------------------

st.sidebar.title("⚙ Dashboard Settings")

theme = st.sidebar.selectbox(
    "Select Theme",
    ["Dark", "Light"]
)

# -----------------------------
# FILE UPLOAD
# -----------------------------

uploaded_file = st.file_uploader(
    "📂 Upload CSV or Excel File",
    type=["csv", "xlsx", "xls"]
)

# -----------------------------
# READ FILE
# -----------------------------

if uploaded_file is not None:

    file_name = uploaded_file.name

    # CSV
    if file_name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)

    # EXCEL
    else:
        df = pd.read_excel(uploaded_file)

    st.success(f"✅ File Uploaded Successfully: {file_name}")

    # -----------------------------
    # OVERVIEW
    # -----------------------------

    st.header("📌 Dataset Overview")

    total_rows = df.shape[0]
    total_cols = df.shape[1]
    missing_values = df.isnull().sum().sum()
    duplicate_rows = df.duplicated().sum()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Rows", total_rows)
    col2.metric("Columns", total_cols)
    col3.metric("Missing Values", missing_values)
    col4.metric("Duplicate Rows", duplicate_rows)

    # -----------------------------
    # DATA TYPES
    # -----------------------------

    st.header("📋 Column Information")

    info_df = pd.DataFrame({
        "Column": df.columns,
        "Data Type": df.dtypes.astype(str),
        "Missing Values": df.isnull().sum().values
    })

    st.dataframe(info_df, use_container_width=True)

    # -----------------------------
    # DATA PREVIEW
    # -----------------------------

    st.header("🗂 Dataset Preview")

    st.dataframe(df.head(20), use_container_width=True)

    # -----------------------------
    # NUMERIC & CATEGORICAL
    # -----------------------------

    numeric_cols = df.select_dtypes(include=np.number).columns.tolist()

    categorical_cols = df.select_dtypes(
        exclude=np.number
    ).columns.tolist()

    # -----------------------------
    # AI INSIGHTS
    # -----------------------------

    st.header("🧠 AI Generated Insights")

    insights = []

    insights.append(
        f"Dataset contains {total_rows} rows and {total_cols} columns."
    )

    insights.append(
        f"Detected {len(numeric_cols)} numeric columns."
    )

    insights.append(
        f"Detected {len(categorical_cols)} categorical columns."
    )

    insights.append(
        f"Total missing values detected: {missing_values}"
    )

    insights.append(
        f"Duplicate rows found: {duplicate_rows}"
    )

    if len(numeric_cols) > 0:

        for col in numeric_cols:

            avg = round(df[col].mean(), 2)
            maximum = round(df[col].max(), 2)
            minimum = round(df[col].min(), 2)

            insights.append(
                f"{col}: average={avg}, minimum={minimum}, maximum={maximum}"
            )

    for item in insights:
        st.info(item)

    # -----------------------------
    # STATISTICS
    # -----------------------------

    st.header("📊 Statistical Analysis")

    if len(numeric_cols) > 0:

        st.dataframe(
            df[numeric_cols].describe(),
            use_container_width=True
        )

    # -----------------------------
    # MISSING VALUES
    # -----------------------------

    st.header("❌ Missing Values Analysis")

    missing_df = pd.DataFrame({
        "Column": df.columns,
        "Missing Values": df.isnull().sum().values
    })

    fig_missing = px.bar(
        missing_df,
        x="Column",
        y="Missing Values",
        title="Missing Values Per Column",
        template="plotly_dark"
    )

    st.plotly_chart(fig_missing, use_container_width=True)

    # -----------------------------
    # VISUALIZATION SECTION
    # -----------------------------

    st.header("📈 Interactive Visualizations")

    # BAR CHART

    if len(categorical_cols) > 0 and len(numeric_cols) > 0:

        st.subheader("📊 Bar Chart")

        x_bar = st.selectbox(
            "Select X-axis",
            categorical_cols,
            key="bar_x"
        )

        y_bar = st.selectbox(
            "Select Y-axis",
            numeric_cols,
            key="bar_y"
        )

        fig_bar = px.bar(
            df.head(20),
            x=x_bar,
            y=y_bar,
            color=y_bar,
            template="plotly_dark",
            title=f"{y_bar} by {x_bar}"
        )

        st.plotly_chart(fig_bar, use_container_width=True)

    # LINE CHART

    if len(numeric_cols) > 0:

        st.subheader("📈 Line Chart")

        line_col = st.selectbox(
            "Select Column for Line Chart",
            numeric_cols,
            key="line_chart"
        )

        fig_line = px.line(
            df,
            y=line_col,
            template="plotly_dark",
            title=f"Trend Analysis - {line_col}"
        )

        st.plotly_chart(fig_line, use_container_width=True)

    # PIE CHART

    if len(categorical_cols) > 0:

        st.subheader("🥧 Pie Chart")

        pie_col = st.selectbox(
            "Select Category Column",
            categorical_cols,
            key="pie_chart"
        )

        pie_data = df[pie_col].value_counts().reset_index()

        pie_data.columns = [pie_col, "Count"]

        fig_pie = px.pie(
            pie_data,
            names=pie_col,
            values="Count",
            template="plotly_dark",
            title=f"Distribution of {pie_col}"
        )

        st.plotly_chart(fig_pie, use_container_width=True)

    # HISTOGRAM

    if len(numeric_cols) > 0:

        st.subheader("📉 Histogram")

        hist_col = st.selectbox(
            "Select Histogram Column",
            numeric_cols,
            key="histogram"
        )

        fig_hist = px.histogram(
            df,
            x=hist_col,
            template="plotly_dark",
            title=f"Histogram - {hist_col}"
        )

        st.plotly_chart(fig_hist, use_container_width=True)

    # SCATTER PLOT

    if len(numeric_cols) >= 2:

        st.subheader("🔵 Scatter Plot")

        scatter_x = st.selectbox(
            "Scatter X-axis",
            numeric_cols,
            key="scatter_x"
        )

        scatter_y = st.selectbox(
            "Scatter Y-axis",
            numeric_cols,
            index=1,
            key="scatter_y"
        )

        fig_scatter = px.scatter(
            df,
            x=scatter_x,
            y=scatter_y,
            template="plotly_dark",
            title=f"{scatter_y} vs {scatter_x}"
        )

        st.plotly_chart(fig_scatter, use_container_width=True)

    # BOX PLOT

    if len(numeric_cols) > 0:

        st.subheader("📦 Box Plot")

        box_col = st.selectbox(
            "Select Box Plot Column",
            numeric_cols,
            key="boxplot"
        )

        fig_box = px.box(
            df,
            y=box_col,
            template="plotly_dark",
            title=f"Box Plot - {box_col}"
        )

        st.plotly_chart(fig_box, use_container_width=True)

    # HEATMAP

    if len(numeric_cols) > 1:

        st.subheader("🔥 Correlation Heatmap")

        corr = df[numeric_cols].corr()

        fig_heatmap = px.imshow(
            corr,
            text_auto=True,
            color_continuous_scale="Blues",
            title="Correlation Matrix"
        )

        st.plotly_chart(fig_heatmap, use_container_width=True)

    # -----------------------------
    # DOWNLOAD SECTION
    # -----------------------------

    st.header("⬇ Download Processed Data")

    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="📥 Download CSV",
        data=csv,
        file_name="processed_data.csv",
        mime="text/csv"
    )

    # -----------------------------
    # FOOTER
    # -----------------------------

    st.markdown("---")

    st.markdown("""
    ### 🚀 Features Included

    ✅ CSV Upload  
    ✅ Excel Upload  
    ✅ Automatic EDA  
    ✅ AI Insights  
    ✅ Statistics  
    ✅ Missing Value Detection  
    ✅ Duplicate Detection  
    ✅ Heatmap  
    ✅ Histogram  
    ✅ Scatter Plot  
    ✅ Box Plot  
    ✅ Interactive Dashboard  
    ✅ Download Dataset  
    ✅ Professional UI  
    """)

else:

    st.warning("⚠ Please upload a CSV or Excel file.")
