import mysql.connector
import sys
import os

# Add parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def get_config():
    """Get configuration from config.py"""
    try:
        # Try importing the simple config first
        from app_config import MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB
        return {
            'host': MYSQL_HOST,
            'user': MYSQL_USER,
            'password': MYSQL_PASSWORD,
            'database': MYSQL_DB
        }
    except ImportError:
        try:
            # Try importing from Config class
            from app_config import Config
            return {
                'host': Config.MYSQL_HOST,
                'user': Config.MYSQL_USER,
                'password': Config.MYSQL_PASSWORD,
                'database': Config.MYSQL_DB
            }
        except (ImportError, AttributeError) as e:
            print(f"❌ Configuration error: {e}")
            print("💡 Using fallback configuration...")
            # Fallback configuration
            return {
                'host': 'localhost',
                'user': 'root',
                'password': 'root925',
                'database': 'campus_connect'
            }

def init_database():
    conn = None
    cursor = None
    
    try:
        print("🚀 Starting database initialization...")
        
        # Get configuration
        config = get_config()
        
        print("📋 Using configuration:")
        for key, value in config.items():
            masked_value = value if key != 'password' else '****' + str(value)[-3:]
            print(f"   ✅ {key}: {masked_value}")
        
        # Connect to MySQL server
        print("🔗 Connecting to MySQL server...")
        conn = mysql.connector.connect(
            host=config['host'],
            user=config['user'],
            password=config['password'],
            auth_plugin='mysql_native_password'
        )
        cursor = conn.cursor()
        print("✅ Connected to MySQL server successfully!")
        
        # Create database
        print(f"📦 Creating database '{config['database']}'...")
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {config['database']}")
        cursor.execute(f"USE {config['database']}")
        print(f"✅ Database '{config['database']}' ready!")
        
        # Read and execute schema
        print("📊 Creating tables from schema...")
        schema_path = os.path.join(os.path.dirname(__file__), 'schema.sql')
        
        if not os.path.exists(schema_path):
            print(f"❌ Schema file not found: {schema_path}")
            print("💡 Creating basic tables instead...")
            # Create basic tables directly
            create_basic_tables(cursor)
        else:
            with open(schema_path, 'r', encoding='utf-8') as file:
                sql_script = file.read()
            
            # Split commands and execute
            commands = [cmd.strip() for cmd in sql_script.split(';') if cmd.strip()]
            
            for command in commands:
                if command and not command.startswith('--'):
                    try:
                        cursor.execute(command)
                        if 'CREATE TABLE' in command.upper():
                            table_name = command.split('(')[0].replace('CREATE TABLE', '').strip()
                            print(f"   ✅ Created: {table_name}")
                    except mysql.connector.Error as e:
                        if "already exists" not in str(e):
                            print(f"   ⚠️  Note: {e}")
        
        conn.commit()
        print("🎉 Database initialized successfully!")
        print("\n✨ Next steps:")
        print("   1. Run: python app.py")
        print("   2. Open: http://localhost:5000")
        print("   3. Register your first account!")

    except mysql.connector.Error as e:
        print(f"❌ MySQL Error: {e}")
        print("\n🔧 Troubleshooting:")
        print("   - Is MySQL running? Try: net start mysql (Windows)")
        print("   - Check if MySQL password is correct")
        print("   - Test manually: mysql -u root -p")
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()
            print("🔒 Connection closed.")

def create_basic_tables(cursor):
    """Create basic tables if schema.sql is missing"""
    tables = [
        """CREATE TABLE IF NOT EXISTS students (
            student_id INT AUTO_INCREMENT PRIMARY KEY,
            email VARCHAR(255) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            name VARCHAR(255) NOT NULL,
            major VARCHAR(100),
            skills TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )""",
        
        """CREATE TABLE IF NOT EXISTS project_groups (
            group_id INT AUTO_INCREMENT PRIMARY KEY,
            group_name VARCHAR(255) NOT NULL,
            description TEXT,
            created_by INT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )""",
        
        """CREATE TABLE IF NOT EXISTS group_members (
            group_id INT,
            student_id INT,
            joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (group_id, student_id)
        )""",
        
        """CREATE TABLE IF NOT EXISTS resources (
            resource_id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            description TEXT,
            file_path VARCHAR(500),
            resource_type ENUM('note', 'link', 'file') DEFAULT 'note',
            uploaded_by INT NOT NULL,
            upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )""",
        
        """CREATE TABLE IF NOT EXISTS events (
            event_id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            description TEXT,
            event_date DATETIME NOT NULL,
            location VARCHAR(255),
            organized_by INT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )""",
        
        """CREATE TABLE IF NOT EXISTS rsvps (
            event_id INT,
            student_id INT,
            status ENUM('going', 'not_going', 'maybe') DEFAULT 'going',
            rsvp_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (event_id, student_id)
        )"""
    ]
    
    for table_sql in tables:
        try:
            cursor.execute(table_sql)
            table_name = table_sql.split('(')[0].replace('CREATE TABLE', '').replace('IF NOT EXISTS', '').strip()
            print(f"   ✅ Created: {table_name}")
        except mysql.connector.Error as e:
            print(f"   ⚠️  Note: {e}")

if __name__ == '__main__':
    init_database()