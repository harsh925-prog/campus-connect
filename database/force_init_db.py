import mysql.connector
import bcrypt
import sys
import os

# Add parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def force_init_database():
    conn = None
    cursor = None
    
    # Direct configuration (no imports needed)
    MYSQL_CONFIG = {
        'host': 'localhost',
        'user': 'root',
        'password': 'root925',
        'database': 'campus_connect'
    }
    
    try:
        print("🚀 FORCE INITIALIZING DATABASE...")
        print("=" * 50)
        print(f"📊 Using database: {MYSQL_CONFIG['database']}")
        print(f"🔗 Connecting to: {MYSQL_CONFIG['host']} as {MYSQL_CONFIG['user']}")
        
        # Connect to MySQL server
        conn = mysql.connector.connect(
            host=MYSQL_CONFIG['host'],
            user=MYSQL_CONFIG['user'],
            password=MYSQL_CONFIG['password'],
            auth_plugin='mysql_native_password'
        )
        cursor = conn.cursor()
        print("✅ Connected to MySQL server")
        
        # Create database
        cursor.execute(f"DROP DATABASE IF EXISTS {MYSQL_CONFIG['database']}")
        cursor.execute(f"CREATE DATABASE {MYSQL_CONFIG['database']}")
        cursor.execute(f"USE {MYSQL_CONFIG['database']}")
        print(f"✅ Database '{MYSQL_CONFIG['database']}' created")
        
        # Create tables directly
        print("📊 Creating tables...")
        
        # Students table
        cursor.execute("""
            CREATE TABLE students (
                student_id INT AUTO_INCREMENT PRIMARY KEY,
                email VARCHAR(255) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                name VARCHAR(255) NOT NULL,
                major VARCHAR(100),
                skills TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("✅ Created 'students' table")
        
        # Project groups table
        cursor.execute("""
            CREATE TABLE project_groups (
                group_id INT AUTO_INCREMENT PRIMARY KEY,
                group_name VARCHAR(255) NOT NULL,
                description TEXT,
                created_by INT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (created_by) REFERENCES students(student_id) ON DELETE CASCADE
            )
        """)
        print("✅ Created 'project_groups' table")
        
        # Group members table
        cursor.execute("""
            CREATE TABLE group_members (
                group_id INT,
                student_id INT,
                joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (group_id, student_id),
                FOREIGN KEY (group_id) REFERENCES project_groups(group_id) ON DELETE CASCADE,
                FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE
            )
        """)
        print("✅ Created 'group_members' table")
        
        # Resources table
        cursor.execute("""
            CREATE TABLE resources (
                resource_id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                description TEXT,
                file_path VARCHAR(500),
                resource_type ENUM('note', 'link', 'file') DEFAULT 'note',
                uploaded_by INT NOT NULL,
                upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (uploaded_by) REFERENCES students(student_id) ON DELETE CASCADE
            )
        """)
        print("✅ Created 'resources' table")
        
        # Events table
        cursor.execute("""
            CREATE TABLE events (
                event_id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                description TEXT,
                event_date DATETIME NOT NULL,
                location VARCHAR(255),
                organized_by INT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (organized_by) REFERENCES students(student_id) ON DELETE CASCADE
            )
        """)
        print("✅ Created 'events' table")
        
        # RSVP table
        cursor.execute("""
            CREATE TABLE rsvps (
                event_id INT,
                student_id INT,
                status ENUM('going', 'not_going', 'maybe') DEFAULT 'going',
                rsvp_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (event_id, student_id),
                FOREIGN KEY (event_id) REFERENCES events(event_id) ON DELETE CASCADE,
                FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE
            )
        """)
        print("✅ Created 'rsvps' table")
        
        conn.commit()
        
        print("\n🎉 DATABASE FORCE INITIALIZED SUCCESSFULLY!")
        print("All tables created successfully!")
        
        # Add a test user
        hashed_password = bcrypt.hashpw('password123'.encode('utf-8'), bcrypt.gensalt())
        cursor.execute(
            "INSERT INTO students (email, password_hash, name, major, skills) VALUES (%s, %s, %s, %s, %s)",
            ('test@student.com', hashed_password, 'Test Student', 'Computer Science', 'Python, Testing')
        )
        conn.commit()
        print("✅ Added test user: test@student.com / password123")
        
        print("\n✨ NEXT STEPS:")
        print("   1. Run: python app.py")
        print("   2. Open: http://localhost:5000")
        print("   3. Login with: test@student.com / password123")
        print("   4. Or register a new account")
        
    except mysql.connector.Error as e:
        print(f"❌ MySQL Error: {e}")
        print("\n🔧 TROUBLESHOOTING:")
        print("   - Is MySQL running? Try: net start mysql (Windows)")
        print("   - Check if MySQL password is correct")
        print("   - Verify MySQL is installed")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()
            print("🔒 Database connection closed")

if __name__ == '__main__':
    force_init_database()