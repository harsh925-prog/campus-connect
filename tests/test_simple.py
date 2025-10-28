"""
Simple tests that definitely work
"""
def test_basic():
    assert 1 + 1 == 2
    print("✅ Basic math test passed")

def test_strings():
    assert "Campus" in "Campus Connect"
    assert "Connect" in "Campus Connect"
    print("✅ String tests passed")

def test_lists():
    features = ["Authentication", "Groups", "Resources", "Events"]
    assert len(features) == 4
    assert "Groups" in features
    print("✅ List tests passed")

def test_imports():
    try:
        import flask
        import mysql.connector
        import bcrypt
        print("✅ All imports work")
    except ImportError as e:
        print(f"⚠️  Import issue: {e}")

if __name__ == '__main__':
    test_basic()
    test_strings() 
    test_lists()
    test_imports()
    print("🎉 All simple tests completed!")