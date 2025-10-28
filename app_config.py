import os

class Config:
    # Flask Secret Key
    SECRET_KEY = 'campus-connect-secret-key-2024'
    
    # MySQL Database Configuration
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = 'root925'
    MYSQL_DB = 'campus_connect'
    MYSQL_CURSORCLASS = 'DictCursor'
    
    # Application Settings
    DEBUG = True

# Development configuration
class DevelopmentConfig(Config):
    DEBUG = True

# Testing configuration  
class TestingConfig(Config):
    TESTING = True
    MYSQL_DB = 'campus_connect_test'

# Production configuration
class ProductionConfig(Config):
    DEBUG = False

# Set default configuration
app_config = DevelopmentConfig

# Make all Config attributes available at module level for backward compatibility
MYSQL_HOST = Config.MYSQL_HOST
MYSQL_USER = Config.MYSQL_USER
MYSQL_PASSWORD = Config.MYSQL_PASSWORD
MYSQL_DB = Config.MYSQL_DB
MYSQL_CURSORCLASS = Config.MYSQL_CURSORCLASS
SECRET_KEY = Config.SECRET_KEY
DEBUG = Config.DEBUG

print("✅ Configuration loaded successfully!")