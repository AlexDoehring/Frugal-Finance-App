# tasks.py
from flask_mail import Mail, Message
from celery_app import make_celery
from flask import current_app as app
from .models import User
from datetime import datetime
from app import mail, celery

mail = Mail(app)
celery = make_celery(app)

@celery.task
def send_reminder_email(user_id): #sending an email with flask mail and celery 
    with app.app_context(): 
        user = User.query.get(user_id) #get user from the database 
        if user and user.notifications:
            msg = Message(  #create email message 
                'Expense Reminder',
                recipients=[user.email],
                body=f"Hi {user.username},\n\nThis is a friendly reminder to log your expenses for today."
            )
            mail.send(msg) #send email 

@celery.task
def schedule_notifications(): #runs every minute to check which users should be notified
    with app.app_context():
        current_time = datetime.now().time().replace(second=0, microsecond=0) #get current time hours and mins only
        users_to_notify = User.query.filter(
            User.notifications == True,
            User.notification_time == current_time
        ).all() #gets all users who have opted for notifications at that time

        for user in users_to_notify: #queue email task for users opted in 
            send_reminder_email.delay(user.id)