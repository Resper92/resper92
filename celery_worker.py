import os
import smtplib
from email.mime.text import MIMEText
from celery import Celery
from sqlalchemy import select
from conectdb import init_db, db_session
from model import Contract, Item


app = Celery('tasks', broker='pyamqp://guest@localhost//')


@app.task
def send_email(contract_id):
    init_db()
    contract = db_session.execute(
        select(Contract).filter_by(contract=contract_id)).scalar()
    item = db_session.execute(
        select(Item).filter_by(id=Contract.item)).scalar()
    import smtplib
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.quit()
