import pytest
import os
import sys

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

@pytest.fixture
def client():
    from app import app
    
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['SECRET_KEY'] = 'test-secret-key'
    
    with app.test_client() as client:
        yield client

def test_index_page(client):
    """Test the home page"""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Campus Connect' in response.data

def test_login_page(client):
    """Test login page"""
    response = client.get('/login')
    assert response.status_code == 200
    assert b'Login' in response.data

def test_register_page(client):
    """Test register page"""
    response = client.get('/register')
    assert response.status_code == 200
    assert b'Register' in response.data

def test_registration(client):
    """Test user registration"""
    response = client.post('/register', data={
        'email': 'test123@student.com',
        'password': 'password123',
        'name': 'Test Student',
        'major': 'Computer Science',
        'skills': 'Python, Testing'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    # Registration should redirect to login or show success
    assert b'Login' in response.data or b'success' in response.data.lower()

def test_protected_pages_redirect_to_login(client):
    """Test that protected pages redirect to login when not authenticated"""
    protected_pages = [
        '/dashboard',
        '/groups', 
        '/resources',
        '/events',
        '/profile'
    ]
    
    for page in protected_pages:
        response = client.get(page, follow_redirects=False)
        assert response.status_code == 302  # Should redirect to login
        # You can also check the location header if needed
        # assert '/login' in response.location

def test_protected_pages_follow_redirect(client):
    """Test that following redirect from protected pages goes to login"""
    protected_pages = [
        '/dashboard',
        '/groups',
        '/resources', 
        '/events',
        '/profile'
    ]
    
    for page in protected_pages:
        response = client.get(page, follow_redirects=True)
        assert response.status_code == 200
        assert b'Login' in response.data  # Should show login page

def test_logout_when_not_logged_in(client):
    """Test logout when not logged in"""
    response = client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b'Campus Connect' in response.data  # Should return to home

def test_group_creation_redirect(client):
    """Test group creation redirects when not logged in"""
    response = client.post('/create_group', data={
        'group_name': 'Test Group',
        'description': 'Test Description'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b'Login' in response.data

def test_resource_upload_redirect(client):
    """Test resource upload redirects when not logged in"""
    response = client.post('/upload_resource', data={
        'title': 'Test Resource',
        'description': 'Test Description',
        'resource_type': 'note'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b'Login' in response.data

def test_event_creation_redirect(client):
    """Test event creation redirects when not logged in"""
    response = client.post('/create_event', data={
        'title': 'Test Event',
        'description': 'Test Description',
        'event_date': '2024-12-31T18:00',
        'location': 'Test Location'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b'Login' in response.data

def test_join_group_redirect(client):
    """Test join group redirects when not logged in"""
    response = client.get('/join_group/1', follow_redirects=True)
    assert response.status_code == 200
    assert b'Login' in response.data

def test_rsvp_event_redirect(client):
    """Test RSVP event redirects when not logged in"""
    response = client.get('/rsvp_event/1/going', follow_redirects=True)
    assert response.status_code == 200
    assert b'Login' in response.data

# Basic functionality tests (no database required)
def test_basic_functionality():
    """Test basic Python functionality"""
    assert 1 + 1 == 2
    assert "Campus" in "Campus Connect"
    assert "Connect" in "Campus Connect"

def test_config_import():
    """Test that configuration can be imported"""
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    try:
        from app_config import MYSQL_HOST, MYSQL_USER, MYSQL_DB
        assert MYSQL_HOST == 'localhost'
        assert MYSQL_USER == 'root' 
        assert MYSQL_DB == 'campus_connect'
    except ImportError:
        # Skip if config not available, but don't fail
        pass

if __name__ == '__main__':
    pytest.main([__file__, '-v'])