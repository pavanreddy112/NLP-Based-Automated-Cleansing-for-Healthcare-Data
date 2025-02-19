import streamlit as st
from home import home_page
from ai_visualization import ai_visualization_page
from visuals import visual_page
from upload import upload_page
from bills import bill_anomoly_page
from diseases import disease_analysis
from performance import performace_metrics

from aipredict import predict_page
def main():
# 🔹 Custom CSS for styling
    st.markdown("""
        <style>
        /* Sidebar title styling */
        .sidebar-title {
            font-size: 26px !important;
            font-weight: bold !important;
            text-align: center;
            color: #2E8B57;
        }
        /* Larger navigation text */
        .sidebar .css-1v3fvcr {
            font-size: 18px !important;
        }
        </style>
    """, unsafe_allow_html=True)

    # 📌 **Custom Sidebar Title**
    st.sidebar.markdown('<h1 class="sidebar-title">🏥 Healthcare Insights</h1>', unsafe_allow_html=True)

    # 📍 **Navigation Menu**
    page = st.sidebar.radio(
        "Go to", 
        [
            "🏠 Home",
            "📤 Upload Data",
            "📊 Visualization",
            "🖥️ AI Visualization",
            "💰 Detection of Anomaly Bills",
            "🩺 Analysis of Diseases",
            "📈 Performance Metrics",
            "🤖 AI Prediction"
        ]
    )

    # 🔄 **Load the Selected Page**
    if page == "🏠 Home":
        home_page()
    elif page == "📊 Visualization":
        visual_page()
    elif page == "🖥️ AI Visualization":
        ai_visualization_page()
    elif page == "📤 Upload Data":
        upload_page()
    elif page == "💰 Detection of Anomaly Bills":
        bill_anomoly_page()
    elif page == "🩺 Analysis of Diseases":
        disease_analysis()
    elif page == "📈 Performance Metrics":
        performace_metrics()
    elif page == "🤖 AI Prediction":
        predict_page()

# ✅ **Run the App**
if __name__ == "__main__":
    main()
