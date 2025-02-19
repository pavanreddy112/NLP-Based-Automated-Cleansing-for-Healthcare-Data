import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest
from sklearn.metrics import classification_report, confusion_matrix, roc_curve, auc
from sklearn.model_selection import train_test_split
import os

def performace_metrics():
    # Set Streamlit app title
    st.title("📊 Performance Metrics & Testing Results")
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
        required_columns = ["Medical Condition", "Billing Amount"]
        missing_columns = [col for col in required_columns if col not in df.columns]

        if missing_columns:
            st.error(f"❌ Missing columns: {', '.join(missing_columns)}")
        else:
            # Convert Billing Amount to numeric
            df["Billing Amount"] = pd.to_numeric(df["Billing Amount"], errors="coerce").fillna(0)

            # Encode Medical Condition as numerical features
            df["Medical_Condition_Code"] = df["Medical Condition"].astype("category").cat.codes

            # Splitting Data into Train and Test
            X = df[["Medical_Condition_Code", "Billing Amount"]]
            X_train, X_test = train_test_split(X, test_size=0.2, random_state=42)

            # Apply Isolation Forest for anomaly detection
            model = IsolationForest(contamination=0.05, random_state=42)
            model.fit(X_train)

            # Predict anomalies
            df["Anomaly_Predicted"] = model.predict(X)
            df["Anomaly_Status"] = df["Anomaly_Predicted"].map({-1: "Rare Condition", 1: "Common Condition"})

            # Generate performance metrics
            y_true = np.where(df["Anomaly_Status"] == "Rare Condition", 1, 0)
            y_pred = np.where(df["Anomaly_Predicted"] == -1, 1, 0)

            # Classification Report in Table Format
            report = classification_report(y_true, y_pred, output_dict=True)
            report_df = pd.DataFrame(report).transpose()
            
            st.subheader("📌 Classification Report")
            st.dataframe(report_df.style.format(precision=2))  # Display as table with 2 decimal places

            # Confusion Matrix
            st.subheader("📊 Confusion Matrix")
            cm = confusion_matrix(y_true, y_pred)
            fig, ax = plt.subplots()
            sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=["Non-Anomaly", "Anomaly"], yticklabels=["Non-Anomaly", "Anomaly"])
            plt.xlabel("Predicted")
            plt.ylabel("Actual")
            st.pyplot(fig)

            # ROC Curve
            fpr, tpr, _ = roc_curve(y_true, y_pred)
            roc_auc = auc(fpr, tpr)

            st.subheader("📈 ROC Curve")
            fig, ax = plt.subplots()
            ax.plot(fpr, tpr, color="blue", lw=2, label=f"AUC = {roc_auc:.2f}")
            ax.plot([0, 1], [0, 1], color="gray", linestyle="--")
            ax.set_xlabel("False Positive Rate")
            ax.set_ylabel("True Positive Rate")
            ax.set_title("ROC Curve")
            ax.legend(loc="lower right")
            st.pyplot(fig)

            # Pie Chart of Anomalies
            st.subheader("📊 Anomaly Distribution")
            anomaly_counts = df["Anomaly_Status"].value_counts()
            fig_pie = px.pie(
                values=anomaly_counts.values,
                names=anomaly_counts.index,
                title="Anomaly vs. Non-Anomaly Distribution",
                color=anomaly_counts.index,
                color_discrete_map={"Common Condition": "green", "Rare Condition": "red"},
            )
            st.plotly_chart(fig_pie)

            # Distribution of Billing Amount for Anomalies vs. Non-Anomalies
            st.subheader("💰 Billing Amount Distribution")
            fig_hist = px.histogram(
                df, x="Billing Amount", color="Anomaly_Status",
                title="Billing Amount Comparison (Rare vs Common Conditions)",
                barmode="overlay", opacity=0.6
            )
            st.plotly_chart(fig_hist)
