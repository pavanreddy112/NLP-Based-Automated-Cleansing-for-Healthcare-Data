import streamlit as st
import os
import pandas as pd

UPLOAD_FOLDER = "uploads"

def upload_page():
    st.title("📂 Upload Your Dataset")

    # Ensure the uploads folder exists
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

    if uploaded_file is not None:
        # Generate a unique filename if the file already exists
        file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
        base_name, ext = os.path.splitext(uploaded_file.name)
        counter = 1

        while os.path.exists(file_path):
            file_path = os.path.join(UPLOAD_FOLDER, f"{base_name}_{counter}{ext}")
            counter += 1

        # Save file
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        st.success(f"✅ File saved successfully: `{os.path.basename(file_path)}`")

        # Read and display the dataset
        df = pd.read_csv(file_path)

        st.write("### 📋 Data Preview")
        st.dataframe(df.head(20))  # Show first 20 rows

        st.write(f"📊 **Total Rows:** {df.shape[0]} | **Total Columns:** {df.shape[1]}")

        # Display column names
        st.write("📝 **Column Names:**")
        st.write(df.columns.tolist())

if __name__ == "__main__":
    upload_page()
