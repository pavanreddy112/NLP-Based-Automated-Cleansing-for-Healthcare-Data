import streamlit as st
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.impute import SimpleImputer
from sklearn.cluster import KMeans
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import plotly.express as px
from wordcloud import WordCloud

# Function to preprocess data
def preprocess_data(df):
    imputer = SimpleImputer(strategy="most_frequent")
    df_filled = df.apply(lambda x: imputer.fit_transform(x.values.reshape(-1, 1)).flatten() if x.isnull().any() else x)

    label_encoder = LabelEncoder()
    for column in df.select_dtypes(include=["object"]).columns:
        df_filled[column] = label_encoder.fit_transform(df_filled[column])

    numeric_columns = df_filled.select_dtypes(include=["number"]).columns
    scaler = StandardScaler()
    df_filled[numeric_columns] = scaler.fit_transform(df_filled[numeric_columns])

    return df_filled

# Function to find and load the latest CSV file from the uploads folder
def load_latest_csv():
    upload_folder = "uploads"
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)

    csv_files = [f for f in os.listdir(upload_folder) if f.endswith(".csv")]
    if not csv_files:
        return None  # No CSV files found

    latest_file = max(csv_files, key=lambda f: os.path.getmtime(os.path.join(upload_folder, f)))
    file_path = os.path.join(upload_folder, latest_file)
    return pd.read_csv(file_path)

# AI Visualization Page
def ai_visualization_page():
    st.title("🏥 AI-Driven Healthcare Data Analysis Dashboard")

    # Load latest CSV file
    df = load_latest_csv()
    if df is None:
        st.error("No CSV file found in the 'uploads' folder. Please add a CSV file and restart the app.")
        return

    # Data Preprocessing
    st.subheader("📂 Preprocessed Data")
    df_filled = preprocess_data(df)
    st.dataframe(df_filled.head())

    
    # **Admissions Time Series**
    if 'Date of Admission' in df.columns:
        st.write("### Admissions Trend")
        df['Date of Admission'] = pd.to_datetime(df['Date of Admission'], errors='coerce')
        df['Year'] = df['Date of Admission'].dt.year
        admissions_by_year = df['Year'].value_counts().sort_index()
        fig = px.bar(admissions_by_year, x=admissions_by_year.index, y=admissions_by_year.values, title="Admissions by Year")
        st.plotly_chart(fig)

    # **Billing Amount Prediction**
    if 'Billing Amount' in df.columns and 'Age' in df.columns:
        X = df_filled[['Age']]
        y = df_filled['Billing Amount']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        model = LinearRegression()
        model.fit(X_train, y_train)

        st.write("### Billing Amount Prediction")
        st.write(f"Predicted Billing Amount for Age 30: {model.predict([[30]])[0]:.2f}")
        st.write(f"Train Score: {model.score(X_train, y_train):.2f}")
        st.write(f"Test Score: {model.score(X_test, y_test):.2f}")

    # **Clustering (KMeans)**
    if 'Age' in df.columns and 'Billing Amount' in df.columns:
        kmeans = KMeans(n_clusters=3)
        df_filled['Cluster'] = kmeans.fit_predict(df_filled[['Age', 'Billing Amount']])

        st.write("### Clustering of Patients")
        fig = px.scatter(df_filled, x="Age", y="Billing Amount", color="Cluster", title="Patient Clusters")
        st.plotly_chart(fig)

    # **Correlation Matrix**
    st.write("### Correlation Heatmap")
    correlation_matrix = df_filled.corr()
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt='.2f', linewidths=0.5, ax=ax)
    st.pyplot(fig)
