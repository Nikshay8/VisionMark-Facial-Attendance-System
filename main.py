import face_recognition
import cv2
import numpy as np
from datetime import datetime
from db import get_connection

video_capture = cv2.VideoCapture(0)

conn = get_connection()
cursor = conn.cursor()

cursor.execute("SELECT id, name, face_encoding_path FROM students")
rows = cursor.fetchall()

known_ids = []
known_face_encodings = []
known_face_names = []

for student_id, name, path in rows:
    if path:
        encoding = np.load(path)
        known_ids.append(student_id)
        known_face_encodings.append(encoding)
        known_face_names.append(name)

students = known_face_names.copy()

now = datetime.now()
current_date = now.strftime("%Y-%m-%d")

while True:
    _, frame = video_capture.read()
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        face_distance = face_recognition.face_distance(known_face_encodings, face_encoding)

        if len(face_distance) == 0:
            continue

        best_match_index = np.argmin(face_distance)

        name = "Unknown"
        student_id = None
        if matches[best_match_index]:
            name = known_face_names[best_match_index]
            student_id = known_ids[best_match_index]

        if name != "Unknown":
            cv2.putText(frame, name + " Present", (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 0, 0), 3, 2)

            if name in students:
                students.remove(name)
                current_time = now.strftime("%H:%M:%S")

                cursor.execute(
                    "SELECT * FROM attendance WHERE student_id = %s AND date = %s",
                    (student_id, current_date)
                )
                already_marked = cursor.fetchone()

                if already_marked is None:
                    cursor.execute(
                        "INSERT INTO attendance (student_id, date, time, status) VALUES (%s, %s, %s, %s)",
                        (student_id, current_date, current_time, "Present")
                    )
                    conn.commit()

    cv2.imshow("Attendance", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

video_capture.release()
cv2.destroyAllWindows()
cursor.close()
conn.close()