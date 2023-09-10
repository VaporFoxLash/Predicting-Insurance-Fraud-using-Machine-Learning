"""
    Simple file to create a sklearn model for deployment in our API

    Author: Explore Data Science Academy

    Description: This script is responsible for training a simple linear
    regression model which is used within the API for initial demonstration
    purposes.

"""

# Dependencies
import pandas as pd
import pickle
from sklearn.linear_model import LinearRegression

# Fetch training data and preprocess for modeling
url = "https://raw.githubusercontent.com/Explore-AI/Public-Data/master/insurance_claims.csv"
train = pd.read_csv(url)
# train = pd.read_csv('./data/df_train.csv')

# Spplit data into X and Y train
y_train = train[['fraud_reported']]
X_train = train[['fraud_reported']]

# Fit model
lm_regression = LinearRegression(normalize=True)
print ("Training Model...")
lm_regression.fit(X_train, y_train)

# Pickle model for use within our API
save_path = '../assets/trained-models/lm_model.pkl'
print (f"Training completed. Saving model to: {save_path}")
pickle.dump(lm_regression, open(save_path,'wb'))
