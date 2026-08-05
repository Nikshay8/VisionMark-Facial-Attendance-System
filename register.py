import cv2
import os
import face_recognition
import numpy as np
from db import get_connection

video_capture = cv2.VideoCapture(0)

print("Press 's' to capture photo, 'q' to quit without saving")

while True:
    ret, frame = video_capture.read()
    cv2.imshow("Register New Student", frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord("s"):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        encodings = face_recognition.face_encodings(rgb_frame)

        if len(encodings) == 0:
            print("No face detected, try again")
            continue

        new_encoding = encodings[0]

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT name, face_encoding_path FROM students")
        existing = cursor.fetchall()

        already_registered = False
        for name, path in existing:
            if path and os.path.exists(path):
                known_encoding = np.load(path)
                match = face_recognition.compare_faces([known_encoding], new_encoding)[0]
                if match:
                    print("Already registered as: " + name)
                    already_registered = True
                    break

        if already_registered:
            cursor.close()
            conn.close()
            continue

        name = input("Enter student name: ")

        image_path = os.path.join("faces", name + ".jpg")
        cv2.imwrite(image_path, frame)

        encoding_path = os.path.join("encodings", name + ".npy")
        os.makedirs("encodings", exist_ok=True)
        np.save(encoding_path, new_encoding)

        cursor.execute(
            "INSERT INTO students (name, face_encoding_path) VALUES (%s, %s)",
            (name, encoding_path)
        )
        conn.commit()
        cursor.close()
        conn.close()

        print(name + " registered successfully!")
        break

    if key == ord("q"):
        break

video_capture.release()
cv2.destroyAllWindows()