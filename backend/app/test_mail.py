from flask_mail import Mail, Message
from flask import Flask

app = Flask(__name__)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'frugalfinanceapp@gmail.com'
app.config['MAIL_PASSWORD'] = 'Frugal1!'

mail = Mail(app)

with app.app_context():
    msg = Message(
        'Test Email',
        sender=app.config['MAIL_USERNAME'],
        recipients=['marktmaloney18@gmail.dom'],
        body='This is a test email.'
    )
    
try:
    mail.send(msg)
    print("Email sent successfully!")
except Exception as e:
    print(f"Failed to send email: {e}")