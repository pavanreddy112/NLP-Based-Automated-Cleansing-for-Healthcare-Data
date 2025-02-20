# NLP-Based Automated Cleansing for Healthcare Data

This project focuses on the development of an AI-powered system designed to automate the cleansing of healthcare data using Natural Language Processing (NLP) techniques. The primary objective is to enhance the quality and reliability of medical datasets by addressing common issues such as inconsistencies, errors, and unstructured information.

## Project Overview

In the healthcare industry, vast amounts of data are generated daily, often containing inconsistencies, typographical errors, and unstructured formats. Manual data cleaning is time-consuming and prone to errors. This project leverages NLP to automate the data cleansing process, ensuring that healthcare datasets are accurate and standardized.

## Features

- **Automated Data Cleansing**: Utilizes NLP algorithms to detect and correct errors in medical records.
- **Standardization**: Ensures uniformity in data formats, such as dates, medical terminologies, and patient information.
- **Integration with IBM Cloud**: Employs IBM's cloud services for secure and scalable data processing.
- **User-Friendly Interface**: Provides a Streamlit-based web application for easy interaction and visualization.

## Data Description

The system processes various types of healthcare data, including:

- **Patient Information**: Names, ages, genders, and blood types.
- **Admission Details**: Dates of admission and discharge, room numbers, and types of admission (e.g., emergency, elective).
- **Medical Records**: Attending doctors, hospitals, medications prescribed, and test results.
- **Billing Information**: Insurance providers and billing amounts.

The data undergoes cleansing processes such as spell correction, standardization of medical terms, and formatting of dates to ensure consistency and accuracy.

## Getting Started

Follow these steps to set up and run the project locally.

### Prerequisites

- **Python 3.7 or higher**: Ensure Python is installed on your system.
- **IBM Cloud Account**: Required for accessing IBM's Machine Learning services.
- **API Key and Deployment URL**: Obtain these from your IBM Cloud account.

### Installation

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/pavanreddy112/NLP-Based-Automated-Cleansing-for-Healthcare-Data.git
   cd NLP-Based-Automated-Cleansing-for-Healthcare-Data
   ```


2. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```


### Configuration

1. **Set Up IBM Cloud Credentials**:

   - Replace the placeholder `API_KEY` in the script with your actual IBM Cloud API key.
   - Replace the placeholder `DEPLOYMENT_URL` with your IBM Machine Learning deployment URL.

   ```python
   API_KEY = "your_ibm_cloud_api_key"
   DEPLOYMENT_URL = "your_ibm_deployment_url"
   ```


### Running the Application

1. **Start the Streamlit App**:

   ```bash
   streamlit run main.py
   ```
   - Or
   ```bash
   python -m streamlit run main.py
   ```


2. **Access the Application**:

   - Open your web browser and navigate to `http://localhost:8501` to interact with the application.

## Usage

- **Data Input**: Enter patient and medical information into the provided form fields.
- **Data Cleansing**: The system will automatically process and cleanse the input data using NLP techniques.
- **Prediction**: After cleansing, the system utilizes IBM's Machine Learning models to predict potential medical conditions based on the provided data.

## Contributing

Contributions are welcome! Please fork the repository and create a pull request with your changes. Ensure that your code adheres to the project's coding standards and includes appropriate tests.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Acknowledgments

- IBM Cloud for providing the Machine Learning infrastructure.
- The open-source community for continuous contributions to NLP and data processing libraries.

---

By automating the data cleansing process, this project aims to improve the efficiency and accuracy of healthcare data management, ultimately contributing to better patient care and medical research. 