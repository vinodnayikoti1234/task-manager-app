from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://n_vinod_kumar_user:HdSRCnT11SfRKXdpTZFsgTFNXRRxGCoA@dpg-d3v09qodl3ps73ff28r0-a:5432/n_vinod_kumar'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

# Task model (for dashboard)
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)
    user_email = db.Column(db.String(120), nullable=False)

with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return "Task manager backend running!"

# Signup endpoint
@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    if User.query.filter((User.email == email) | (User.username == username)).first():
        return jsonify({'error': 'Email or username already exists'}), 400
    user = User(username=username, email=email, password=password)
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully'})

# Login endpoint
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    user = User.query.filter_by(email=email, password=password).first()
    if not user:
        return jsonify({'error': 'Invalid credentials'}), 401
    return jsonify({'message': 'Login successful', 'username': user.username})

# Get all tasks for user
@app.route('/tasks', methods=['GET'])
def get_tasks():
    user_email = request.args.get('user_email')
    tasks = Task.query.filter_by(user_email=user_email).all()
    return jsonify([{'id': t.id, 'description': t.description} for t in tasks])

# Add a task
@app.route('/tasks', methods=['POST'])
def add_task():
    data = request.get_json()
    description = data.get('description')
    user_email = data.get('user_email')
    if not description or not user_email:
        return jsonify({'error': 'Missing data'}), 400
    task = Task(description=description, user_email=user_email)
    db.session.add(task)
    db.session.commit()
    return jsonify({'message': 'Task added!'})

# Delete a task
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    db.session.delete(task)
    db.session.commit()
    return jsonify({'message': 'Task deleted!'})

# Serve static files (if needed)
@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('static', path)

if __name__ == "__main__":
    if not os.path.exists("instance"):
        os.makedirs("instance")
    app.run(debug=True)
