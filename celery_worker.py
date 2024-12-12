import os
import smtplib
from email.mime.text import MIMEText
from celery import Celery
from sqlalchemy import select
from conectdb import init_db, db_session
from model import Contract, Item

# ... (configurazioni Celery)


@Celery.task
def send_email(contract):
    try:
        init_db()
        contrac = db_session.query(Contract).get(contract)
        if contrac:
            message = MIMEText('new contract')
            message['From'] = os.environ.get('EMAIL_SENDER')  # (Consider secure storage)
            message['To'] = os.environ.get('EMAIL_RECIPIENT')  # (Consider secure storage)
            message['Subject'] = 'Nuovo contratto'

            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(os.environ.get('EMAIL_USER'), os.environ.get('EMAIL_PASSWORD'))  # (Consider secure storage)
                smtp.sendmail(message['From'], message['To'], message.as_string())
        else:
            print(f"Contract with ID {id} not found")
    except Exception as e:
        # Implement more specific error handling (e.g., smtplib.exceptions)
        print(f"Errore durante l'invio dell'email: {str(e)}")