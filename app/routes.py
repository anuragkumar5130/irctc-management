from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app import db, bcrypt
from app.models import User, Train, Booking
from config import Config
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import load_only

routes = Blueprint('routes', __name__)

# ✅ 1️⃣ Register a User
@routes.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    role = data.get('role', 'user')  # Default role is 'user'

    if role not in ['admin', 'user']:
        return jsonify({"message": "Invalid role. Choose 'admin' or 'user'"}), 400

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    new_user = User(username=username, password=hashed_password, role=role)

    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "User registered successfully"}), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({"message": "Username already exists"}), 400


# ✅ 2️⃣ Login User
@routes.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()
    if not user or not bcrypt.check_password_hash(user.password, password):
        return jsonify({"message": "Invalid credentials"}), 401

    access_token = create_access_token(identity={'id': user.id, 'role': user.role})
    return jsonify({"access_token": access_token}), 200


# ✅ 3️⃣ Add a New Train (Admin Only)
@routes.route('/add_train', methods=['POST'])
def add_train():
    api_key = request.headers.get('X-API-KEY')
    if api_key != Config.ADMIN_API_KEY:
        return jsonify({"message": "Unauthorized"}), 403

    data = request.json
    name = data.get('name')
    source = data.get('source')
    destination = data.get('destination')
    total_seats = data.get('total_seats')

    if not name or not source or not destination or not total_seats:
        return jsonify({"message": "All fields are required"}), 400

    new_train = Train(name=name, source=source, destination=destination, total_seats=total_seats, available_seats=total_seats)
    db.session.add(new_train)
    db.session.commit()
    
    return jsonify({"message": "Train added successfully"}), 201


# ✅ 4️⃣ Get Seat Availability
@routes.route('/seat_availability', methods=['GET'])
def seat_availability():
    source = request.args.get('source')
    destination = request.args.get('destination')

    if not source or not destination:
        return jsonify({"message": "Source and destination are required"}), 400

    trains = Train.query.filter_by(source=source, destination=destination).all()

    if not trains:
        return jsonify({"message": "No trains found"}), 404

    result = [{"train_id": train.id, "name": train.name, "available_seats": train.available_seats} for train in trains]
    return jsonify(result), 200


# ✅ 5️⃣ Book a Seat
@routes.route('/book_seat', methods=['POST'])
@jwt_required()
def book_seat():
    user = get_jwt_identity()
    data = request.json
    train_id = data.get("train_id")

    train = db.session.query(Train).filter_by(id=train_id).with_for_update().first()

    if not train or train.available_seats <= 0:
        return jsonify({"message": "No seats available"}), 400

    seat_number = train.total_seats - train.available_seats + 1
    train.available_seats -= 1
    new_booking = Booking(user_id=user['id'], train_id=train_id, seat_number=seat_number)

    db.session.add(new_booking)
    db.session.commit()

    return jsonify({"message": "Seat booked successfully", "seat_number": seat_number}), 201


# ✅ 6️⃣ Get Specific Booking Details
@routes.route('/booking_details/<int:booking_id>', methods=['GET'])
@jwt_required()
def booking_details(booking_id):
    user = get_jwt_identity()
    booking = Booking.query.filter_by(id=booking_id, user_id=user['id']).first()

    if not booking:
        return jsonify({"message": "Booking not found"}), 404

    train = Train.query.filter_by(id=booking.train_id).first()

    return jsonify({
        "booking_id": booking.id,
        "train_name": train.name,
        "source": train.source,
        "destination": train.destination,
        "seat_number": booking.seat_number
    }), 200
