import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_basic():
    """Basic test without Flask app context"""
    print("🧪 Running basic tests...")
    
    # Test 1: Check if config exists
    try:
        from app_config import MYSQL_HOST, MYSQL_USER, MYSQL_DB
        print("✅ Config import successful")
    except ImportError as e:
        print(f"❌ Config import failed: {e}")
        return False
    
    # Test 2: Check if app can be imported
    try:
        from app import app
        print("✅ App import successful")
    except ImportError as e:
        print(f"❌ App import failed: {e}")
        return False
    
    # Test 3: Test app configuration
    try:
        with app.test_client() as client:
            response = client.get('/')
            assert response.status_code == 200
            print("✅ Homepage accessible")
    except Exception as e:
        print(f"❌ App test failed: {e}")
        return False
    
    print("🎉 All basic tests passed!")
    return True

if __name__ == '__main__':
    test_basic()