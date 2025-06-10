from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return jsonify({"message": "ربات تولید محتوای اینستاگرام فعال است!"})

@app.route('/api/generate-content', methods=['POST'])
def generate_content():
    try:
        data = request.get_json()

        product = data.get('productData', {})
        tone = data.get('contentTone', 'normal')
        lang = data.get('outputLanguage', 'farsi')

        name = product.get('name', '')
        color = product.get('color', '')
        usage = product.get('usage', '')
        origin = product.get('originCountry', '')
        features = product.get('features', '')

        content = f"{name} یک سنگ {color} از {origin} است که برای {usage} بسیار مناسب می‌باشد. ویژگی‌ها: {features}. لحن: {tone}، زبان خروجی: {lang}"

        return jsonify({"generatedContent": content})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


