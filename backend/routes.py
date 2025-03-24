from flask import Blueprint, jsonify, request
from database import (
    add_user, get_user, add_task, complete_task, 
    update_mood, update_progress
)

game_routes = Blueprint('game_routes', __name__)

@game_routes.route('/user/create', methods=['POST'])
def create_user():
    """Create a new user"""
    data = request.json
    username = data.get('username')
    mood = data.get('mood', 'neutral')
    
    try:
        add_user(username, mood)
        return jsonify({'message': f'User {username} created successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@game_routes.route('/user/get/<username>', methods=['GET'])
def retrieve_user(username):
    """Retrieve user details"""
    user = get_user(username)
    
    if user:
        return jsonify({
            'id': user[0],
            'username': user[1],
            'mood': user[2],
            'coins': user[3]
        }), 200
    else:
        return jsonify({'error': 'User not found'}), 404

@game_routes.route('/tasks/add', methods=['POST'])
def create_task():
    """Add a new task for a user"""
    data = request.json
    username = data.get('username')
    task_type = data.get('task_type')
    description = data.get('description')
    
    try:
        add_task(username, task_type, description)
        return jsonify({'message': 'Task added successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@game_routes.route('/tasks/complete/<int:task_id>', methods=['POST'])
def finish_task(task_id):
    """Mark a task as completed"""
    try:
        complete_task(task_id)
        return jsonify({'message': f'Task {task_id} completed'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@game_routes.route('/user/mood', methods=['PUT'])
def set_mood():
    """Update user mood"""
    data = request.json
    username = data.get('username')
    new_mood = data.get('mood')
    
    try:
        update_mood(username, new_mood)
        return jsonify({'message': 'Mood updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@game_routes.route('/user/progress/<username>', methods=['POST'])
def update_user_progress(username):
    """Update user game progress"""
    try:
        update_progress(username)
        return jsonify({'message': 'Progress updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

