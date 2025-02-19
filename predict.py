import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import os

def predict_page():
    # 🌟 Page Title
    st.title("🏥 Patient Stay & Billing Prediction Dashboard")
    st.markdown("📊 **Analyze and predict patient hospital stay duration & billing amounts based on past data.**")

    # 🔄 File Upload Handling
    UPLOAD_FOLDER = "uploads"
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    # Fetch available CSV files
    files = [f for f in os.listdir(UPLOAD_FOLDER) if f.endswith('.csv')]

    if files:
        # Load the most recent file
        latest_file = max(files, key=lambda f: os.path.getctime(os.path.join(UPLOAD_FOLDER, f)))
        file_path = os.path.join(UPLOAD_FOLDER, latest_file)

        # Load dataset
        df = pd.read_csv(file_path)
            
        # 🚨 **Check for Missing Columns**
        required_columns = ["Medical Condition", "Date of Admission", "Discharge Date", "Medication", "Billing Amount", "Admission Type"]
        missing_columns = [col for col in required_columns if col not in df.columns]

        if missing_columns:
            st.error(f"❌ **Missing columns in dataset:** {', '.join(missing_columns)}")
            return

        # 🕒 Convert dates to datetime
        df["Date of Admission"] = pd.to_datetime(df["Date of Admission"], errors="coerce")
        df["Discharge Date"] = pd.to_datetime(df["Discharge Date"], errors="coerce")

        # 💰 Convert Billing Amount to numeric
        df["Billing Amount"] = pd.to_numeric(df["Billing Amount"], errors="coerce").fillna(0)

        # 🏥 **Calculate Length of Stay**
        df["Stay Duration"] = (df["Discharge Date"] - df["Date of Admission"]).dt.days.fillna(0).astype(int)

        # ❌ **Filter out invalid stay durations**
        df = df[df["Stay Duration"] >= 0]

        # 📋 **Display List of Medical Conditions**
        st.subheader("🦠 Medical Conditions in Dataset")
        diseases = df["Medical Condition"].unique()
        disease_list = "\n".join([f"- {d}" for d in diseases])
        st.text(disease_list)

        # 📈 **Predictions: Stay Duration & Billing Amount**
        avg_stay = df.groupby("Medical Condition")["Stay Duration"].mean().sort_values(ascending=False)
        avg_billing = df.groupby("Medical Condition")["Billing Amount"].mean().sort_values(ascending=False)

        st.subheader("📊 Predicted Stay Duration & Billing Amount per Disease")
        for disease in avg_stay.index:
            stay_days = avg_stay[disease]
            billing_amount = avg_billing[disease]
            st.write(f"✅ **Patients with {disease} stay an average of {stay_days:.1f} days, with an average billing amount of ${billing_amount:,.2f}.**")

        # 💊 **Most Common Medications per Disease**
        st.subheader("💊 Most Prescribed Medications per Condition")
        top_medications = df.groupby("Medical Condition")["Medication"].agg(lambda x: x.value_counts().idxmax())

        medication_df = pd.DataFrame({
            "Medical Condition": top_medications.index,
            "Most Common Medication": top_medications.values
        })

        # 📑 **Display Medication Table with Styling**
        st.dataframe(medication_df.style.set_properties(**{
            'background-color': '#f4f4f4', 
            'border': '1px solid black',
            'text-align': 'center'
        }))

        # 📅 **Visualization: Stay Duration per Disease**
        st.subheader("📅 Average Stay Duration per Medical Condition")
        fig_stay = px.bar(avg_stay, 
                          x=avg_stay.index, 
                          y=avg_stay.values, 
                          labels={"x": "Medical Condition", "y": "Average Stay (Days)"},
                          title="Average Stay Duration per Disease", 
                          color=avg_stay.values, 
                          color_continuous_scale="reds")
        st.plotly_chart(fig_stay)

        # 💰 **Visualization: Billing Amount per Disease**
        st.subheader("💰 Average Billing Amount per Medical Condition")
        fig_billing = px.bar(avg_billing, 
                             x=avg_billing.index, 
                             y=avg_billing.values, 
                             labels={"x": "Medical Condition", "y": "Average Billing Amount ($)"},
                             title="Average Billing Amount per Disease", 
                             color=avg_billing.values, 
                             color_continuous_scale="blues")
        st.plotly_chart(fig_billing)

        # 🔍 **Scatter Plot: Billing vs Stay Duration**
        st.subheader("📊 Billing Amount vs Stay Duration")
        fig_scatter = px.scatter(df, 
                                 x="Stay Duration", 
                                 y="Billing Amount", 
                                 color="Medical Condition",
                                 title="Correlation between Stay Duration & Billing Amount", 
                                 opacity=0.7)
        st.plotly_chart(fig_scatter)

    else:
        st.warning("⚠️ **No uploaded files found. Please upload a dataset to proceed.**")
