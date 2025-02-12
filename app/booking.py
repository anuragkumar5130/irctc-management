from flask import request, jsonify
from app import app, db
from app.models import Booking, Train
from flask_jwt_extended import jwt_required, get_jwt_identity

@app.route('/book_seat', methods=['POST'])
@jwt_required()
def book_seat():
    user = get_jwt_identity()
    data = request.json
    train_id = data.get("train_id")

    with db.session.begin_nested():  # Ensure transaction safety
        train = db.session.query(Train).filter_by(id=train_id).with_for_update().first()

        if not train or train.available_seats <= 0:
            return jsonify({"message": "No seats available"}), 400

        seat_number = train.total_seats - train.available_seats + 1
        train.available_seats -= 1
        booking = Booking(user_id=user['id'], train_id=train_id, seat_number=seat_number)

        db.session.add(booking)
        db.session.commit()

    return jsonify({"message": "Seat booked successfully", "seat_number": seat_number}), 201
