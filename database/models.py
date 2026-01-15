from sqlalchemy import Column, Integer,  DateTime, BigInteger, Text,  Date,    ForeignKey
from datetime import datetime

from .db import Base


class Clients(Base):
    __tablename__ = 'clients'

    id = Column(Integer, primary_key=True)
    telegram_id = Column(BigInteger, unique=True)
    full_name = Column(Text)
    status = Column(Text, default="active")
    phone_number = Column(Text, default=0)

    created_at = Column(DateTime, default=datetime.utcnow)


class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True)

    client_id = Column(BigInteger, ForeignKey("clients.id"), index=True)

    amount = Column(Integer)
    due_date = Column(Date)  # дата оплаты

    status = Column(Text, default="pending", index=True)

    last_notification_at = Column(DateTime)

    created_at = Column(DateTime, default=datetime.utcnow)


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True)

    client_id = Column(BigInteger, ForeignKey("clients.id"), index=True)
    subscription_id = Column(Integer, ForeignKey("subscriptions.id"))

    payment_id = Column(Text)
    payment_url = Column(Text)

    amount = Column(Integer)
    status = Column(Text, default="pending")  # pending / succeeded / canceled

    created_at = Column(DateTime, default=datetime.utcnow)


class Admin(Base):
    __tablename__ = "admins"

    id = Column(Integer, primary_key=True)
    telegram_id = Column(BigInteger, index=True)