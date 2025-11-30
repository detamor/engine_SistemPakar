"""
Test script untuk menguji endpoint diagnosis
"""
import requests
import json

url = "http://localhost:8001/api/diagnose"

data = {
    "diagnosis_id": 999,
    "plant_id": 1,
    "symptoms": [
        {"symptom_id": 1, "user_cf": 0.8},
        {"symptom_id": 2, "user_cf": 0.6}
    ],
    "diseases_data": [
        {
            "id": 1,
            "name": "Test Disease",
            "description": "Test",
            "cause": "",
            "solution": "",
            "prevention": "",
            "symptoms": [
                {"symptom_id": 1, "certainty_factor": 0.9},
                {"symptom_id": 2, "certainty_factor": 0.7}
            ]
        }
    ]
}

print("Testing endpoint:", url)
print("Request data:", json.dumps(data, indent=2))

try:
    response = requests.post(url, json=data, timeout=30)
    print(f"\nStatus Code: {response.status_code}")
    print(f"Response Headers: {dict(response.headers)}")
    print(f"Response Body: {response.text[:500]}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"\nSuccess: {result.get('success')}")
        print(f"Data keys: {list(result.get('data', {}).keys())}")
    else:
        print(f"Error: {response.text}")
except Exception as e:
    print(f"Error: {e}")


