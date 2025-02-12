# 🚆 IRCTC Railway Management System

## 📌 Project Overview
This is a **Railway Management System** built using **Python Flask** and **PostgreSQL**. It allows users to **register, login, check train availability, book seats, and retrieve booking details**. Admins can add new trains using an API key authentication system.

---

## 🛠 Tech Stack
- **Backend:** Flask, Flask-SQLAlchemy, Flask-JWT-Extended, Flask-Bcrypt
- **Database:** PostgreSQL
- **Authentication:** JWT (JSON Web Token) + API Key Authentication
- **ORM:** SQLAlchemy
- **Hosting:** Localhost (can be deployed to a cloud service)

---

## 🚀 Features
### 🔹 User Management
- User Registration (Admin/User roles)
- User Login (JWT Authentication)

### 🔹 Train Management
- Admin can add new trains
- Get train seat availability
- Book a seat on a train
- View booking details

---

## 📦 Installation & Setup

### 1️⃣ **Clone the Repository**
```bash
git clone https://github.com/anuragkumar5130/irctc-management.git
cd irctc-management
```

### 2️⃣ **Create Virtual Environment & Install Dependencies**
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
pip install -r requirements.txt
```

### 3️⃣ **Set Up PostgreSQL Database**
Update `config.py` with your PostgreSQL credentials:
```python
class Config:
    SECRET_KEY = 'your_secret_key'
    SQLALCHEMY_DATABASE_URI = 'postgresql://username:password@host/database_name'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ADMIN_API_KEY = 'your_admin_api_key'
```

### 4️⃣ **Initialize Database**
```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

### 5️⃣ **Run the Flask Server**
```bash
flask run
```
Your API will be available at `http://127.0.0.1:5000/`

---

## 📌 API Endpoints

### 1️⃣ **User Registration**
**Endpoint:** `POST /register`
```json
{
  "username": "john_doe",
  "password": "securepassword",
  "role": "admin"  // or "user"
}
```

### 2️⃣ **User Login**
**Endpoint:** `POST /login`
```json
{
  "username": "john_doe",
  "password": "securepassword"
}
```
**Response:**
```json
{
  "access_token": "your_jwt_token"
}
```

### 3️⃣ **Add Train (Admin Only)**
**Endpoint:** `POST /add_train`
**Headers:**
```json
{
  "Authorization": "Bearer your_jwt_token",
  "X-API-KEY": "your_admin_api_key"
}
```
**Request Body:**
```json
{
  "name": "Express 101",
  "source": "New York",
  "destination": "Boston",
  "total_seats": 200
}
```

### 4️⃣ **Check Seat Availability**
**Endpoint:** `GET /seat_availability?source=New York&destination=Boston`
**Response:**
```json
[
  { "train_id": 1, "name": "Express 101", "available_seats": 150 }
]
```

### 5️⃣ **Book a Seat**
**Endpoint:** `POST /book_seat`
**Headers:**
```json
{
  "Authorization": "Bearer your_jwt_token"
}
```
**Request Body:**
```json
{
  "train_id": 1
}
```
**Response:**
```json
{
  "message": "Seat booked successfully",
  "seat_number": 51
}
```

### 6️⃣ **Get Booking Details**
**Endpoint:** `GET /booking_details/{booking_id}`
**Headers:**
```json
{
  "Authorization": "Bearer your_jwt_token"
}
```
**Response:**
```json
{
  "booking_id": 12,
  "train_name": "Express 101",
  "source": "New York",
  "destination": "Boston",
  "seat_number": 51
}
```

---

## 🔍 Debugging & Common Issues
- **403 Forbidden on `/add_train`?**
  - Ensure `X-API-KEY` is included in the headers and matches `ADMIN_API_KEY` in `config.py`.
- **ModuleNotFoundError for Flask packages?**
  - Run `pip install -r requirements.txt` inside the virtual environment.
- **Flask `db` command not found?**
  - Ensure Flask-Migrate is installed: `pip install flask-migrate`.

---

---

## ✨ Contributors
- **[Anurag Kumar]** - Developer
- Contributions are welcome! Feel free to submit a pull request.

---

## 📬 Contact
For any questions or suggestions, feel free to contact me at **anuragendgame69@gmail.com**.



