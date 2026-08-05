import tkinter as tk
from tkinter import messagebox
import subprocess
import sys
from datetime import datetime
from db import get_connection

def start_attendance():
    subprocess.run([sys.executable, "main.py"])

def register_student():
    subprocess.run([sys.executable, "register.py"])

def view_report():
    today = datetime.now().strftime("%Y-%m-%d")
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT students.name, attendance.time, attendance.status FROM attendance JOIN students ON attendance.student_id = students.id WHERE attendance.date = %s",
        (today,)
    )
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    if not rows:
        messagebox.showinfo("Today's Report", "No attendance marked today")
        return

    report = ""
    for name, time, status in rows:
        report += name + " - " + str(time) + " - " + status + "\n"

    messagebox.showinfo("Today's Report", report)

def datewise_report():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT date, COUNT(*) FROM attendance GROUP BY date ORDER BY date DESC"
    )
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    if not rows:
        messagebox.showinfo("Date-wise Report", "No records found")
        return

    report = ""
    for date, count in rows:
        report += str(date) + " - " + str(count) + " present\n"

    messagebox.showinfo("Date-wise Report", report)

def studentwise_report():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT students.name, COUNT(*) FROM attendance JOIN students ON attendance.student_id = students.id GROUP BY students.name"
    )
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    if not rows:
        messagebox.showinfo("Student-wise Report", "No records found")
        return

    report = ""
    for name, count in rows:
        report += name + " - " + str(count) + " days present\n"

    messagebox.showinfo("Student-wise Report", report)

root = tk.Tk()
root.title("Attendance System")
root.geometry("300x300")

tk.Button(root, text="Start Attendance", width=25, command=start_attendance).pack(pady=8)
tk.Button(root, text="Register New Student", width=25, command=register_student).pack(pady=8)
tk.Button(root, text="View Today's Report", width=25, command=view_report).pack(pady=8)
tk.Button(root, text="Date-wise Report", width=25, command=datewise_report).pack(pady=8)
tk.Button(root, text="Student-wise Report", width=25, command=studentwise_report).pack(pady=8)

root.mainloop()