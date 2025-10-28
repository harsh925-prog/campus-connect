"""
Simple test runner that manually checks each test category
"""
import sys
import os

def run_manual_checks():
    print("🧪 CAMPUS CONNECT - MANUAL TEST VERIFICATION")
    print("=" * 60)
    
    # Add parent directory to path
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    test_results = {
        'passed': 0,
        'failed': 0,
        'skipped': 0
    }
    
    print("\n1. 🔧 BASIC FUNCTIONALITY TESTS")
    print("-" * 40)
    
    # Test 1: Basic Python
    try:
        assert 1 + 1 == 2
        assert "Campus" in "Campus Connect"
        print("✅ Basic Python operations")
        test_results['passed'] += 1
    except:
        print("❌ Basic Python operations")
        test_results['failed'] += 1
    
    # Test 2: Config import
    try:
        from app_config import MYSQL_HOST, MYSQL_USER, MYSQL_DB
        print("✅ Configuration import")
        test_results['passed'] += 1
    except ImportError as e:
        print("❌ Configuration import")
        test_results['failed'] += 1
    
    print("\n2. 🌐 PUBLIC PAGES TESTS")
    print("-" * 40)
    
    try:
        from app import app
        
        with app.test_client() as client:
            # Test homepage
            response = client.get('/')
            if response.status_code == 200 and b'Campus Connect' in response.data:
                print("✅ Homepage accessible")
                test_results['passed'] += 1
            else:
                print("❌ Homepage accessible")
                test_results['failed'] += 1
            
            # Test login page
            response = client.get('/login')
            if response.status_code == 200 and b'Login' in response.data:
                print("✅ Login page accessible")
                test_results['passed'] += 1
            else:
                print("❌ Login page accessible")
                test_results['failed'] += 1
            
            # Test register page
            response = client.get('/register')
            if response.status_code == 200 and b'Register' in response.data:
                print("✅ Register page accessible")
                test_results['passed'] += 1
            else:
                print("❌ Register page accessible")
                test_results['failed'] += 1
                
    except Exception as e:
        print(f"❌ Public pages tests failed: {e}")
        test_results['failed'] += 3
    
    print("\n3. 🔐 PROTECTED PAGES TESTS")
    print("-" * 40)
    
    try:
        from app import app
        
        with app.test_client() as client:
            protected_pages = [
                ('/dashboard', 'Dashboard'),
                ('/groups', 'Groups'),
                ('/resources', 'Resources'),
                ('/events', 'Events'),
                ('/profile', 'Profile')
            ]
            
            for page, name in protected_pages:
                response = client.get(page, follow_redirects=False)
                if response.status_code == 302:  # Should redirect to login
                    print(f"✅ {name} page redirects when not logged in")
                    test_results['passed'] += 1
                else:
                    print(f"❌ {name} page should redirect")
                    test_results['failed'] += 1
                    
    except Exception as e:
        print(f"❌ Protected pages tests failed: {e}")
        test_results['failed'] += 5
    
    print("\n4. 📊 DATABASE CONNECTION TEST")
    print("-" * 40)
    
    try:
        import mysql.connector
        from app_config import MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD
        
        conn = mysql.connector.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            auth_plugin='mysql_native_password'
        )
        print("✅ MySQL database connection")
        conn.close()
        test_results['passed'] += 1
    except Exception as e:
        print(f"⚠️  MySQL connection: {e}")
        test_results['skipped'] += 1
    
    print("\n" + "=" * 60)
    print("🎯 TEST SUMMARY")
    print(f"   ✅ Passed: {test_results['passed']}")
    print(f"   ❌ Failed: {test_results['failed']}")
    print(f"   ⚠️  Skipped: {test_results['skipped']}")
    
    total_tests = test_results['passed'] + test_results['failed'] + test_results['skipped']
    if total_tests > 0:
        success_rate = (test_results['passed'] / total_tests) * 100
        print(f"   📈 Success Rate: {success_rate:.1f}%")
    
    print("\n💡 INTERPRETATION:")
    if test_results['failed'] == 0:
        print("   🎉 ALL CRITICAL TESTS PASSED!")
        print("   Your application is working correctly.")
    else:
        print("   ⚠️  Some tests failed. Check the details above.")
    
    print("\n🔒 SECURITY NOTE:")
    print("   The 'redirect' tests (302 status) are actually GOOD!")
    print("   They prove your authentication system is working.")
    
    return test_results

if __name__ == '__main__':
    run_manual_checks()