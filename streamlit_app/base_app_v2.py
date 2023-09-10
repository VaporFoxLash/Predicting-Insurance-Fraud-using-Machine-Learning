"""
Simple Streamlit webserver application for serving developed insurance fraud detection
models.

Author: Radebe Lehlohonolo

Documentation:
https://docs.streamlit.io/en/latest/
"""

# Streamlit dependencies
import streamlit as st
import joblib, os
import pickle
# Data dependencies
import pandas as pd
from sklearn.preprocessing import StandardScaler, LabelEncoder

# Load your raw data
url = "https://raw.githubusercontent.com/Explore-AI/Public-Data/master/insurance_claims.csv"
raw = pd.read_csv(url)
# raw = pd.read_csv("resources/insurance_claims.csv")

# Importing feature_engineering function
from utils.feature_engineering import feature_engineering

# The main function where we will build the actual app
def main():
    """Insurance Fraud Detection App with Streamlit """
    # Creates a main title and subheader on your page -
    st.title("Insurance Fraud Detection App")
    st.subheader("Predict if an insurance claim is fraudulent or not")

    # Creating sidebar with selection box
    options = ["Prediction", "Information"]
    selection = st.sidebar.selectbox("Choose Option", options)

    # Building out the "Information" page
    if selection == "Information":
        st.info("General Information")
        st.markdown("This application classifies insurance claims as fraudulent or not based on provided input data.")
        st.subheader("Raw Insurance Claims Data")
        if st.checkbox('Show raw data'):  # data is hidden if box is unchecked
            st.write(raw)  # will display the dataframe

    # Create a file uploader for test data
    uploaded_file = st.file_uploader("Upload Test Data (CSV)", type="csv")

    # Building out the prediction page
    if selection == "Prediction":
        st.info("Predict if a claim is fraudulent")
        # Sample input features for prediction can be added here

        st.subheader("Capture customer information and make a prediction")
        # Convert user inputs to a dictionary
        # Inputs for the model
        age = st.text_input("Age")
        months_as_customer = st.text_input("months_as_customer")
        gender = st.selectbox("Gender", ["Select Gender", "Male", "Female"])
        vehicle_make = st.text_input("vehicle_make")
        auto_model = st.text_input("auto_model")
        incident_city = st.text_input("incident_city")
        incident_severity = st.text_input("incident_severity")
        police_report = st.selectbox("Police report available?", ["Option", "Yes", "No"])
        fraud_reported = st.selectbox("Fraud reported?", ["Option", "Yes", "No"])
        location = st.text_input("incident_location")
        auto_make = st.text_input("auto_make")
        policy_number = st.text_input("policy_number")
        incident_date = st.text_input("incident_date")
        total_claim_amount = st.text_input("total_claim_amount")
        # policy_annual_premium = st.text_input("policy_annual_premium")
        # umbrella_limit = st.text_input("umbrella_limit")
        witnesses = st.text_input("witnesses")
        # bodily_injuries = st.text_input("bodily_injuries")
        # property_damage = st.selectbox("property_damage", ["Option", "Yes", "No"])
        police_report_available = st.selectbox("police_report_available", ["Option", "Yes", "No"])
        incident_type = st.selectbox("incident_type", ["Select Incident Type", "Multi-vehicle collision", "Single vehicle collision", "Parked vehicle", "Vehicle theft"])

        inputs = {
            "age": age,
            "gender": gender,
            "auto_model": auto_model,
            "incident_city": incident_city,
            "incident_severity": incident_severity,
            "fraud_reported": fraud_reported,  # Note: This might not be necessary if you're predicting it
            "incident_location": location,
            "auto_make": auto_make,
            # "policy_number": policy_number,
            "months_as_customer": months_as_customer,
            "incident_date": incident_date,
            "total_claim_amount": total_claim_amount,
            # "policy_annual_premium": policy_annual_premium,
            # "umbrella_limit": umbrella_limit,
            # "witnesses": witnesses,
            # "bodily_injuries": bodily_injuries,
            # "property_damage": property_damage,
            "police_report_available": police_report_available,
            "incident_type": incident_type
        }


        # Convert the dictionary to a dataframe
        df_input = pd.DataFrame([inputs])

        # Apply feature engineering
        df_input = feature_engineering(df_input)
        
        selected_features = ['months_as_customer', 'age', 'auto_model', 'incident_severity']
        df_input = df_input[selected_features]

        # Encoding the categorical variables among the selected features
        label_encoders = {}
        for column in df_input.select_dtypes(include=['object']).columns:
            if column in label_encoders:
                df_input[column] = label_encoders[column].transform(df_input[column])


        # Drop the 'fraud_reported' column if it exists
        df_input = df_input.drop(columns=['fraud_reported'], errors='ignore')

        # Encode categorical variables after feature_engineering
        for column in df_input.select_dtypes(include=['object']).columns:
            le = LabelEncoder()
            df_input[column] = le.fit_transform(df_input[column])

        # Convert datetime columns to numerical representation after feature_engineering
        for col in df_input.columns:
            if df_input[col].dtype == 'datetime64[ns]':
                earliest_date = df_input[col].min()
                df_input[col] = (df_input[col] - earliest_date).dt.days

        # Scale the numerical variables with a StandardScaler after feature_engineering
        scaler = StandardScaler()
        df_input = scaler.fit_transform(df_input)

        if st.button("Predict"):
            # Choose the model for prediction
            model_options = ["Logistic Regression", "Gradient boosting", "Support Vector Machine", "Decison Tree"]
            selected_model = st.selectbox("Choose a Model", model_options)

            if selected_model == "Logistic Regression":
                predictor = joblib.load(os.path.join("resources/logistic_regression.pkl"))
            elif selected_model == "Gradient boosting":
                predictor = joblib.load(os.path.join("resources/gradient_boosting.pkl"))
            elif selected_model == "Decison Tree":
                predictor = joblib.load(os.path.join("resources/decision_tree.pkl"))
            elif selected_model == "Support Vector Machine":
                predictor = joblib.load(os.path.join("resources/svc.pkl"))

            # Make a prediction
            prediction = predictor.predict(df_input)

            st.success("The claim is predicted as: {}".format("Fraudulent" if prediction[0] == 1 else "Not Fraudulent"))


        # Check if a file is uploaded
        if uploaded_file is not None:
            with st.spinner("Uploading..."):
                # Read the uploaded CSV file
                df_test = pd.read_csv(uploaded_file)

                # Apply feature engineering to the uploaded data
                df_test = feature_engineering(df_test)
                df_test = df_test.drop(columns=['fraud_reported'], errors='ignore')

                # Encode categorical variables after feature_engineering
                for column in df_test.select_dtypes(include=['object']).columns:
                    le = LabelEncoder()
                    df_test[column] = le.fit_transform(df_test[column])

                # Convert datetime columns to numerical representation after feature_engineering
                for col in df_test.columns:
                    if df_test[col].dtype == 'datetime64[ns]':
                        earliest_date = df_test[col].min()
                        df_test[col] = (df_test[col] - earliest_date).dt.days

                # Scale the numerical variables with a StandardScaler after feature_engineering
                scaler = StandardScaler()
                df_test = scaler.fit_transform(df_test)

                # Drop the 'fraud_reported' column if it exists
                # df_test = df_test.drop(columns=['fraud_reported'], errors='ignore')

                # Display the processed test data
                st.subheader("Processed Test Data")
                st.dataframe(df_test)

                # Load your model and use it for prediction
                predictor = joblib.load(os.path.join("resources/logistic_regression.pkl"))
                prediction = predictor.predict(df_test)  # Ensure that your model can handle the processed dataframe as input
                
                # Assuming prediction contains multiple predictions
                predicted_labels = ["Fraudulent" if p == 1 else "Not Fraudulent" for p in prediction]
                predictions_string = ", ".join(predicted_labels)
                st.success(f"The claims are predicted as: {predictions_string}")


# Required to let Streamlit instantiate our web app.
if __name__ == '__main__':
    main()
