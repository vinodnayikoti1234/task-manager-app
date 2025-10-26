from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import re
import os

app = Flask(__name__)
CORS(app)

# Render PostgreSQL config (use your values, already filled below)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://n_vinod_kumar_user:HdSRCnT11SfRKXdpTZFsgTFNXRRxGCoA@dpg-d3v09qodl3ps73ff28r0-a:5432/n_vinod_kumar'
db = SQLAlchemy(app)

# User model (make sure you migrate the DB for changes)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

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

    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email already exists'}), 400
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

# Serve static files (use if needed)
@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('static', path)

if __name__ == "__main__":
    if not os.path.exists("instance"):
        os.makedirs("instance")
    with app.app_context():
        db.create_all()
    app.run(debug=True)
