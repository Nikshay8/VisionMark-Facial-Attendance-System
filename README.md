# Face Recognition Attendance System

A Python-based attendance system that uses face recognition to mark student attendance automatically, with a MySQL database and a Tkinter GUI.

## Features
- Real-time face recognition using webcam
- Dynamic student registration with face-based duplicate detection
- MySQL database for persistent attendance records
- Simple GUI with 5 options: Start Attendance, Register Student, Today's Report, Date-wise Report, Student-wise Report

## Tech Stack
- Python
- OpenCV
- face_recognition (dlib)
- MySQL
- Tkinter

## Setup

1. Clone the repo
2. Install dependencies: pip install -r requirements.txt
3. Set up MySQL database using `Attendance System.sql`
4. Create a `.env` file with your database credentials:

DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=attendance_system

5. Run the GUI:

## How it works
- Click "Register New Student" to capture a face and add it to the database
- Click "Start Attendance" to open the webcam and mark attendance automatically
- Use the report buttons to view attendance analytics