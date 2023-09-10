import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder

def handle_missing_values(data):
    """Handle placeholder values "?" in the dataframe."""
    print("Handling missing values...")
    # Columns where "?" should be converted to NaN
    numerical_columns_with_question_mark = ['total_claim_amount', 'witnesses']
    for col in numerical_columns_with_question_mark:
        data[col] = pd.to_numeric(data[col], errors='coerce')
    
    # Categorical columns where "?" can be treated as a separate category
    categorical_columns_with_question_mark = ['police_report_available', 'property_damage', 'collision_type']
    for col in categorical_columns_with_question_mark:
        data[col].replace("?", "Unknown", inplace=True)
    
    return data

def convert_to_datetime(data, columns):
    """Convert specified columns to datetime format."""
    for col in columns:
        data[col] = pd.to_datetime(data[col])
    return data

def generate_new_features(data):
    """Generate new features based on existing columns."""
    data["Contract Years"] = data["months_as_customer"] / 12
    data['total_premiums_paid'] = (data['policy_annual_premium'] / 12) * data['months_as_customer']
    data['net_value_of_customer'] = data['total_premiums_paid'] - data['total_claim_amount']
    data['days_since_policy_binding'] = (data['incident_date'] - data['policy_bind_date']).dt.days
    return data

def extract_date_parts(data, columns):
    """Extract month and day from specified date columns."""
    for col in columns:
        data[col + '_month'] = data[col].dt.month
        data[col + '_day'] = data[col].dt.day
    return data

def encode_columns(data, columns):
    """Label encode specified columns and create new encoded columns."""
    le = LabelEncoder()
    for col in columns:
        data[col + '_encoded'] = le.fit_transform(data[col])
    return data

# def feature_engineering(df):
    """Apply feature engineering transformations to the provided dataframe."""
    print("Starting feature engineering...")
    data = df.copy()

    # Handle placeholder values "?"
    data = handle_missing_values(data)

    # Convert specified columns to datetime format
    print("Converting date columns to datetime format...")
    data = convert_to_datetime(data, ['policy_bind_date', 'incident_date'])

    # Drop columns with all missing values
    print("Dropping columns with all missing values...")
    if '_c39' in data.columns:
        data.drop(columns=['_c39'], inplace=True)

    # Generate new features
    print("Generating new features...")
    data = generate_new_features(data)

    # Extract month and day from date columns
    data = extract_date_parts(data, ['policy_bind_date', 'incident_date'])

    # Drop the original date columns
    print("Dropping original date columns...")
    data.drop(['policy_bind_date', 'incident_date'], axis=1, inplace=True)

    # Label encoding for specified columns
    print("Encoding categorical columns...")
    data = encode_columns(data, ['auto_make', 'auto_model', 'incident_city', 'incident_severity'])

    print("Feature engineering completed!")
    print("Saving data to csv as insurance_laims_ata.csv")
    data.to_csv("./insurance_laims_ata.csv")
    print("csv file")
    return data

# def feature_engineering(df):
#     """
#     Apply feature engineering transformations to the provided dataframe.
    
#     Parameters:
#     - df: The dataframe to transform.
    
#     Returns:
#     - Transformed dataframe.
#     """
#     # Create a copy of the dataframe to avoid modifying the original one
#     data = df.copy()
#     data['fraud_satus'] = data['fraud_reported'].map({1: 'Fraud', 0: 'No Fraud'})
#     # data.columns.drop('fraud_reported')
    
#     # Convert 'policy_bind_date' and 'incident_date' to datetime
#     data['policy_bind_date'] = pd.to_datetime(data['policy_bind_date'])
#     data['incident_date'] = pd.to_datetime(data['incident_date'])
    
#     # Handling Missing Values
#     # Since the column '_c39' has all missing values, we can drop it
#     data.drop(columns=['_c39'], inplace=True)
    
#     # New columns
#     df["Contract Years"] = df["months_as_customer"]/12
#     df['total_premiums_paid'] = (df['policy_annual_premium']/12) * df['months_as_customer']
#     df['net_value_of_customer'] = df['total_premiums_paid'] - df['total_claim_amount']

    
#     # Calculate 'days_since_policy_binding' feature
#     data['days_since_policy_binding'] = (data['incident_date'] - data['policy_bind_date']).dt.days
    
#     # Extract the month and day from 'policy_bind_date' and 'incident_date'
#     data['policy_bind_month'] = data['policy_bind_date'].dt.month
#     data['policy_bind_day'] = data['policy_bind_date'].dt.day
#     data['incident_month'] = data['incident_date'].dt.month
#     data['incident_day'] = data['incident_date'].dt.day
    
#     # Convert the 'fraud_reported' column to numerical values
# #     data['fraud_reported'] = data['fraud_reported'].map({'Y': 1, 'N': 0})
    
#     # Drop the original 'policy_bind_date' and 'incident_date' columns
#     data.drop(['policy_bind_date', 'incident_date'], axis=1, inplace=True)
    
#     # Label encoding for columns you specified to retain their word values
#     columns_to_encode = ['auto_make', 'auto_model', 'incident_city', 'incident_severity']
    
#     for col in columns_to_encode:
#         le = LabelEncoder()
#         data[col + '_encoded'] = le.fit_transform(data[col])  # New encoded columns
    
#     return data


def feature_engineering(data):
    # Ensure columns exist before performing operations
    if 'policy_bind_date' in data.columns:
        # Convert 'policy_bind_date' to datetime
        data['policy_bind_date'] = pd.to_datetime(data['policy_bind_date'], errors='coerce')
    
    if 'incident_date' in data.columns:
        # Convert 'incident_date' to datetime
        data['incident_date'] = pd.to_datetime(data['incident_date'], errors='coerce')
    
    # Handling Missing Values
    if '_c39' in data.columns:
        data.drop(columns=['_c39'], inplace=True)

    # New columns
    if 'months_as_customer' in data.columns:
        data["Contract Years"] = pd.to_numeric(data["months_as_customer"], errors='coerce') / 12
    
    if 'policy_annual_premium' in data.columns and 'months_as_customer' in data.columns:
        data['total_premiums_paid'] = (pd.to_numeric(data['policy_annual_premium'], errors='coerce') / 12) * pd.to_numeric(data['months_as_customer'], errors='coerce')
    
    if 'total_premiums_paid' in data.columns and 'total_claim_amount' in data.columns:
        data['net_value_of_customer'] = pd.to_numeric(data['total_premiums_paid'], errors='coerce') - pd.to_numeric(data['total_claim_amount'], errors='coerce')

    # Calculate 'days_since_policy_binding' feature
    if 'incident_date' in data.columns and 'policy_bind_date' in data.columns:
        data['days_since_policy_binding'] = (data['incident_date'] - data['policy_bind_date']).dt.days
    
    # Extract the month and day from 'policy_bind_date' and 'incident_date'
    if 'policy_bind_date' in data.columns:
        data['policy_bind_month'] = data['policy_bind_date'].dt.month
        data['policy_bind_day'] = data['policy_bind_date'].dt.day
    
    if 'incident_date' in data.columns:
        data['incident_month'] = data['incident_date'].dt.month
        data['incident_day'] = data['incident_date'].dt.day
    
    # Convert the 'fraud_reported' column to numerical values
    # Ensure the column exists and contains the expected values
    if 'fraud_reported' in data.columns:
        unique_values = data['fraud_reported'].unique()
        if set(unique_values).issubset({'Y', 'N'}):
            data['fraud_reported'] = data['fraud_reported'].map({'Y': 1, 'N': 0})
    
    # Drop the original 'policy_bind_date' and 'incident_date' columns if they exist
    data.drop(['policy_bind_date', 'incident_date'], axis=1, errors='ignore', inplace=True)
    
    # Label encoding for columns you specified to retain their word values
    columns_to_encode = ['auto_make', 'auto_model', 'incident_city', 'incident_severity']
    for col in columns_to_encode:
        le = LabelEncoder()
        data[col + '_encoded'] = le.fit_transform(data[col])  # New encoded columns

    return data
