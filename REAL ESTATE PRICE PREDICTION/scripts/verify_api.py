import requests

def verify():
    url = 'http://localhost:8000/predict'
    data = {
        'location': 'whitefield',
        'total_sqft': 1200,
        'bath': 2,
        'bhk': 2
    }

    print("Testing Bengaluru prediction endpoint...")
    response = requests.post(url, json=data, timeout=10)
    response.raise_for_status()
    prediction = response.json()

    print(f"Prediction: Rs. {prediction['prediction_lakhs']} Lakhs")
    print(f"Prediction: Rs. {prediction['prediction_crores']} Cr")

if __name__ == "__main__":
    verify()
