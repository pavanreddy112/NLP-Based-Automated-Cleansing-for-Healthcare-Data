import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest
from sklearn.svm import OneClassSVM
import os

def bill_anomoly_page():
    # Function for preprocessing (normalizing Billing Amount)
    def preprocess_billing_data(df):
        df = df.dropna(subset=['Billing Amount'])
        scaler = StandardScaler()
        df['Normalized Billing Amount'] = scaler.fit_transform(df[['Billing Amount']])
        return df

    # Anomaly Detection with Isolation Forest
    def isolation_forest_anomaly_detection(df):
        model = IsolationForest(contamination=0.05)
        df['Anomaly_Status'] = model.fit_predict(df[['Normalized Billing Amount']])
        df['Anomaly_Status'] = df['Anomaly_Status'].map({1: 'Normal', -1: 'Suspected Anomaly'})
        return df

    # Anomaly Detection with One-Class SVM
    def one_class_svm_anomaly_detection(df):
        model = OneClassSVM(nu=0.05, kernel='rbf', gamma='scale')
        df['Anomaly_Status'] = model.fit_predict(df[['Normalized Billing Amount']])
        df['Anomaly_Status'] = df['Anomaly_Status'].map({1: 'Normal', -1: 'Suspected Anomaly'})
        return df

    # Streamlit App Title
    st.title("💸 Billing Anomaly Detection")

    # Load Latest Uploaded CSV
    UPLOAD_FOLDER = "uploads"
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    files = [f for f in os.listdir(UPLOAD_FOLDER) if f.endswith('.csv')]

    if files:
        latest_file = max(files, key=lambda f: os.path.getctime(os.path.join(UPLOAD_FOLDER, f)))
        file_path = os.path.join(UPLOAD_FOLDER, latest_file)
        df = pd.read_csv(file_path)


        # Preprocess Data
        df = preprocess_billing_data(df)

        # Sidebar: Anomaly Detection Method Selection
        st.sidebar.subheader("Anomaly Detection Method")
        detection_method = st.sidebar.selectbox("Choose an anomaly detection method:", ["Isolation Forest", "One-Class SVM"])

        # Apply Anomaly Detection
        if detection_method == "Isolation Forest":
            df = isolation_forest_anomaly_detection(df)
        elif detection_method == "One-Class SVM":
            df = one_class_svm_anomaly_detection(df)

        # Sidebar: Filter by Anomaly Status
        st.sidebar.subheader("Filter Data by Anomaly Status")
        anomaly_filter = st.sidebar.selectbox("Select Anomaly Status to Display:", ["Normal", "Suspected Anomaly"])
        filtered_data = df[df['Anomaly_Status'] == anomaly_filter]

        # **1️⃣ Show Filtered Data First**
        st.subheader(f"📋 {anomaly_filter} Billing Records")
        st.write(f"Total {anomaly_filter} Records: {filtered_data.shape[0]}")
        filtered_data_table = filtered_data[['Name', 'Medical Condition', 'Gender', 'Billing Amount', 'Anomaly_Status']]
        filtered_data_table.rename(columns={'Anomaly_Status': 'Status'}, inplace=True)
        st.dataframe(filtered_data_table)

        # **2️⃣ Pie Chart - Anomalous vs Normal Billing**
        st.subheader("📊 Anomaly vs Normal Billing Distribution")
        fig = plt.figure(figsize=(8, 8))
        df['Anomaly_Status'].value_counts().plot.pie(autopct='%1.1f%%', startangle=90, colors=['#ff9999', '#66b3ff'])
        plt.title("Suspected Anomalies vs Normal Billing")
        st.pyplot(fig)

        # **3️⃣ Scatter Plot - Billing Amount vs Index**
        st.subheader("📊 Billing Anomalies")
        fig, ax = plt.subplots(figsize=(10, 6))
        normal_data = df[df['Anomaly_Status'] == 'Normal']
        anomaly_data = df[df['Anomaly_Status'] == 'Suspected Anomaly']
        ax.scatter(normal_data.index, normal_data['Billing Amount'], c='blue', label='Normal', alpha=0.6)
        ax.scatter(anomaly_data.index, anomaly_data['Billing Amount'], c='red', label='Suspected Anomaly', alpha=0.6)
        ax.set_title("Billing Amount with Anomalies Highlighted")
        ax.set_xlabel("Index")
        ax.set_ylabel("Billing Amount")
        ax.legend()
        st.pyplot(fig)

        # **4️⃣ Distribution of Billing Amounts**
        st.subheader("📈 Distribution of Billing Amounts")
        fig = plt.figure(figsize=(10, 6))
        ax = fig.add_subplot(111)
        ax.hist(df['Billing Amount'], bins=30, color='lightblue', edgecolor='black')
        ax.set_title("Distribution of Billing Amounts")
        ax.set_xlabel("Billing Amount")
        ax.set_ylabel("Frequency")
        st.pyplot(fig)

        # **5️⃣ Display Sample of Data**
        st.subheader("📋 Data with Detected Anomalies")
        st.write(df[['Billing Amount', 'Anomaly_Status']].head())

        # **6️⃣ Anomaly Summary**
        st.subheader("📊 Anomaly Detection Summary")
        anomaly_percentage = (df['Anomaly_Status'].value_counts(normalize=True)['Suspected Anomaly']) * 100
        st.write(f"Suspected Anomalous Billing Amounts: {anomaly_percentage:.2f}%")
