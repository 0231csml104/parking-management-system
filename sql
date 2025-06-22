CREATE DATABASE IF NOT EXISTS DBMSPROJECT11; 
USE DBMSPROJECT11; 
 -- Parking space info 
CREATE TABLE IF NOT EXISTS ParkingSpaces ( 
    space_id INT PRIMARY KEY AUTO_INCREMENT, 
    space_number VARCHAR(10), 
    is_occupied BOOLEAN DEFAULT FALSE 
); 
 -- Vehicle registry 
CREATE TABLE IF NOT EXISTS Vehicles ( 
    vehicle_id INT PRIMARY KEY AUTO_INCREMENT, 
    registration_number VARCHAR(20) UNIQUE, 
    vehicle_type VARCHAR(50), 
    owner_name VARCHAR(100) 
); 
 -- Entry/Exit records 
CREATE TABLE IF NOT EXISTS ParkingRecords ( 
    record_id INT AUTO_INCREMENT PRIMARY KEY, 
    vehicle_id INT, 
    space_id INT, 
    entry_time TIMESTAMP, 
    exit_time TIMESTAMP, 
    total_parking_duration INT, 
    FOREIGN KEY (vehicle_id) REFERENCES Vehicles(vehicle_id), 
    FOREIGN KEY (space_id) REFERENCES ParkingSpaces(space_id) 
); 
 -- Payment logs 
15 
 
CREATE TABLE IF NOT EXISTS PaymentRecords ( 
    payment_id INT AUTO_INCREMENT PRIMARY KEY, 
    record_id INT, 
    payment_amount DECIMAL(10, 2), 
    payment_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
    FOREIGN KEY (record_id) REFERENCES ParkingRecords(record_id) 
); 
 -- Sample spaces 
INSERT INTO parkingspacesParkingSpaces (space_number) VALUES  
('A1'), ('A2'), ('B1'), ('B2'), ('C1');
