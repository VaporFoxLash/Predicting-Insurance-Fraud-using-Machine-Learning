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

# Data dependencies
import pandas as pd

# Load your raw data
url = "https://raw.githubusercontent.com/Explore-AI/Public-Data/master/insurance_claims.csv"
raw = pd.read_csv(url)
# raw = pd.read_csv("resources/insurance_claims.csv")

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

    # Building out the prediction page
    if selection == "Prediction":
        st.info("Predict if a claim is fraudulent")
        # Sample input features for prediction can be added here
        claim_amount = st.text_input("Total Claim Amount")
        # Additional features can be added

        if st.button("Classify"):
            # Process input data and make prediction here
            # Load your .pkl model file for fraud detection
            predictor = joblib.load(open(os.path.join("resources/insurance_fraud_detection_model.pkl"), "rb"))
            # Replace below with processing and prediction logic
            prediction = predictor.predict([[claim_amount]])  # This should be adjusted based on model's requirements
            st.success("The claim is predicted as: {}".format("Fraudulent" if prediction[0] == 1 else "Not Fraudulent"))

# Required to let Streamlit instantiate our web app.  
if __name__ == '__main__':
    main()
