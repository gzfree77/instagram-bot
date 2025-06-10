import requests
import json

# Test the content generation API
def test_content_generation():
    url = "https://instagram-bot-y86e.onrender.com/api/generate-content"

    
    test_data = {
        "productData": {
            "name": "مرمر کرارا",
            "type": "مرمر",
            "color": "سفید",
            "usage": "کف و دیوار",
            "features": "مقاوم در برابر آب، براق، ضد لک",
            "originCountry": "ایتالیا"
        },
        "outputLanguage": "arabic",
        "contentTone": "luxury"
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(url, data=json.dumps(test_data), headers=headers)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    print("Testing Content Generation API...")
    success = test_content_generation()
    print(f"Test {'PASSED' if success else 'FAILED'}")

