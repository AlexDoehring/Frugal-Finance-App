from apscheduler.schedulers.background import BackgroundScheduler
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time
import sqlite3  # Assuming you are using SQLite

def send_email():
    # Database connection
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()

    # Fetch opted-in users
    cursor.execute("SELECT email FROM users WHERE notifications = 1")
    users = cursor.fetchall()

    # Close the database connection
    conn.close()

    sender_email = "frugalfinanceapp@gmail.com"
    password = "Frugal1!"

    subject = "Daily Update"
    body = "Don't forget to log your expenses today!"

    for user in users:
        receiver_email = user[0]

        # Create email
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = subject
        message.attach(MIMEText(body, "plain"))

        # Send email
        try:
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(sender_email, password)
                server.sendmail(sender_email, receiver_email, message.as_string())
            print(f"Email sent successfully to {receiver_email}!")
        except Exception as e:
            print(f"Failed to send email to {receiver_email}: {e}")

# Create a scheduler
scheduler = BackgroundScheduler()
scheduler.add_job(send_email, 'cron', hour=9, minute=0)  # Schedule daily at 9:00 AM
scheduler.start()

print("Scheduler started...")

# Keep the script running
try:
    while True:
        time.sleep(1)
except (KeyboardInterrupt, SystemExit):
    scheduler.shutdown()