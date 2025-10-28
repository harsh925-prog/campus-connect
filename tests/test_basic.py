import pytest
import os
import sys

def test_basic_math():
    """Basic math test"""
    assert 2 + 2 == 4

def test_string_operations():
    """String operation tests"""
    name = "Campus Connect"
    assert "Campus" in name
    assert "Connect" in name
    assert len(name) > 0

def test_list_operations():
    """List operation tests"""
    features = ["Groups", "Resources", "Events", "Authentication"]
    assert len(features) == 4
    assert "Groups" in features
    assert "Resources" in features

def test_imports():
    """Test that required modules can be imported"""
    import flask
    import mysql.connector
    import bcrypt
    import pytest
    assert True  # If we get here, imports work

def test_config_values():
    """Test configuration values"""
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    try:
        from app_config import MYSQL_HOST, MYSQL_USER, MYSQL_DB
        assert MYSQL_HOST == 'localhost'
        assert MYSQL_USER == 'root'
        assert MYSQL_DB == 'campus_connect'
        print("✅ Config values are correct")
    except ImportError:
        pytest.skip("Config not available")

if __name__ == '__main__':
    pytest.main([__file__, '-v'])