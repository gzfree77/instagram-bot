from flask import Blueprint, request, jsonify
# import openai  # Commented out for now - will be used when OpenAI integration is needed
import os
import json
from datetime import datetime
from flask import current_app
from src.models.user import db

content_bp = Blueprint('content', __name__)

# OpenAI API configuration
# Note: In production, this should be set as an environment variable
# openai.api_key = os.getenv('OPENAI_API_KEY')

def create_prompt(product_data, output_language, content_tone):
    """
    Create an intelligent prompt for OpenAI based on Persian input
    """
    
    # Language mapping
    language_map = {
        'arabic': 'Arabic',
        'english': 'English',
        'both': 'both Arabic and English'
    }
    
    # Tone mapping
    tone_map = {
        'formal': 'formal and professional',
        'promotional': 'promotional and marketing-focused',
        'luxury': 'luxury and premium',
        'friendly': 'friendly and approachable'
    }
    
    target_language = language_map.get(output_language, 'Arabic')
    target_tone = tone_map.get(content_tone, 'professional')
    
    prompt = f"""
You are an expert Instagram content creator specializing in luxury stone and construction materials for the Middle Eastern and international markets.

Create Instagram content in {target_language} with a {target_tone} tone for the following stone product:

Product Details (in Persian):
- Name: {product_data.get('name', '')}
- Type: {product_data.get('type', '')}
- Color: {product_data.get('color', '')}
- Usage: {product_data.get('usage', '')}
- Features: {product_data.get('features', '')}
- Origin Country: {product_data.get('originCountry', '')}

Please provide:
1. A catchy post title (max 50 characters)
2. An engaging Instagram caption (max 150 characters, suitable for Instagram posts)
3. 6-8 relevant hashtags (mix of industry-specific, regional, and trending hashtags)

Requirements:
- Content should appeal to architects, interior designers, and luxury construction market
- Include emotional appeal and quality emphasis
- Use appropriate emojis sparingly
- Hashtags should include stone industry, architecture, interior design, and regional market terms
- If Arabic: use proper Arabic grammar and terminology
- If English: use international English suitable for global audience
- If both languages: provide separate versions for each language

Format your response as JSON:
{{
    "title": "post title here",
    "caption": "caption text here", 
    "hashtags": ["hashtag1", "hashtag2", "hashtag3", "hashtag4", "hashtag5", "hashtag6"]
}}
"""
    
    return prompt

def generate_mock_content(product_data, output_language, content_tone):
    """
    Generate mock content for testing when OpenAI API is not available
    """
    
    # Mock content based on language and tone
    if output_language == 'arabic':
        if content_tone == 'luxury':
            return {
                "title": "رخام كرارا الفاخر الأصلي",
                "caption": "اكتشف جمال الرخام الإيطالي الأصلي ✨ جودة استثنائية وتصميم فريد لمساحاتك الفاخرة",
                "hashtags": ["#رخام_إيطالي", "#حجر_طبيعي", "#تصميم_داخلي", "#فخامة", "#معمار", "#ديكور_فاخر"]
            }
        else:
            return {
                "title": "رخام كرارا عالي الجودة",
                "caption": "رخام إيطالي أصلي بجودة عالية ومتانة فائقة. مثالي للأرضيات والجدران",
                "hashtags": ["#رخام", "#حجر_بناء", "#تصميم", "#جودة", "#إيطاليا", "#بناء"]
            }
    
    elif output_language == 'english':
        if content_tone == 'luxury':
            return {
                "title": "Premium Carrara Marble Collection",
                "caption": "Experience unparalleled beauty with authentic Italian marble ✨ Premium quality for your luxury spaces",
                "hashtags": ["#CarraraMarble", "#LuxuryStone", "#InteriorDesign", "#PremiumMaterials", "#Architecture", "#LuxuryHomes"]
            }
        else:
            return {
                "title": "High-Quality Carrara Marble",
                "caption": "Authentic Italian marble with superior quality and durability. Perfect for floors and walls",
                "hashtags": ["#Marble", "#NaturalStone", "#Construction", "#Quality", "#Italian", "#Building"]
            }
    
    else:  # both languages
        return {
            "title_arabic": "رخام كرارا الفاخر",
            "title_english": "Premium Carrara Marble",
            "caption_arabic": "اكتشف جمال الرخام الإيطالي الأصلي ✨ جودة استثنائية لمساحاتك الفاخرة",
            "caption_english": "Experience authentic Italian marble beauty ✨ Premium quality for luxury spaces",
            "hashtags": ["#رخام_إيطالي", "#CarraraMarble", "#تصميم_داخلي", "#InteriorDesign", "#فخامة", "#LuxuryStone"]
        }

@content_bp.route('/generate-content', methods=['POST'])
def generate_content():
    """
    Generate Instagram content based on product information
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['productData', 'outputLanguage', 'contentTone']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        product_data = data['productData']
        output_language = data['outputLanguage']
        content_tone = data['contentTone']
        
        # Validate product data has at least name
        if not product_data.get('name'):
            return jsonify({'error': 'Product name is required'}), 400
        
        # Save or get product from database
        from src.models.content import Product, GeneratedContent
        
        product = Product.query.filter_by(name=product_data.get('name')).first()
        if not product:
            product = Product(
                name=product_data.get('name', ''),
                type=product_data.get('type', ''),
                color=product_data.get('color', ''),
                usage=product_data.get('usage', ''),
                features=product_data.get('features', ''),
                origin_country=product_data.get('originCountry', '')
            )
            db.session.add(product)
            db.session.commit()
        
        # For now, use mock content generation
        # In production, uncomment the OpenAI integration below
        
        # Mock content generation
        generated_content = generate_mock_content(product_data, output_language, content_tone)
        
        # Save generated content to database
        content_record = GeneratedContent(
            product_id=product.id,
            output_language=output_language,
            content_tone=content_tone,
            title=generated_content.get('title', ''),
            caption=generated_content.get('caption', ''),
            hashtags=json.dumps(generated_content.get('hashtags', []))
        )
        db.session.add(content_record)
        db.session.commit()
        
        # OpenAI integration (commented out for now)
        """
        try:
            prompt = create_prompt(product_data, output_language, content_tone)
            
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert Instagram content creator for luxury construction materials."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.7
            )
            
            # Parse the JSON response from OpenAI
            import json
            generated_content = json.loads(response.choices[0].message.content)
            
        except Exception as openai_error:
            return jsonify({'error': f'OpenAI API error: {str(openai_error)}'}), 500
        """
        
        # Add metadata
        result = {
            'content': generated_content,
            'metadata': {
                'generated_at': datetime.now().isoformat(),
                'language': output_language,
                'tone': content_tone,
                'product_name': product_data.get('name'),
                'content_id': content_record.id,
                'product_id': product.id
            }
        }
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@content_bp.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint
    """
    return jsonify({
        'status': 'healthy',
        'service': 'Instagram Content Generator API',
        'timestamp': datetime.now().isoformat()
    }), 200


@content_bp.route('/content-history', methods=['GET'])
def get_content_history():
    """
    Get history of generated content
    """
    try:
        from src.models.content import GeneratedContent
        
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        # Query with pagination
        contents = GeneratedContent.query.order_by(GeneratedContent.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        result = {
            'contents': [content.to_dict() for content in contents.items],
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': contents.total,
                'pages': contents.pages,
                'has_next': contents.has_next,
                'has_prev': contents.has_prev
            }
        }
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@content_bp.route('/products', methods=['GET'])
def get_products():
    """
    Get list of all products
    """
    try:
        from src.models.content import Product
        
        products = Product.query.order_by(Product.created_at.desc()).all()
        result = {
            'products': [product.to_dict() for product in products]
        }
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@content_bp.route('/products/<int:product_id>/contents', methods=['GET'])
def get_product_contents(product_id):
    """
    Get all generated content for a specific product
    """
    try:
        from src.models.content import Product, GeneratedContent
        
        product = Product.query.get_or_404(product_id)
        contents = GeneratedContent.query.filter_by(product_id=product_id).order_by(GeneratedContent.created_at.desc()).all()
        
        result = {
            'product': product.to_dict(),
            'contents': [content.to_dict() for content in contents]
        }
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

