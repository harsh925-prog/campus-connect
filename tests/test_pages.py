"""
Test page accessibility
"""
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_pages():
    print("🌐 Testing Page Accessibility")
    print("-" * 30)
    
    try:
        from app import app
        
        with app.test_client() as client:
            # Public pages - should return 200
            public_pages = [
                ('/', 'Campus Connect'),
                ('/login', 'Login'),
                ('/register', 'Register')
            ]
            
            for url, content in public_pages:
                response = client.get(url)
                status = "✅" if response.status_code == 200 else "❌"
                print(f"{status} {url} - Status: {response.status_code}")
            
            print("\n🔐 Testing Protected Pages (should redirect)")
            print("-" * 40)
            
            # Protected pages - should return 302 (redirect)
            protected_pages = ['/dashboard', '/groups', '/resources', '/events', '/profile']
            
            for url in protected_pages:
                response = client.get(url, follow_redirects=False)
                status = "✅" if response.status_code == 302 else "❌"
                print(f"{status} {url} - Status: {response.status_code} (should be 302)")
                
    except Exception as e:
        print(f"❌ Error testing pages: {e}")

if __name__ == '__main__':
    test_pages()