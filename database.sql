-- Create the database (Run this separately if needed)
CREATE DATABASE irctc;

-- Use the database
\c irctc;

-- Create Users Table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role VARCHAR(10) CHECK (role IN ('admin', 'user')) NOT NULL
);

-- Create Trains Table
CREATE TABLE trains (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    source VARCHAR(50) NOT NULL,
    destination VARCHAR(50) NOT NULL,
    total_seats INT NOT NULL,
    available_seats INT NOT NULL
);

-- Create Bookings Table
CREATE TABLE bookings (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    train_id INT REFERENCES trains(id) ON DELETE CASCADE,
    seat_number INT UNIQUE NOT NULL
);
