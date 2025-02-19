import streamlit as st
import requests

# IBM Cloud API Credentials
API_KEY = "26OF7RolbSCEU03s0h9fHXgbbEE_5TBVW7SXSW4OmaoL"  # Replace with your IBM API key
DEPLOYMENT_URL = "https://private.us-south.ml.cloud.ibm.com/ml/v4/deployments/fe8ead3a-16d8-45e2-805f-914f4a2206df/predictions?version=2021-05-01"

# Function to get IBM authentication token
def get_ibm_token():
    token_url = "https://iam.cloud.ibm.com/identity/token"
    payload = {"apikey": API_KEY, "grant_type": "urn:ibm:params:oauth:grant-type:apikey"}
    response = requests.post(token_url, data=payload)
    return response.json().get("access_token")

# Function to predict medical condition
def predict_medical_condition(inputs):
    token = get_ibm_token()
    if not token:
        return "❌ Authentication Failed"

    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    
    # Constructing JSON in required format
    payload = {
        "input_data": [
            {
                "fields": [
                    "Name", "Age", "Gender", "Blood Type", "Date of Admission", "Doctor", 
                    "Hospital", "Insurance Provider", "Billing Amount", "Room Number", 
                    "Admission Type", "Discharge Date", "Medication", "Test Results"
                ],
                "values": [inputs]
            }
        ]
    }

    # Sending request to IBM API
    response = requests.post(DEPLOYMENT_URL, json=payload, headers=headers)

    if response.status_code == 200:
        prediction = response.json()["predictions"][0]["values"][0][0]  # Extract prediction
        return f"🩺 **Predicted Medical Condition:** {prediction}"
    else:
        return f"❌ API Error: {response.text}"

# Streamlit UI
def predict_page():
    st.title("🩺 AI-Based Medical Condition Predictor")

    # Form for user input
    with st.form("medical_form"):
        name = st.text_input("👤 Name")
        age = st.number_input("👴 Age", min_value=0, max_value=120, step=1)
        gender = st.selectbox("🚻 Gender", ["Male", "Female", "Other"])
        blood_type = st.selectbox("🩸 Blood Type", ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"])
        date_of_admission = st.date_input("📅 Date of Admission")
        doctor = st.text_input("👨‍⚕️ Doctor's Name")
        hospital = st.text_input("🏥 Hospital Name")
        insurance_provider = st.text_input("💳 Insurance Provider")
        billing_amount = st.number_input("💰 Billing Amount", min_value=0, step=100)
        room_number = st.text_input("🚪 Room Number")
        admission_type = st.selectbox("📑 Admission Type", ["Emergency", "Elective", "Routine"])
        discharge_date = st.date_input("📅 Discharge Date")
        medication = st.text_area("💊 Medication (comma-separated)")
        test_results = st.text_area("📝 Test Results")

        submit_button = st.form_submit_button("🔍 Predict Condition")

    if submit_button:
        user_inputs = [
            name, age, gender, blood_type, str(date_of_admission), doctor, hospital,
            insurance_provider, billing_amount, room_number, admission_type,
            str(discharge_date), medication, test_results
        ]
        
        # Call prediction function
        result = predict_medical_condition(user_inputs)
        st.success(result)

if __name__ == "__main__":
    predict_page()
