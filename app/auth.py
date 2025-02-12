from flask import request, jsonify
from app import app, db, bcrypt
from app.models import User
from flask_jwt_extended import create_access_token

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    hashed_pw = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    user = User(username=data['username'], password=hashed_pw, role=data['role'])
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User registered successfully"}), 201

@app.route('/+', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(username=data['username']).first()
    if user and bcrypt.check_password_hash(user.password, data['password']):
        token = create_access_token(identity={"id": user.id, "role": user.role})
        return jsonify({"access_token": token}), 200
    return jsonify({"message": "Invalid credentials"}), 401
