from flask import Flask, jsonify, request, redirect, abort
from app.models import URLStore
from app.utils import generate_short_code, validate_url
from datetime import datetime

App = Flask(__name__)
url_store = URLStore()

@App.errorhandler(400)
def bad_request(error):
    return jsonify({"description": error.description}), 400

@App.errorhandler(404)
def not_found(error):
    return jsonify({"description": error.description}), 404

@App.errorhandler(500)
def internal_error(error):
    return jsonify({"description": error.description}), 500

@App.route('/')
def health_check():
    return jsonify({
        "status": "healthy",
        "service": "URL Shortener API"
    })

@App.route('/api/health')
def api_health():
    return jsonify({
        "status": "ok",
        "message": "URL Shortener API is running"
    })

@App.route('/api/shorten', methods=['POST'])
def shorten_url():
    data = request.get_json()
    if not data or 'url' not in data:
        abort(400, description="Missing 'url' in request body")
    
    long_url = data['url']
    if not validate_url(long_url):
        abort(400, description="Invalid URL")
    
    short_code = None
    attempts = 0
    max_attempts = 10
    while attempts < max_attempts:
        short_code = generate_short_code()
        if url_store.add_url(short_code, long_url):
            break
        attempts += 1
    if not short_code or attempts >= max_attempts:
        abort(500, description="Failed to generate unique short code")
    
    short_url = f"http://localhost:5000/{short_code}"
    return jsonify({
        "short_code": short_code,
        "short_url": short_url
    }), 201

@App.route('/<short_code>')
def redirect_url(short_code):
    url_data = url_store.get_url(short_code)
    if not url_data:
        abort(404, description="Short code not found")
    
    url_store.increment_clicks(short_code)
    return redirect(url_data['url'])

@App.route('/api/stats/<short_code>')
def get_stats(short_code):
    url_data = url_store.get_url(short_code)
    if not url_data:
        abort(404, description="Short code not found")
    
    return jsonify({
        "url": url_data['url'],
        "clicks": url_data['clicks'],
        "created_at": url_data['created_at'].isoformat()
    })

if __name__ == '__main__':
    App.run(host='0.0.0.0', port=5000, debug=True)