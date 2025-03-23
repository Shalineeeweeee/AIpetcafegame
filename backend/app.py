from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Database connection helper function
def get_db_connection():
    conn = sqlite3.connect("alpetcafe.db")
    conn.row_factory = sqlite3.Row  # Enables dictionary-like access to rows
    return conn

# Route: Home
@app.route("/")
def home():
    return jsonify({"message": "Welcome to AlpetCafeGame API!"})

# Route: Add a new user
@app.route("/add_user", methods=["POST"])
def add_user():
    data = request.json
    username = data.get("username")
    mood = data.get("mood", "neutral")

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO users (username, mood) VALUES (?, ?)", (username, mood))
        conn.commit()
        return jsonify({"message": f"User {username} added successfully!"}), 201
    except sqlite3.IntegrityError:
        return jsonify({"error": "Username already exists!"}), 400
    finally:
        conn.close()

# Route: Get user details
@app.route("/get_user/<username>", methods=["GET"])
def get_user(username):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()

    if user:
        return jsonify(dict(user))
    else:
        return jsonify({"error": "User not found!"}), 404

# Route: Add a task
@app.route("/add_task", methods=["POST"])
def add_task():
    data = request.json
    username = data.get("username")
    task_type = data.get("task_type")
    description = data.get("description")

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()

    if user:
        user_id = user["id"]
        cursor.execute("INSERT INTO tasks (user_id, task_type, description) VALUES (?, ?, ?)",
                       (user_id, task_type, description))
        conn.commit()
        conn.close()
        return jsonify({"message": f"Task '{description}' added for {username}."}), 201
    else:
        conn.close()
        return jsonify({"error": "User not found!"}), 404

# Route: Complete a task
@app.route("/complete_task/<int:task_id>", methods=["POST"])
def complete_task(task_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("UPDATE tasks SET completed = 1 WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()

    return jsonify({"message": f"Task {task_id} marked as completed."})

# Route: Update user mood
@app.route("/update_mood", methods=["POST"])
def update_mood():
    data = request.json
    username = data.get("username")
    new_mood = data.get("mood")

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("UPDATE users SET mood = ? WHERE username = ?", (new_mood, username))
    conn.commit()
    conn.close()

    return jsonify({"message": f"{username}'s mood updated to {new_mood}."})

# Route: Update game progress
@app.route("/update_progress/<username>", methods=["POST"])
def update_progress(username):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()

    if user:
        user_id = user["id"]
        cursor.execute("SELECT COUNT(*) FROM tasks WHERE user_id = ? AND completed = 1", (user_id,))
        completed_tasks = cursor.fetchone()[0]

        cursor.execute("UPDATE game_progress SET tasks_completed = ?, level = ? WHERE user_id = ?",
                       (completed_tasks, (completed_tasks // 3) + 1, user_id))
        conn.commit()
        conn.close()
        return jsonify({"message": f"{username}'s progress updated."})
    else:
        conn.close()
        return jsonify({"error": "User not found!"}), 404

# Start the Flask app
if __name__ == "__main__":
    app.run(debug=True)
