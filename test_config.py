import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from app_config import Config
    print("✅ Successfully imported config.py")
    
    # Check required attributes
    required = ['MYSQL_HOST', 'MYSQL_USER', 'MYSQL_PASSWORD', 'MYSQL_DB', 'MYSQL_CURSORCLASS']
    all_good = True
    
    for attr in required:
        if hasattr(Config, attr):
            value = getattr(Config, attr)
            if value:
                masked = value if attr != 'MYSQL_PASSWORD' else '****'
                print(f"✅ {attr}: {masked}")
            else:
                print(f"❌ {attr}: EMPTY VALUE")
                all_good = False
        else:
            print(f"❌ {attr}: ATTRIBUTE MISSING")
            all_good = False
    
    if all_good:
        print("\n🎉 Configuration looks good! You can run: python database/init_db.py")
    else:
        print("\n❌ Please fix your config.py file")
        
except ImportError as e:
    print(f"❌ Cannot import config: {e}")
    print("💡 Make sure config.py exists in the same directory as this test file")
except Exception as e:
    print(f"❌ Error: {e}")