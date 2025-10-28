import mysql.connector
from config import Config

def init_database():
    try:
        # Connect to MySQL server (without selecting database)
        conn = mysql.connector.connect(
            host=Config.MYSQL_HOST,
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD
        )
        cursor = conn.cursor()
        
        # Read and execute schema file
        with open('database/schema.sql', 'r') as file:
            sql_commands = file.read().split(';')
            
            for command in sql_commands:
                if command.strip():
                    cursor.execute(command)
        
        conn.commit()
        print("Database initialized successfully!")
        
    except mysql.connector.Error as e:
        print(f"Error: {e}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == '__main__':
    init_database()