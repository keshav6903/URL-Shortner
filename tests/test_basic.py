import pytest
from app.main import App, url_store

@pytest.fixture
def client():
    App.config['TESTING'] = True
    with App.test_client() as client:
        yield client

def test_health_check(client):
    response = client.get('/')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'healthy'
    assert data['service'] == 'URL Shortener API'

def test_shorten_url_valid(client):
    response = client.post('/api/shorten', json={'url': 'https://www.example.com'})
    assert response.status_code == 201
    data = response.get_json()
    assert 'short_code' in data
    assert 'short_url' in data
    assert len(data['short_code']) == 6
    assert data['short_url'].startswith('http://localhost:5000/')

def test_shorten_url_invalid(client):
    response = client.post('/api/shorten', json={'url': 'invalid-url'})
    assert response.status_code == 400
    data = response.get_json()
    assert 'description' in data
    assert data['description'] == 'Invalid URL'

def test_shorten_url_missing(client):
    response = client.post('/api/shorten', json={})
    assert response.status_code == 400
    data = response.get_json()
    assert 'description' in data
    assert data['description'] == "Missing 'url' in request body"

def test_redirect_valid(client):
    # Use the shorten endpoint to create a URL
    response = client.post('/api/shorten', json={'url': 'https://www.example.com'})
    assert response.status_code == 201
    short_code = response.get_json()['short_code']
    
    response = client.get(f'/{short_code}', follow_redirects=False)
    assert response.status_code == 302
    assert response.location == 'https://www.example.com'
    assert url_store.get_url(short_code)['clicks'] == 1

def test_redirect_invalid(client):
    response = client.get('/invalid', follow_redirects=False)
    assert response.status_code == 404
    data = response.get_json()
    assert 'description' in data
    assert data['description'] == 'Short code not found'

def test_stats_valid(client):
    
    response = client.post('/api/shorten', json={'url': 'https://www.example.com'})
    assert response.status_code == 201
    short_code = response.get_json()['short_code']
    client.get(f'/{short_code}', follow_redirects=False)
    
    response = client.get(f'/api/stats/{short_code}')
    assert response.status_code == 200
    data = response.get_json()
    assert data['url'] == 'https://www.example.com'
    assert data['clicks'] == 1
    assert 'created_at' in data

def test_stats_invalid(client):
    response = client.get('/api/stats/invalid')
    assert response.status_code == 404
    data = response.get_json()
    assert 'description' in data
    assert data['description'] == 'Short code not found'