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

def feature_engineering(df):
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
    return data

# Display the refactored function
print(feature_engineering)
