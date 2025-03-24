from database import db
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    """User account model"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    
    # Relationships
    game_progress = db.relationship('GameProgress', back_populates='user', uselist=False)
    orders = db.relationship('Order', back_populates='user')
    tasks = db.relationship('Task', back_populates='user')
    
    def set_password(self, password):
        """Create hashed password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check hashed password"""
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        """Convert user to dictionary"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email
        }

class GameProgress(db.Model):
    """Tracks user's game progression"""
    __tablename__ = 'game_progress'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    
    # Game stats
    coins = db.Column(db.Integer, default=100)
    level = db.Column(db.Integer, default=1)
    experience = db.Column(db.Integer, default=0)
    
    # Relationships
    user = db.relationship('User', back_populates='game_progress')
    
    def to_dict(self):
        """Convert game progress to dictionary"""
        return {
            'user_id': self.user_id,
            'coins': self.coins,
            'level': self.level,
            'experience': self.experience
        }

class Order(db.Model):
    """Game orders model"""
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Order details
    items = db.Column(db.JSON, nullable=False)  # Store list of items
    reward = db.Column(db.Integer, nullable=False)
    time_limit = db.Column(db.Integer, nullable=False)  # in seconds
    status = db.Column(db.String(20), default='active')
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime, nullable=True)
    
    # Relationships
    user = db.relationship('User', back_populates='orders')
    
    def to_dict(self):
        """Convert order to dictionary"""
        return {
            'id': self.id,
            'items': self.items,
            'reward': self.reward,
            'time_limit': self.time_limit,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None
        }

class Task(db.Model):
    """Game tasks model"""
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Task details
    description = db.Column(db.String(255), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime, nullable=True)
    
    # Relationships
    user = db.relationship('User', back_populates='tasks')
    
    def to_dict(self):
        """Convert task to dictionary"""
        return {
            'id': self.id,
            'description': self.description,
            'completed': self.completed,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None
        }