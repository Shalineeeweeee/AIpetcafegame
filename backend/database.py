import sqlite3

# Connect to the database (creates the file if it doesn't exist)
conn = sqlite3.connect("alpetcafe.db")
cursor = conn.cursor()

# Create users table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        mood TEXT,
        coins INTEGER DEFAULT 0
    )
''')

# Create tasks table (tracks work, relaxation, and self-care tasks)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        task_type TEXT CHECK(task_type IN ('work', 'relaxation', 'self-care')),
        description TEXT NOT NULL,
        completed BOOLEAN DEFAULT 0,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
''')

# Create game progress table (tracks user level and task completion)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS game_progress (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        level INTEGER DEFAULT 1,
        tasks_completed INTEGER DEFAULT 0,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
''')

conn.commit()

# Function to add a new user
def add_user(username, mood="neutral"):
    try:
        cursor.execute("INSERT INTO users (username, mood) VALUES (?, ?)", (username, mood))
        conn.commit()
        print(f"User {username} added successfully.")
    except sqlite3.IntegrityError:
        print("Username already exists!")

# Function to get user details
def get_user(username):
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    return cursor.fetchone()

# Function to add a task for a user
def add_task(username, task_type, description):
    cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    
    if user:
        user_id = user[0]
        cursor.execute("INSERT INTO tasks (user_id, task_type, description) VALUES (?, ?, ?)",
                       (user_id, task_type, description))
        conn.commit()
        print(f"Task '{description}' added for {username}.")
    else:
        print("User not found!")

# Function to mark a task as completed
def complete_task(task_id):
    cursor.execute("UPDATE tasks SET completed = 1 WHERE id = ?", (task_id,))
    conn.commit()
    print(f"Task {task_id} marked as completed.")

# Function to update user mood
def update_mood(username, new_mood):
    cursor.execute("UPDATE users SET mood = ? WHERE username = ?", (new_mood, username))
    conn.commit()
    print(f"{username}'s mood updated to {new_mood}.")

# Function to track level progression
def update_progress(username):
    cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()

    if user:
        user_id = user[0]
        cursor.execute("SELECT COUNT(*) FROM tasks WHERE user_id = ? AND completed = 1", (user_id,))
        completed_tasks = cursor.fetchone()[0]

        cursor.execute("UPDATE game_progress SET tasks_completed = ?, level = ? WHERE user_id = ?",
                       (completed_tasks, (completed_tasks // 3) + 1, user_id))
        conn.commit()
        print(f"{username}'s progress updated.")
    else:
        print("User not found!")

# Close connection when script finishes
def close_connection():
    conn.close()

# Initialize default user for testing (optional)
if __name__ == "__main__":
    add_user("test_user")
    add_task("test_user", "work", "Complete coding project")
    add_task("test_user", "relaxation", "Read a book")
    add_task("test_user", "self-care", "Drink water")
    update_progress("test_user")
    close_connection()
