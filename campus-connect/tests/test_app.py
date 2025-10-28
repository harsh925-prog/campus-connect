import pytest
import os
import sys
from app import app, mysql
from flask import url_for
import bcrypt

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    with app.test_client() as client:
        with app.app_context():
            # Initialize test database
            init_test_database()
        yield client

def init_test_database():
    """Initialize test database with sample data"""
    try:
        cursor = mysql.connection.cursor()
        
        # Clear existing test data
        cursor.execute("DELETE FROM rsvps")
        cursor.execute("DELETE FROM group_members")
        cursor.execute("DELETE FROM resources")
        cursor.execute("DELETE FROM events")
        cursor.execute("DELETE FROM project_groups")
        cursor.execute("DELETE FROM students")
        
        # Insert test users
        hashed_password = bcrypt.hashpw('password123'.encode('utf-8'), bcrypt.gensalt())
        cursor.execute(
            "INSERT INTO students (student_id, email, password_hash, name, major, skills) VALUES (%s, %s, %s, %s, %s, %s)",
            (1, 'test@student.com', hashed_password, 'Test Student', 'Computer Science', 'Python, Java')
        )
        
        cursor.execute(
            "INSERT INTO students (student_id, email, password_hash, name, major, skills) VALUES (%s, %s, %s, %s, %s, %s)",
            (2, 'john@student.com', hashed_password, 'John Doe', 'Mathematics', 'Calculus, Statistics')
        )
        
        # Insert test groups
        cursor.execute(
            "INSERT INTO project_groups (group_id, group_name, description, created_by) VALUES (%s, %s, %s, %s)",
            (1, 'Web Development Team', 'Building web applications', 1)
        )
        
        # Insert test resources
        cursor.execute(
            "INSERT INTO resources (resource_id, title, description, resource_type, uploaded_by) VALUES (%s, %s, %s, %s, %s)",
            (1, 'Python Notes', 'Comprehensive Python programming notes', 'note', 1)
        )
        
        mysql.connection.commit()
        cursor.close()
        
    except Exception as e:
        print(f"Error initializing test database: {e}")

def test_index_page(client):
    """Test the home page"""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Campus Connect' in response.data

def test_registration(client):
    """Test user registration"""
    response = client.post('/register', data={
        'email': 'new@student.com',
        'password': 'newpassword123',
        'name': 'New Student',
        'major': 'Physics',
        'skills': 'Physics, Math'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    # Should redirect to login after successful registration
    assert b'Login' in response.data or b'success' in response.data

def test_login_logout(client):
    """Test user login and logout"""
    # Login
    response = client.post('/login', data={
        'email': 'test@student.com',
        'password': 'password123'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b'Dashboard' in response.data or b'success' in response.data
    
    # Logout
    response = client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b'Login' in response.data

def test_dashboard_access(client):
    """Test dashboard access for authenticated user"""
    # Login first
    client.post('/login', data={
        'email': 'test@student.com',
        'password': 'password123'
    })
    
    # Access dashboard
    response = client.get('/dashboard')
    assert response.status_code == 200
    assert b'Welcome' in response.data

def test_group_creation(client):
    """Test creating a new group"""
    # Login first
    client.post('/login', data={
        'email': 'test@student.com',
        'password': 'password123'
    })
    
    # Create group
    response = client.post('/create_group', data={
        'group_name': 'Test Group',
        'description': 'This is a test group'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b'Test Group' in response.data or b'success' in response.data

def test_resource_upload(client):
    """Test uploading a resource"""
    # Login first
    client.post('/login', data={
        'email': 'test@student.com',
        'password': 'password123'
    })
    
    # Upload resource
    response = client.post('/upload_resource', data={
        'title': 'Test Resource',
        'description': 'This is a test resource',
        'resource_type': 'note'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b'Test Resource' in response.data or b'success' in response.data

if __name__ == '__main__':
    pytest.main([__file__, '-v'])