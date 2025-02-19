import streamlit as st

# Custom CSS for better UI styling
st.markdown("""
    <style>
        /* Background and Font */
        body {
            background-color: #f4f9fc;
            font-family: 'Arial', sans-serif;
        }
        
        /* Title Styling */
        .title {
            font-size: 36px;
            font-weight: bold;
            color: #004d99;
            text-align: center;
            margin-bottom: 20px;
        }
        
        /* Section Headers */
        .section-header {
            font-size: 24px;
            font-weight: bold;
            color: #0073e6;
            margin-top: 30px;
            border-left: 5px solid #0073e6;
            padding-left: 10px;
        }
        
        /* Paragraph Text */
        .content-text {
            font-size: 16px;
            line-height: 1.6;
            color: #333;
            text-align: justify;
        }
        
        /* Icon Styling */
        .icon {
            font-size: 20px;
            color: #0073e6;
            margin-right: 10px;
        }

        /* Box Styling */
        .info-box {
            background-color: white;
            border-radius: 8px;
            padding: 15px;
            margin-top: 15px;
            box-shadow: 0px 2px 10px rgba(0, 0, 0, 0.1);
        }

    </style>
""", unsafe_allow_html=True)

def home_page():
    st.markdown('<h1 class="title">🏠 NLP-Based Automated Cleansing for Healthcare Data</h1>', unsafe_allow_html=True)

    # Introduction Section
    st.markdown('<h2 class="section-header">🧑‍⚕️ Introduction</h2>', unsafe_allow_html=True)
    st.markdown('<p class="content-text">Healthcare data is often inconsistent, containing redundant or inaccurate information due to manual errors, mismatched formats, or unstructured data sources. NLP (Natural Language Processing) offers a solution by automating the cleansing process to ensure accurate, structured, and meaningful data for healthcare professionals and researchers.</p>', unsafe_allow_html=True)

    # Features of NLP-Based Cleansing
    st.markdown('<h2 class="section-header">🚀 Features of NLP-Based Cleansing</h2>', unsafe_allow_html=True)
    
    features = {
        "📌 Duplicate Record Removal": "Detects and eliminates duplicate patient records and redundant medical entries.",
        "📌 Standardization": "Converts various medical terminologies, formats, and abbreviations into standardized data.",
        "📌 Anomaly Detection": "Identifies unusual or incorrect values in patient data, such as incorrect dosages or symptoms.",
        "📌 Data Imputation": "Fills missing fields intelligently based on medical context and historical data.",
        "📌 Named Entity Recognition (NER)": "Extracts relevant medical entities such as diseases, medications, and procedures from unstructured text.",
        "📌 Sentiment Analysis": "Analyzes patient feedback and medical reports to gain insights into healthcare service quality."
    }

    for feature, description in features.items():
        st.markdown(f'<div class="info-box"><span class="icon">{feature}</span><p class="content-text">{description}</p></div>', unsafe_allow_html=True)

    # Benefits Section
    st.markdown('<h2 class="section-header">🌟 Benefits of Automated Healthcare Data Cleansing</h2>', unsafe_allow_html=True)
    benefits = [
        "✅ Improves the accuracy of Electronic Health Records (EHR).",
        "✅ Reduces manual effort and administrative costs in data processing.",
        "✅ Enhances patient safety by preventing errors in prescriptions and diagnoses.",
        "✅ Speeds up medical research by providing clean, structured datasets.",
        "✅ Enables better decision-making for doctors and healthcare providers."
    ]

    for benefit in benefits:
        st.markdown(f'<div class="info-box"><span class="icon">✔</span><p class="content-text">{benefit}</p></div>', unsafe_allow_html=True)

    # Conclusion
    st.markdown('<h2 class="section-header">🔍 Conclusion</h2>', unsafe_allow_html=True)
    st.markdown('<p class="content-text">NLP-powered data cleansing in healthcare is a transformative approach that ensures data accuracy, improves patient care, and accelerates medical research. By leveraging AI-driven techniques, hospitals and research centers can enhance data-driven decision-making while reducing errors and inefficiencies.</p>', unsafe_allow_html=True)
