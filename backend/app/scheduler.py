from apscheduler.schedulers.background import BackgroundScheduler
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time
import sqlite3  # Assuming you are using SQLite
from datetime import datetime

def send_email():
    sender_email = "frugalfinanceapp@gmail.com"
    password = "uwra usgn jmij raam" 
    receiver_email = "marktmaloney18@gmail.com"

    subject = "Test Email"
    body = "Log yo damn expenses boy"

    # Create the email
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    try:
        # Set up the SMTP server and send the email
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()  # Secure the connection
            server.login(sender_email, password)  # Login to the SMTP server
            server.sendmail(sender_email, receiver_email, message.as_string())  # Send the email
        print(f"Test email sent successfully to {receiver_email}!")
    except Exception as e:
        print(f"Failed to send email to {receiver_email}: {e}")

'''def send_email():
    # Database connection
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()

    # Get the current time
    current_time = datetime.now().time()

    # Fetch opted-in users whose notification time matches the current time
    cursor.execute("""
        SELECT email 
        FROM user 
        WHERE notifications = 1 
        AND notification_time = ?
    """, (current_time.strftime('%H:%M:%S'),))
    users = cursor.fetchall()

    conn.close()

    # Email sending logic (same as your current code)
    sender_email = "frugalfinanceapp@gmail.com"
    password = "Frugal1!"
    subject = "Daily Reminder"
    body = "Don't forget to log your expenses today!"

    for user in users:
        receiver_email = "marktmaloney18@gmail.com"
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = subject
        message.attach(MIMEText(body, "plain"))

        try:
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(sender_email, password)
                server.sendmail(sender_email, receiver_email, message.as_string())
            print(f"Email sent successfully to {receiver_email}!")
        except Exception as e:
            print(f"Failed to send email to {receiver_email}: {e}")'''


send_email()

# Create a scheduler
scheduler = BackgroundScheduler()
scheduler.add_job(send_email, 'interval', minutes=1)  # Check every minute
scheduler.start()

print("Scheduler started...")

# Keep the script running
try:
    while True:
        time.sleep(1)
except (KeyboardInterrupt, SystemExit):
    scheduler.shutdown()