"""
Tests for protected pages that require authentication
These tests verify proper redirect behavior
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

def test_protected_pages_redirect(client):
    """Test that protected pages redirect to login"""
    protected_pages = [
        '/dashboard',
        '/groups',
        '/resources',
        '/events', 
        '/profile',
        '/create_group',
        '/upload_resource',
        '/create_event'
    ]
    
    for page in protected_pages:
        # Test without following redirect (should be 302)
        response = client.get(page) if page.startswith('/create') else client.get(page)
        assert response.status_code == 302, f"Page {page} should redirect (302)"
        
        # Test following redirect (should go to login)
        response = client.get(page, follow_redirects=True) if page.startswith('/create') else client.get(page, follow_redirects=True)
        assert response.status_code == 200, f"Page {page} redirect should work"
        assert b'Login' in response.data, f"Page {page} should redirect to login"

def test_post_protected_pages_redirect(client):
    """Test that POST to protected endpoints redirect to login"""
    protected_endpoints = [
        ('/create_group', {'group_name': 'Test', 'description': 'Test'}),
        ('/upload_resource', {'title': 'Test', 'description': 'Test', 'resource_type': 'note'}),
        ('/create_event', {'title': 'Test', 'description': 'Test', 'event_date': '2024-12-31T18:00', 'location': 'Test'})
    ]
    
    for endpoint, data in protected_endpoints:
        response = client.post(endpoint, data=data, follow_redirects=True)
        assert response.status_code == 200
        assert b'Login' in response.data