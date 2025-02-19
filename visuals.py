import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import numpy as np
from wordcloud import WordCloud

def visual_page():
    st.title("📊 Data Visualization Dashboard")

    # Ensure the uploads directory exists
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


        # Display Preview
        st.write("### 📋 Preview of Data:")
        st.write(df.head())

        # Basic Statistics
        st.subheader('📊 Basic Statistics')
        st.write(df.describe())

        # Handling Date Columns
        date_columns = ['Date of Admission', 'Discharge Date']
        for col in date_columns:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors='coerce')

        # 1️⃣ Yearly Admissions
        if 'Date of Admission' in df.columns:
            df['Admission Year'] = df['Date of Admission'].dt.year
            st.subheader('📊 Yearly Patient Admissions')
            plt.figure(figsize=(10, 5))
            sns.countplot(x=df['Admission Year'].dropna(), palette='viridis')
            plt.xticks(rotation=45)
            plt.xlabel("Year")
            plt.ylabel("Number of Admissions")
            plt.title("Patient Admissions Per Year")
            st.pyplot(plt)

        # 2️⃣ Yearly Discharges
        if 'Discharge Date' in df.columns:
            df['Discharge Year'] = df['Discharge Date'].dt.year
            st.subheader('📊 Yearly Patient Discharges')
            plt.figure(figsize=(10, 5))
            sns.countplot(x=df['Discharge Year'].dropna(), hue=df['Discharge Year'].dropna(), palette='coolwarm', legend=False)

            plt.xticks(rotation=45)
            plt.xlabel("Year")
            plt.ylabel("Number of Discharges")
            plt.title("Patient Discharges Per Year")
            st.pyplot(plt)

        # 3️⃣ Billing Amount Histogram
        if 'Billing Amount' in df.columns:
            st.subheader('💰 Billing Amount Distribution')
            df['Billing Amount Log'] = np.log1p(df['Billing Amount'][df['Billing Amount'] > 0].dropna())

            plt.figure(figsize=(10, 5))
            sns.histplot(df['Billing Amount Log'], bins=30, kde=True, color='teal')
            plt.xlabel("Log of Billing Amount")
            plt.ylabel("Frequency")
            plt.title("Distribution of Billing Amount (Log Transformed)")
            st.pyplot(plt)

        # 4️⃣ Gender Distribution
        if 'Gender' in df.columns:
            st.subheader('👥 Gender Distribution')
            plt.figure(figsize=(6, 6))
            gender_counts = df['Gender'].value_counts()
            plt.pie(gender_counts, labels=gender_counts.index, autopct='%1.1f%%', colors=['skyblue', 'pink'], startangle=90)
            plt.title("Gender Distribution")
            st.pyplot(plt)

        # 5️⃣ Age Group Distribution
        if 'Age' in df.columns:
            st.subheader('📈 Age Group Distribution')
            bins = [0, 18, 35, 50, 65, 100]
            labels = ['0-18', '19-35', '36-50', '51-65', '65+']
            df['Age Group'] = pd.cut(df['Age'], bins=bins, labels=labels, right=False)
            plt.figure(figsize=(10, 5))
            sns.countplot(x=df['Age Group'].dropna(), hue=df['Age Group'].dropna(), palette='muted', legend=False)


            plt.xlabel("Age Group")
            plt.ylabel("Count")
            plt.title("Distribution of Patients by Age Group")
            st.pyplot(plt)

        # 6️⃣ WordCloud for Medical Conditions
        if 'Medical Condition' in df.columns:
            st.subheader('🩺 Most Common Medical Conditions')
            text = " ".join(df['Medical Condition'].dropna().astype(str).values)
            wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
            plt.figure(figsize=(10, 5))
            plt.imshow(wordcloud, interpolation='bilinear')
            plt.axis("off")
            st.pyplot(plt)
        if 'Blood Group' in df.columns:
            st.subheader('🩸 Blood Group Distribution')
            plt.figure(figsize=(6, 6))
            blood_counts = df['Blood Group'].value_counts()
            plt.pie(blood_counts, labels=blood_counts.index, autopct='%1.1f%%', colors=['red', 'blue', 'green', 'purple', 'orange'], startangle=90)
            plt.title("Blood Group Distribution")
            st.pyplot(plt)

        # 🏥 **2️⃣ Insurance Provider Distribution (Percentage Breakdown)**
        if 'Insurance Provider' in df.columns:
            st.subheader('🏥 Insurance Provider Distribution')
            plt.figure(figsize=(6, 6))
            insurance_counts = df['Insurance Provider'].value_counts()
            plt.pie(insurance_counts, labels=insurance_counts.index, autopct='%1.1f%%', colors=['lightblue', 'pink', 'gray', 'yellow'], startangle=90)
            plt.title("Insurance Provider Breakdown")
            st.pyplot(plt)

        # 💰 **3️⃣ Billing Amount Histogram**
        if 'Billing Amount' in df.columns:
            st.subheader('💰 Billing Amount Distribution')
            df['Billing Amount Log'] = np.log1p(df['Billing Amount'].dropna())  # Log transform to handle skewness
            plt.figure(figsize=(10, 5))
            sns.histplot(df['Billing Amount Log'], bins=30, kde=True, color='teal')
            plt.xlabel("Log of Billing Amount")
            plt.ylabel("Frequency")
            plt.title("Distribution of Billing Amount (Log Transformed)")
            st.pyplot(plt)

        # 💊 **4️⃣ Medication/Test Results (Count Plot)**
        if 'Medication/Test Results' in df.columns:
            st.subheader('💊 Medication/Test Results Distribution')
            plt.figure(figsize=(12, 6))
            sns.countplot(y=df['Medication/Test Results'], order=df['Medication/Test Results'].value_counts().index, palette='muted')
            plt.xlabel("Count")
            plt.ylabel("Medication/Test Results")
            plt.title("Distribution of Medication & Test Results")
            st.pyplot(plt)

        # 7️⃣ Correlation Heatmap (Numerical Columns)
        st.subheader("🔥 Correlation Heatmap")
        numeric_cols = df.select_dtypes(include=['number']).columns
        if len(numeric_cols) > 1:
            plt.figure(figsize=(10, 6))
            sns.heatmap(df[numeric_cols].corr(), annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5)
            plt.title("Correlation Heatmap")
            st.pyplot(plt)
        else:
            st.warning("⚠ Not enough numerical data to generate a heatmap.")

    else:
        st.error("❌ No CSV file found in the 'uploads' folder. Please place a dataset in the folder and restart the app.")

# Call the function if running as a script
if __name__ == "__main__":
    visual_page()
