import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import joblib

# Sample dataset with more training data
data = pd.DataFrame({
    "Transaction Details": ["Software licensing fee", "Invoice settlement", "Marketing campaign fee", "Software licensing fee", "Consulting fee", "Royalty payment", "Equipment purchase"],
    "Amount": ["$428000", "$476000", "$268000", "$445000", "$390000", "$520000", "$310000"],
    "Receiver Country": ["Japan", "France", "India", "France", "USA", "Germany", "Canada"],
    "Entity Type": ["Corporation", "Non-Profit", "Corporation", "Individual", "LLC", "Corporation", "Government"],
    "Risk Score": [0.58, 0.8, 0.29, 0.17, 0.35, 0.75, 0.2]
})

# Clean and convert Amount column to numeric
data["Amount"] = data["Amount"].replace({'\\$': '', ',': ''}, regex=True).astype(float)

# Encode categorical variables
categorical_cols = ["Transaction Details", "Receiver Country", "Entity Type"]
label_encoders = {}
for col in categorical_cols:
    le = LabelEncoder()
    data[col] = le.fit_transform(data[col])
    label_encoders[col] = le

# Standardize numerical features
scaler = StandardScaler()
data["Amount"] = scaler.fit_transform(data[["Amount"]])

# Split dataset into training and test sets
X = data.drop(columns=["Risk Score"])
y = data["Risk Score"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestRegressor()
model.fit(X_train, y_train)

# Function to process a single transaction
def process_transaction(transaction):
    df = pd.DataFrame([transaction])
    
    # Clean Amount value
    df["Amount"] = df["Amount"].replace({'\\$': '', ',': ''}, regex=True).astype(float)
    
    # Encode categorical variables
    for col in categorical_cols:
        if transaction[col] in label_encoders[col].classes_:
            df[col] = label_encoders[col].transform([transaction[col]])[0]
        else:
            df[col] = -1  # Assign unknown category
    
    # Standardize amount
    df["Amount"] = scaler.transform(df[["Amount"]])
    
    # Ensure the feature names match
    df = df[X_train.columns]
    
    # Predict risk score
    risk_score = model.predict(df)[0]
    return round(float(risk_score), 2)  # Return risk score rounded to two decimal places

# # Example transaction
# transaction = {
#     "Transaction Details": "Invoice settlement",
#     "Amount": "$322000",
#     "Receiver Country": "India",
#     "Entity Type": "Non-Profit"
# }

# # Example usage
# predicted_risk_score = process_transaction(transaction)
# print(f"Predicted Risk Score: {predicted_risk_score}")

joblib.dump(model, 'model.pkl', protocol=4)