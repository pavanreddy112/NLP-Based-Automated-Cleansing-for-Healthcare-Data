import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.ensemble import IsolationForest
import os
def disease_analysis():
    # Set Streamlit app title
    st.title("🩺 Medical Condition Anomaly Detection")

    # File Upload
    UPLOAD_FOLDER = "uploads"
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    # Get the list of files in the uploads folder
    files = [f for f in os.listdir(UPLOAD_FOLDER) if f.endswith('.csv')]

    if files:
        # Load the latest file in the uploads folder
        latest_file = max(files, key=lambda f: os.path.getctime(os.path.join(UPLOAD_FOLDER, f)))
        file_path = os.path.join(UPLOAD_FOLDER, latest_file)

        # Load the dataset
        df = pd.read_csv(file_path)





        # Ensure required columns exist
        required_columns = ["Name", "Age", "Gender", "Medical Condition", "Billing Amount"]
        missing_columns = [col for col in required_columns if col not in df.columns]

        if missing_columns:
            st.error(f"❌ Missing columns: {', '.join(missing_columns)}")
        else:
            # Convert Billing Amount to numeric (handling missing values)
            df["Billing Amount"] = pd.to_numeric(df["Billing Amount"], errors="coerce").fillna(0)

            # Encode Medical Condition as numerical features
            df["Medical_Condition_Code"] = df["Medical Condition"].astype("category").cat.codes

            # Apply Isolation Forest for anomaly detection
            model = IsolationForest(contamination=0.05, random_state=42)  # 5% contamination assumed
            df["Anomaly"] = model.fit_predict(df[["Medical_Condition_Code", "Billing Amount"]])

            # Map -1 to "Rare Condition" and 1 to "Common Condition"
            df["Anomaly_Status"] = df["Anomaly"].map({-1: "Rare Condition", 1: "Common Condition"})

            

            # Count occurrences
            anomaly_counts = df["Anomaly_Status"].value_counts()
            total_patients = len(df)
            anomaly_percentage = anomaly_counts.get("Rare Condition", 0) / total_patients * 100

            # Display Key Metrics
            st.metric("Total Patients", total_patients)
            st.metric("Rare Condition Cases", anomaly_counts.get("Rare Condition", 0))
            st.metric("Percentage of Rare Conditions", f"{anomaly_percentage:.2f}%")

            # Filter based on condition type
            status_filter = st.radio("Filter by Condition Type", ["All", "Common Condition", "Rare Condition"])
            if status_filter != "All":
                df_filtered = df[df["Anomaly_Status"] == status_filter]
            else:
                df_filtered = df

            # Show filtered data
            st.subheader(f"Filtered Data ({status_filter})")
            st.dataframe(df_filtered[["Name", "Medical Condition", "Gender", "Billing Amount", "Anomaly_Status"]])

            # Visualization: Pie Chart of Anomalies
            fig_pie = px.pie(
                values=anomaly_counts.values,
                names=anomaly_counts.index,
                title="Distribution of Medical Conditions",
                color=anomaly_counts.index,
                color_discrete_map={"Common Condition": "green", "Rare Condition": "red"},
            )
            st.plotly_chart(fig_pie)

            # Visualization: Histogram of Billing Amount by Anomaly Status
            fig_hist = px.histogram(
                df, x="Billing Amount", color="Anomaly_Status",
                title="Billing Amount Distribution (Rare vs Common Conditions)",
                barmode="overlay", opacity=0.6
            )
            st.plotly_chart(fig_hist)

            # Visualization: Bar Chart for Most Frequent Medical Conditions
            condition_counts = df["Medical Condition"].value_counts().head(10)
            fig_bar = px.bar(
                x=condition_counts.index, y=condition_counts.values,
                title="Top 10 Most Common Medical Conditions",
                labels={"x": "Medical Condition", "y": "Count"},
                color=condition_counts.index
            )
            st.plotly_chart(fig_bar)
