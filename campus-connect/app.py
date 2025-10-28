from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_mysqldb import MySQL
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import bcrypt
import mysql.connector
from config import DevelopmentConfig

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)

# Initialize MySQL
mysql = MySQL(app)

# Initialize Login Manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

class User(UserMixin):
    def __init__(self, student_id, email, name, major, skills):
        self.id = student_id
        self.email = email
        self.name = name
        self.major = major
        self.skills = skills

@login_manager.user_loader
def load_user(student_id):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM students WHERE student_id = %s", (student_id,))
        user_data = cursor.fetchone()
        cursor.close()
        
        if user_data:
            return User(user_data['student_id'], user_data['email'], user_data['name'], 
                       user_data['major'], user_data['skills'])
        return None
    except Exception as e:
        print(f"Error loading user: {e}")
        return None

# Helper function for database connection
def get_db_connection():
    return mysql.connection.cursor()

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        name = request.form['name']
        major = request.form['major']
        skills = request.form['skills']
        
        try:
            cursor = mysql.connection.cursor()
            
            # Check if email already exists
            cursor.execute("SELECT * FROM students WHERE email = %s", (email,))
            if cursor.fetchone():
                flash('Email already registered!', 'danger')
                return render_template('register.html')
            
            # Hash password
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            
            # Insert new user
            cursor.execute(
                "INSERT INTO students (email, password_hash, name, major, skills) VALUES (%s, %s, %s, %s, %s)",
                (email, hashed_password, name, major, skills)
            )
            mysql.connection.commit()
            cursor.close()
            
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
            
        except Exception as e:
            flash('Registration failed! Please try again.', 'danger')
            print(f"Error: {e}")
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        try:
            cursor = mysql.connection.cursor()
            cursor.execute("SELECT * FROM students WHERE email = %s", (email,))
            user_data = cursor.fetchone()
            cursor.close()
            
            if user_data and bcrypt.checkpw(password.encode('utf-8'), user_data['password_hash'].encode('utf-8')):
                user = User(user_data['student_id'], user_data['email'], user_data['name'], 
                           user_data['major'], user_data['skills'])
                login_user(user)
                flash('Login successful!', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('Invalid email or password!', 'danger')
                
        except Exception as e:
            flash('Login failed! Please try again.', 'danger')
            print(f"Error: {e}")
    
    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    try:
        cursor = mysql.connection.cursor()
        
        # Get user's groups
        cursor.execute("""
            SELECT g.* FROM project_groups g 
            JOIN group_members gm ON g.group_id = gm.group_id 
            WHERE gm.student_id = %s
        """, (current_user.id,))
        user_groups = cursor.fetchall()
        
        # Get recent resources
        cursor.execute("SELECT * FROM resources ORDER BY upload_date DESC LIMIT 5")
        recent_resources = cursor.fetchall()
        
        # Get upcoming events
        cursor.execute("SELECT * FROM events WHERE event_date > NOW() ORDER BY event_date ASC LIMIT 5")
        upcoming_events = cursor.fetchall()
        
        cursor.close()
        
    except Exception as e:
        print(f"Error: {e}")
        user_groups = []
        recent_resources = []
        upcoming_events = []
    
    return render_template('dashboard.html', 
                         groups=user_groups, 
                         resources=recent_resources, 
                         events=upcoming_events)

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        name = request.form['name']
        major = request.form['major']
        skills = request.form['skills']
        
        try:
            cursor = mysql.connection.cursor()
            cursor.execute(
                "UPDATE students SET name = %s, major = %s, skills = %s WHERE student_id = %s",
                (name, major, skills, current_user.id)
            )
            mysql.connection.commit()
            cursor.close()
            flash('Profile updated successfully!', 'success')
        except Exception as e:
            flash('Profile update failed!', 'danger')
            print(f"Error: {e}")
    
    return render_template('profile.html')

@app.route('/groups')
@login_required
def groups():
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("""
            SELECT g.*, s.name as creator_name 
            FROM project_groups g 
            JOIN students s ON g.created_by = s.student_id
        """)
        all_groups = cursor.fetchall()
        cursor.close()
    except Exception as e:
        print(f"Error: {e}")
        all_groups = []
    
    return render_template('groups.html', groups=all_groups)

@app.route('/create_group', methods=['POST'])
@login_required
def create_group():
    group_name = request.form['group_name']
    description = request.form['description']
    
    try:
        cursor = mysql.connection.cursor()
        cursor.execute(
            "INSERT INTO project_groups (group_name, description, created_by) VALUES (%s, %s, %s)",
            (group_name, description, current_user.id)
        )
        group_id = cursor.lastrowid
        
        # Add creator as member
        cursor.execute(
            "INSERT INTO group_members (group_id, student_id) VALUES (%s, %s)",
            (group_id, current_user.id)
        )
        
        mysql.connection.commit()
        cursor.close()
        flash('Group created successfully!', 'success')
    except Exception as e:
        flash('Group creation failed!', 'danger')
        print(f"Error: {e}")
    
    return redirect(url_for('groups'))

@app.route('/join_group/<int:group_id>')
@login_required
def join_group(group_id):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute(
            "INSERT IGNORE INTO group_members (group_id, student_id) VALUES (%s, %s)",
            (group_id, current_user.id)
        )
        mysql.connection.commit()
        cursor.close()
        flash('Joined group successfully!', 'success')
    except Exception as e:
        flash('Failed to join group!', 'danger')
        print(f"Error: {e}")
    
    return redirect(url_for('groups'))

@app.route('/resources')
@login_required
def resources():
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("""
            SELECT r.*, s.name as uploader_name 
            FROM resources r 
            JOIN students s ON r.uploaded_by = s.student_id 
            ORDER BY r.upload_date DESC
        """)
        all_resources = cursor.fetchall()
        cursor.close()
    except Exception as e:
        print(f"Error: {e}")
        all_resources = []
    
    return render_template('resources.html', resources=all_resources)

@app.route('/upload_resource', methods=['POST'])
@login_required
def upload_resource():
    title = request.form['title']
    description = request.form['description']
    resource_type = request.form['resource_type']
    
    try:
        cursor = mysql.connection.cursor()
        cursor.execute(
            "INSERT INTO resources (title, description, resource_type, uploaded_by) VALUES (%s, %s, %s, %s)",
            (title, description, resource_type, current_user.id)
        )
        mysql.connection.commit()
        cursor.close()
        flash('Resource uploaded successfully!', 'success')
    except Exception as e:
        flash('Resource upload failed!', 'danger')
        print(f"Error: {e}")
    
    return redirect(url_for('resources'))

@app.route('/events')
@login_required
def events():
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("""
            SELECT e.*, s.name as organizer_name,
            (SELECT COUNT(*) FROM rsvps WHERE event_id = e.event_id AND status = 'going') as going_count
            FROM events e 
            JOIN students s ON e.organized_by = s.student_id 
            ORDER BY e.event_date ASC
        """)
        all_events = cursor.fetchall()
        cursor.close()
    except Exception as e:
        print(f"Error: {e}")
        all_events = []
    
    return render_template('events.html', events=all_events)

@app.route('/create_event', methods=['POST'])
@login_required
def create_event():
    title = request.form['title']
    description = request.form['description']
    event_date = request.form['event_date']
    location = request.form['location']
    
    try:
        cursor = mysql.connection.cursor()
        cursor.execute(
            "INSERT INTO events (title, description, event_date, location, organized_by) VALUES (%s, %s, %s, %s, %s)",
            (title, description, event_date, location, current_user.id)
        )
        mysql.connection.commit()
        cursor.close()
        flash('Event created successfully!', 'success')
    except Exception as e:
        flash('Event creation failed!', 'danger')
        print(f"Error: {e}")
    
    return redirect(url_for('events'))

@app.route('/rsvp_event/<int:event_id>/<status>')
@login_required
def rsvp_event(event_id, status):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute(
            "INSERT INTO rsvps (event_id, student_id, status) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE status = %s",
            (event_id, current_user.id, status, status)
        )
        mysql.connection.commit()
        cursor.close()
        flash('RSVP updated successfully!', 'success')
    except Exception as e:
        flash('RSVP update failed!', 'danger')
        print(f"Error: {e}")
    
    return redirect(url_for('events'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)