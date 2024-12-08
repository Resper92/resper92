import os
from sqlalchemy import select

from celery import Celery
from conectdb import init_db, db_session
from model import Contract, Item


app = Celery(
    'task', broker=f'pyamqp://guest@{os.environ.get("RABBIT_HOST", "localhost")}//')


@app.task
def send_email(contract_id):
    init_db()
    contract = db_session.execute(
        select(Contract).filter_by(id=contract_id)).scalar()
    item = db_session.execute(
        select(Item).filter_by(id=contract.item)).scalar()
    import smtplib
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login("t6q8p@example.com", "mais2023")
    message = ("sdasdasdassd")
    s.sendmail("t6q8p@example.com", "t6q8p@example.com", message)
    s.sendmail("t6q8p@example.com", "t6q8p@example.com", message)
    s.quit()
