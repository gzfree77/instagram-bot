from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    msg = {"message": "ربات تولید محتوا فعال است!"}
    return Response(json.dumps(msg, ensure_ascii=False), mimetype="application/json")

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

        content = f"{name} یک سنگ {color} از {origin} است که برای {usage} بسیار مناسب می‌باشد. ویژگی‌ها: {features}. لحن محتوا: {tone}، زبان: {lang}"

        return Response(json.dumps({"generatedContent": content}, ensure_ascii=False), mimetype="application/json")
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
