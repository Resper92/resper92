from sqlalchemy import Column, Integer, String, ForeignKey, REAL, DateTime, func
import datetime
from sqlalchemy.orm import mapped_column
from conectdb import Base


class User(Base):
    __tablename__ = 'user'
    user_id = Column(Integer, primary_key=True)
    login = Column(String(50))
    password = Column(String(50))
    ipn = Column(String(50))
    full_name = Column(String(50))
    contacts = Column(String(120))
    photo = Column(String(120))
    passport = Column(String(120), unique=True)
    email = Column(String(200), nullable=True)

    def init(self, login=None, password=None, ipn=None, full_name=None, contacts=None, photo=None, passport=None, email=None):
        self.login = login
        self.password = password
        self.ipn = ipn
        self.full_name = full_name
        self.contacts = contacts
        self.photo = photo
        self.passport = passport
        self.email = email

class Item(Base):
    __tablename__ = 'item'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    photo = Column(String(120))
    description = Column(String(200))
    price_hour = Column(REAL)
    price_day = Column(REAL)
    price_week = Column(REAL)
    price_month = Column(REAL)
    owner = mapped_column(ForeignKey('user.user_id'))

    def __init__(self, name=None, photo=None, description=None, price_hour=None, price_day=None, price_week=None, price_month=None, owner=None):
        self.name = name
        self.photo = photo
        self.description = description
        self.price_hour = price_hour
        self.price_day = price_day
        self.price_week = price_week
        self.price_month = price_month
        self.owner = owner


class Contract(Base):
    __tablename__ = 'contract'
    contract = Column(Integer, primary_key=True)
    text = Column(String(200))
    start_date = Column(String(50))
    end_date = Column(String(50))
    leaser = mapped_column(ForeignKey('user.user_id'))
    taker = mapped_column(ForeignKey('user.user_id'))
    item = mapped_column(ForeignKey('item.id'))

    def __init__(self, text=None, start_date=None, end_date=None, leaser=None, taker=None, item=None):
        self.text = text
        self.start_date = start_date
        self.end_date = end_date
        self.leaser = leaser
        self.taker = taker
        self.item = item


class Feedback(Base):
    __tablename__ = 'feedback'
    id = Column(Integer, primary_key=True)
    author = mapped_column(ForeignKey('user.user_id'))
    user = mapped_column(ForeignKey('user.user_id'))
    grade = Column(Integer)
    contract = mapped_column(ForeignKey('contract.contract'))

    def __init__(self, author=None, user=None, grade=None, contract=None):
        self.author = author
        self.user = user
        self.grade = grade
        self.contract = contract


class Favorite(Base):
    __tablename__ = 'favorites'
    id = Column(Integer, primary_key=True)
    user = mapped_column(ForeignKey('user.user_id'))
    item = mapped_column(ForeignKey('item.id'))

    def __init__(self, user=None, item=None):
        self.user = user
        self.item = item


class Search_history(Base):
    __tablename__ = 'search_history'
    id = Column(Integer, primary_key=True)
    user = mapped_column(ForeignKey('user.user_id'))
    search_text = Column(String(50))
    timestamp = Column(String(50))

    def __init__(self, user=None, search_text=None, timestamp=None):
        self.user = user
        self.search_text = search_text
        self.timestamp = timestamp

    def __repr__(self):
        return f'<User {self.name!r}>'
