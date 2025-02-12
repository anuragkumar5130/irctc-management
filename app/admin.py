from flask import request, jsonify
from app import app, db
from app.models import Train
from config import Config

@app.route('/add_train', methods=['POST'])
def add_train():
    if request.headers.get("Admin-API-Key") != Config.ADMIN_API_KEY:
        return jsonify({"message": "Unauthorized"}), 403

    data = request.json
    train = Train(
        name=data['name'], source=data['source'],
        destination=data['destination'], total_seats=data['total_seats'],
        available_seats=data['total_seats']
    )
    db.session.add(train)
    db.session.commit()
    return jsonify({"message": "Train added successfully"}), 201
