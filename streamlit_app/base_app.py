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
        age = st.text_input("Age")
        
        genders = ["Select Gender", "Male", "Female"]
        gender = st.selectbox("Gender", genders)
        
        fraud_options = ["Option","Yes", "No"]
        police_report = st.selectbox("Police report available?", fraud_options)
        
        fraud_reported = st.selectbox("Fraud reported?", fraud_options)
        
        location = st.text_input("Location")
        
        vehicle_make = st.text_input("Vehicle make")
        
        policy_number = st.text_input("Policy number")
        
        number_of_months = st.text_input("months_as_customer")
        
        incident_date = st.text_input("incident date")
        
        claim_amount = st.text_input("Total Claim Amount")
        
        
        # Check if a file is uploaded
        if uploaded_file is not None:
            with st.spinner("Uploading..."):
                # Read the uploaded CSV file
                df_test = pd.read_csv(uploaded_file)
                
                # Apply feature engineering to the uploaded data
                df_test = feature_engineering(df_test)
                
                df_test = df_test.drop(columns=['fraud_reported'], errors='ignore')

                # Display the processed test data
                st.subheader("Processed Test Data")
                st.dataframe(df_test)

                # Load your model and use it for prediction
                predictor = joblib.load(os.path.join("resources/logistic_regression.pkl"))
                prediction = predictor.predict(df_test)  # Ensure that your model can handle the processed dataframe as input
                
                st.success("The claim is predicted as: {}".format("Fraudulent" if prediction[0] == 1 else "Not Fraudulent"))

        # if st.button("Make a prediction"):
        #     # Process input data and make prediction here
        #     # Load your .pkl model file for fraud detection
        #     predictor = joblib.load(open(os.path.join("resources/logistic_regression.pkl"), "rb"))
        #     # Replace below with processing and prediction logic
        #     prediction = predictor.predict([[claim_amount, age, police_report, fraud_reported, location, vehicle_make, policy_number, number_of_months, incident_date, gender]])  # This should be adjusted based on model's requirements
        #     st.success("The claim is predicted as: {}".format("Fraudulent" if prediction[0] == 1 else "Not Fraudulent"))
        # Load the encoding function from the pickled file
        with open("resources/encode_function.pkl", "rb") as f:
            encode_columns = pickle.load(f)

        # Assuming you also pickled the encoders, load them
        with open("encoders.pkl", "rb") as f:
            encoders = pickle.load(f)

        # Define a function to process and encode the user inputs
        def process_input_data(inputs, encoders):
            # Create a DataFrame from the inputs
            df = pd.DataFrame([inputs], columns=inputs.keys())
            
            # Encode the categorical variables using the loaded encoders
            for col, encoder in encoders.items():
                df[col] = encoder.transform(df[col])
            
            return df

        # Inside the 'if st.button("Make a prediction"):' block:
        if st.button("Make a prediction"):
        # Convert user inputs to a dictionary
            inputs = {
                "Age": age,
                "Gender": gender,
                "Police report available?": police_report,
                "Fraud reported?": fraud_reported,
                "Location": location,
                "Vehicle make": vehicle_make,
                "Policy number": policy_number,
                "months_as_customer": number_of_months,
                "incident date": incident_date,
                "Total Claim Amount": claim_amount
            }
            
            # Process and encode the inputs
            processed_data = process_input_data(inputs, encoders)
            
            # Load the logistic regression model
            predictor = joblib.load(os.path.join("resources/logistic_regression.pkl"))
            
            # Make a prediction
            prediction = predictor.predict(processed_data)  # Adjust based on model's requirements
            
            st.success("The claim is predicted as: {}".format("Fraudulent" if prediction[0] == 1 else "Not Fraudulent"))

# Required to let Streamlit instantiate our web app.  
if __name__ == '__main__':
    main()
