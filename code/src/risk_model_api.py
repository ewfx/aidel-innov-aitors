from flask import Flask, request, jsonify
import joblib  # For loading ML models
import numpy as np
import pandas as pd

# Initialize Flask app
app = Flask(__name__)

# Load the trained model
model = joblib.load("model.pkl")

# Define data preprocessing function
def preprocess_data(transaction):
    # Example preprocessing logic for the new dataset
    amount = float(transaction["Amount"].replace("$", "").replace(",", ""))

    # Encoding categorical data
    transaction_details_map = {"Software licensing fee": 0, "Invoice settlement": 1,
                               "Marketing campaign fee": 2, "Consulting fee": 3,
                               "Royalty payment": 4, "Equipment purchase": 5}
    receiver_country_map = {"Japan": 0, "France": 1, "India": 2, "USA": 3,
                            "Germany": 4, "Canada": 5}
    entity_type_map = {"Corporation": 0, "Non-Profit": 1, "Individual": 2,
                       "LLC": 3, "Government": 4}

    transaction_details = transaction_details_map.get(transaction["Transaction Details"], -1)
    receiver_country = receiver_country_map.get(transaction["Receiver Country"], -1)
    entity_type = entity_type_map.get(transaction["Entity Type"], -1)

    return np.array([[transaction_details, amount, receiver_country, entity_type]])

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Welcome to the Risk Scoring API!"})

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        features = preprocess_data(data)
        prediction = model.predict(features)
        return jsonify({"prediction": prediction.tolist()})
    except Exception as e:
        return jsonify({"error": str(e)})

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
