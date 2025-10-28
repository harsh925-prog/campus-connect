"""
Tests for public pages that don't require authentication
"""
import pytest
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

@pytest.fixture
def client():
    from app import app
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    with app.test_client() as client:
        yield client

def test_public_pages(client):
    """Test all public pages that should be accessible without login"""
    public_pages = [
        ('/', 'Campus Connect'),
        ('/login', 'Login'),
        ('/register', 'Register')
    ]
    
    for url, expected_content in public_pages:
        response = client.get(url)
        assert response.status_code == 200, f"Page {url} should be accessible"
        assert expected_content.encode() in response.data, f"Page {url} should contain {expected_content}"

def test_homepage_content(client):
    """Test specific homepage content"""
    response = client.get('/')
    assert response.status_code == 200
    # Check for key phrases that should be on homepage
    assert b'Campus Connect' in response.data
    assert b'student' in response.data.lower() or b'collaboration' in response.data.lower()

def test_login_form_exists(client):
    """Test that login form is present"""
    response = client.get('/login')
    assert response.status_code == 200
    assert b'form' in response.data.lower()
    assert b'email' in response.data.lower()
    assert b'password' in response.data.lower()

def test_register_form_exists(client):
    """Test that register form is present"""
    response = client.get('/register')
    assert response.status_code == 200
    assert b'form' in response.data.lower()
    assert b'name' in response.data.lower()
    assert b'email' in response.data.lower()
    