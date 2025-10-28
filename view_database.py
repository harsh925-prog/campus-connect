import mysql.connector
from app_config import MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB

def view_database():
    try:
        print("🔍 VIEWING CAMPUS CONNECT DATABASE")
        print("=" * 50)
        
        # Connect to database
        conn = mysql.connector.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DB,
            auth_plugin='mysql_native_password'
        )
        cursor = conn.cursor(dictionary=True)  # Returns dictionaries instead of tuples
        
        # Get table counts
        tables = ['students', 'project_groups', 'resources', 'events', 'group_members', 'rsvps']
        
        for table in tables:
            cursor.execute(f"SELECT COUNT(*) as count FROM {table}")
            result = cursor.fetchone()
            print(f"📊 {table.capitalize()}: {result['count']} records")
        
        print("\n👥 STUDENTS DETAILS:")
        print("-" * 40)
        cursor.execute("SELECT student_id, email, name, major, skills, created_at FROM students")
        students = cursor.fetchall()
        for student in students:
            print(f"ID: {student['student_id']} | Email: {student['email']} | Name: {student['name']} | Major: {student['major']}")
        
        print("\n👥 PROJECT GROUPS:")
        print("-" * 40)
        cursor.execute("""
            SELECT g.group_id, g.group_name, g.description, s.name as creator_name, g.created_at 
            FROM project_groups g 
            JOIN students s ON g.created_by = s.student_id
        """)
        groups = cursor.fetchall()
        for group in groups:
            print(f"ID: {group['group_id']} | Name: {group['group_name']} | Creator: {group['creator_name']}")
        
        print("\n📚 RESOURCES:")
        print("-" * 40)
        cursor.execute("""
            SELECT r.resource_id, r.title, r.resource_type, s.name as uploader, r.upload_date 
            FROM resources r 
            JOIN students s ON r.uploaded_by = s.student_id
        """)
        resources = cursor.fetchall()
        for resource in resources:
            print(f"ID: {resource['resource_id']} | Title: {resource['title']} | Type: {resource['resource_type']} | By: {resource['uploader']}")
        
        print("\n📅 EVENTS:")
        print("-" * 40)
        cursor.execute("""
            SELECT e.event_id, e.title, e.event_date, e.location, s.name as organizer 
            FROM events e 
            JOIN students s ON e.organized_by = s.student_id
        """)
        events = cursor.fetchall()
        for event in events:
            print(f"ID: {event['event_id']} | Title: {event['title']} | Date: {event['event_date']} | Location: {event['location']}")
        
        print("\n🔗 GROUP MEMBERSHIPS:")
        print("-" * 40)
        cursor.execute("""
            SELECT gm.group_id, g.group_name, s.name as member_name, gm.joined_at 
            FROM group_members gm 
            JOIN project_groups g ON gm.group_id = g.group_id 
            JOIN students s ON gm.student_id = s.student_id
        """)
        members = cursor.fetchall()
        for member in members:
            print(f"Group: {member['group_name']} | Member: {member['member_name']} | Joined: {member['joined_at']}")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Error viewing database: {e}")

if __name__ == '__main__':
    view_database()