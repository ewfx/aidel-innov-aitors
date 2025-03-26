import requests
import json

class RiskScorer:
    def __init__(self, api_url="http://127.0.0.1:5000/predict"):
        self.api_url = api_url

    def run(self, transaction_data):
        try:
            headers = {'Content-Type': 'application/json'}
            response = requests.post(self.api_url, json=transaction_data, headers=headers)
            response_data = response.json()

            if "prediction" in response_data:
                return response_data["prediction"]
            else:
                return f"Error: {response_data.get('error', 'Unknown error occurred')}"
        except Exception as e:
            return f"Exception occurred: {str(e)}"

# Example usage
if __name__ == "__main__":
    predictor = RiskScorer()

    transaction = {
        "Transaction Details": "Invoice settlement",
        "Amount": "$322000",
        "Receiver Country": "India",
        "Entity Type": "Non-Profit"
    }

    result = predictor.run(transaction)
    print(f"Prediction: {result}")
