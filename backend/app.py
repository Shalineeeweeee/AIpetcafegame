from flask import Flask, request, jsonify
import sqlite3
import requests
import os
from datetime import datetime

app = Flask(__name__)

# Nebius AI Configuration
NEBIUS_API_ENDPOINT = "https://neo.ai.nebius.cloud/v1/chat/completions"
NEBIUS_API_KEY = os.getenv('NEBIUS_API_KEY')

def get_db_connection():
    conn = sqlite3.connect("petcafe.db")
    conn.row_factory = sqlite3.Row
    return conn

# Enhanced User Registration
@app.route("/register", methods=["POST"])
def register_user():
    data = request.json
    username = data.get("username")
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            INSERT INTO users 
            (username, mood_score, current_level, total_coins, last_login) 
            VALUES (?, 50, 1, 0, ?)
        """, (username, datetime.now()))
        
        conn.commit()
        return jsonify({"message": "User registered successfully", "level": 1, "coins": 0}), 201
    except sqlite3.IntegrityError:
        return jsonify({"error": "Username already exists"}), 400
    finally:
        conn.close()

# AI-Powered Goal Generation
@app.route("/generate_goals", methods=["POST"])
def generate_goals():
    data = request.json
    username = data.get("username")
    
    # Retrieve user's current mood and level
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT mood_score, current_level FROM users WHERE username = ?", (username,))
    user_data = cursor.fetchone()
    
    if not user_data:
        return jsonify({"error": "User not found"}), 404
    
    mood_score = user_data['mood_score']
    current_level = user_data['current_level']
    
    try:
        # Nebius AI Goal Generation
        headers = {
            "Authorization": f"Bearer {NEBIUS_API_KEY}",
            "Content-Type": "application/json"
        }
        
        prompt = f"""
        Generate 3 personalized goals for a user with:
        - Mood Score: {mood_score}/100
        - Current Game Level: {current_level}
        
        Goals should be:
        1. Work/Productivity Goal
        2. Relaxation Goal
        3. Self-Care Goal
        
        Adjust goal difficulty based on mood score.
        """
        
        payload = {
            "model": "yandex/yandex-gpt-latest",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 300
        }
        
        response = requests.post(NEBIUS_API_ENDPOINT, headers=headers, json=payload)
        
        if response.status_code == 200:
            ai_goals = response.json()['choices'][0]['message']['content']
            
            # Parse and insert goals
            goals = ai_goals.split('\n')[1:]  # Remove first line
            for goal_type, description in zip(['work', 'relaxation', 'self-care'], goals):
                cursor.execute("""
                    INSERT INTO goals 
                    (user_id, goal_type, description, status, difficulty, created_at) 
                    VALUES ((SELECT id FROM users WHERE username = ?), ?, ?, 'pending', ?, ?)
                """, (username, goal_type, description.strip(), current_level, datetime.now()))
            
            conn.commit()
            return jsonify({"goals": goals}), 200
        else:
            return jsonify({"error": "Goal generation failed"}), 500
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

# Mood and Progression Tracking
@app.route("/update_mood", methods=["POST"])
def update_mood():
    data = request.json
    username = data.get("username")
    mood_change = data.get("mood_change", 0)
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            UPDATE users 
            SET mood_score = MAX(0, MIN(100, mood_score + ?)) 
            WHERE username = ?
        """, (mood_change, username))
        
        conn.commit()
        return jsonify({"message": "Mood updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

if __name__ == "__main__":
    app.run(debug=True)
