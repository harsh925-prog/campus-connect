-- Test data for Campus Connect

-- Test Students
INSERT INTO students (student_id, email, password_hash, name, major, skills) VALUES
(1, 'alice@university.com', '$2b$12$hashedpassword1', 'Alice Johnson', 'Computer Science', 'Python, Java, Web Development'),
(2, 'bob@university.com', '$2b$12$hashedpassword2', 'Bob Smith', 'Mathematics', 'Calculus, Statistics, Data Analysis'),
(3, 'carol@university.com', '$2b$12$hashedpassword3', 'Carol Davis', 'Physics', 'Quantum Mechanics, Research');

-- Test Groups
INSERT INTO project_groups (group_id, group_name, description, created_by) VALUES
(1, 'Web Dev Team 2024', 'Building modern web applications using React and Flask', 1),
(2, 'Math Study Group', 'Collaborative learning for advanced calculus', 2),
(3, 'Physics Research', 'Quantum computing research project', 3);

-- Test Group Members
INSERT INTO group_members (group_id, student_id) VALUES
(1, 1), (1, 2),  -- Alice and Bob in Web Dev Team
(2, 2), (2, 3),  -- Bob and Carol in Math Study Group
(3, 3), (3, 1);  -- Carol and Alice in Physics Research

-- Test Resources
INSERT INTO resources (resource_id, title, description, resource_type, uploaded_by) VALUES
(1, 'Flask Tutorial', 'Complete guide to Flask web development', 'note', 1),
(2, 'Calculus Formulas', 'Important formulas for calculus exam', 'note', 2),
(3, 'Quantum Physics Notes', 'Notes from quantum mechanics lectures', 'note', 3);

-- Test Events
INSERT INTO events (event_id, title, description, event_date, location, organized_by) VALUES
(1, 'Tech Talk: AI in Education', 'Discussion about AI applications in education', '2024-12-15 18:00:00', 'Main Auditorium', 1),
(2, 'Math Competition', 'Annual university math competition', '2024-12-20 10:00:00', 'Science Building Room 101', 2),
(3, 'Physics Seminar', 'Recent advances in quantum computing', '2024-12-18 16:00:00', 'Physics Department', 3);

-- Test RSVPs
INSERT INTO rsvps (event_id, student_id, status) VALUES
(1, 1, 'going'), (1, 2, 'going'), (1, 3, 'maybe'),
(2, 2, 'going'), (2, 1, 'not_going'),
(3, 3, 'going'), (3, 1, 'going');