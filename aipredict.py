import streamlit as st
import requests
import json
import re
from datetime import datetime
from textblob import TextBlob  # NLP for Spelling Correction

# API Credentials
API_KEY = "LJ3Ez-krsVbjJYqMLxIPZtaU5PO72flDsfkKU5sWe-Pu"  # Replace with your actual API key
DEPLOYMENT_URL = "https://us-south.ml.cloud.ibm.com/ml/v4/deployments/6df9db5a-e5b2-42b7-a418-b68a8052a7e7/predictions?version=2021-05-01"

# 🛢️ Predefined Suggestions
DOCTORS = ["Dr. Smith", "Dr. Johnson", "Dr. Lee", "Dr. Patel"]
HOSPITALS = ["City Hospital", "Green Valley Medical Center", "St. Mary’s Hospital"]
MEDICATIONS = ["Aspirin", "Metformin", "Ibuprofen", "Lisinopril","Paracetamol", "Cough Syrup", "Insulin", "Blood Thinners","Antibiotics","Diuretics","ACE Inhibitors"

]
TEST_RESULTS = [
    "Normal", 
    "High Blood Pressure", 
    "Diabetes Type 2", 
    "Cholesterol Elevated",
    "High BP", 
    "Elevated Sugar Levels",
    "Mild Fever", 
    "Sinus Infection",
    "High Cholesterol", 
    "Cardiac Risk", 
    "Diabetes", 
    "Risk of Clots","Chronic Kidney Disease", "High BP","Asthma Attack", "Breathing Issues"


]

INSURANCE_PROVIDERS = ["BlueCross", "UnitedHealth", "Aetna", "Cigna"]

# 🛢️ Function to Get IBM Auth Token
def get_ibm_token():
    token_url = "https://iam.cloud.ibm.com/identity/token"
    payload = {"apikey": API_KEY, "grant_type": "urn:ibm:params:oauth:grant-type:apikey"}
    
    try:
        response = requests.post(token_url, data=payload, timeout=15)
        response.raise_for_status()
        return response.json().get("access_token")
    except requests.exceptions.RequestException as e:
        return f"ERROR: {e}"

# 🛢️ NLP-Based Data Cleansing
def clean_medical_data(user_inputs):
    # Spell Correction for Name
    user_inputs[0] = str(TextBlob(user_inputs[0]).correct()).title()
    
    # Standardize Gender
    gender_map = {"M": "Male", "F": "Female", "O": "Other"}
    user_inputs[2] = gender_map.get(user_inputs[2], user_inputs[2])
    
    # Validate Blood Type
    valid_blood_types = {"A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"}
    user_inputs[3] = user_inputs[3].upper() if user_inputs[3].upper() in valid_blood_types else "Unknown"
    
    # Extract Only Room Number (Remove Alphabets)
    user_inputs[9] = re.sub(r'\D', '', str(user_inputs[9])) or "0"
    
    # Convert Date Fields to YYYY-MM-DD Format
    try:
        user_inputs[4] = datetime.strptime(user_inputs[4], "%Y-%m-%d").strftime("%Y-%m-%d")
        user_inputs[11] = datetime.strptime(user_inputs[11], "%Y-%m-%d").strftime("%Y-%m-%d")
    except ValueError:
        user_inputs[4] = "0000-00-00"
        user_inputs[11] = "0000-00-00"
    
    return user_inputs

# 🛢️ Function to Predict Medical Condition
def predict_medical_condition(user_inputs):
    token = get_ibm_token()
    if "ERROR" in token:
        return f"❌ Authentication Failed: {token}"
    
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    
    payload = {
        "input_data": [
            {
                "fields": [
                    "Name", "Age", "Gender", "Blood Type", "Date of Admission", 
                    "Doctor", "Hospital", "Insurance Provider", "Billing Amount", 
                    "Room Number", "Admission Type", "Discharge Date", "Medication", "Test Results"
                ],
                "values": [user_inputs]
            }
        ]
    }
    
    try:
        response = requests.post(DEPLOYMENT_URL, json=payload, headers=headers, timeout=30)
        response.raise_for_status()
        result = response.json()
        prediction = result["predictions"][0]["values"][0][0]
        return f"🧬 **Predicted Medical Condition:** {prediction}"
    except requests.exceptions.RequestException as e:
        return f"❌ API Request Error: {e}"

# 🛢️ Streamlit UI
def predict_page():
    st.title("📝 NLP-Based Automated Cleansing for Healthcare Data")
    
    with st.form("medical_form"):
        name = st.text_input("👤 Name")
        age = st.number_input("👴 Age", min_value=0, max_value=120, step=1)
        gender = st.selectbox("🏣 Gender", ["Male", "Female", "Other"])
        blood_type = st.selectbox("🩸 Blood Type", ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"])
        date_of_admission = st.date_input("📅 Date of Admission")

        doctor = st.selectbox("👨‍⚕️ Doctor's Name", DOCTORS)
        hospital = st.selectbox("🏥 Hospital Name", HOSPITALS)
        insurance_provider = st.selectbox("💳 Insurance Provider", INSURANCE_PROVIDERS)

        billing_amount = st.number_input("💰 Billing Amount", min_value=0, step=100)
        room_number = st.text_input("🚪 Room Number")
        admission_type = st.selectbox("📝 Admission Type", ["Emergency", "Elective", "Routine"])
        discharge_date = st.date_input("📅 Discharge Date")

        medications = st.multiselect("💊 Medications", MEDICATIONS)
        test_results = st.multiselect("🗃️ Test Results", TEST_RESULTS)

        submit_button = st.form_submit_button("🔍 Predict Condition")
    
    if submit_button:
        final_medications = ", ".join(medications)
        final_test_results = ". ".join(test_results)
        
        user_inputs = [
            name, age, gender, blood_type, str(date_of_admission), doctor, hospital,
            insurance_provider, billing_amount, room_number, admission_type,
            str(discharge_date), final_medications, final_test_results
        ]
        
        cleaned_inputs = clean_medical_data(user_inputs)
        result = predict_medical_condition(cleaned_inputs)
        st.success(result)

if __name__ == "__main__":
    predict_page()
