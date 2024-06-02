from datetime import datetime

from sqlalchemy import Column, Integer, ForeignKey, DateTime, String

from src.database import Base
from src.payments.schemas import PaymentStatus


class Payment(Base):
    __tablename__ = 'payments'

    id_ = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id_'), nullable=False)
    message_id = Column(Integer, nullable=False)
    amount = Column(Integer, nullable=False)
    currency = Column(String, default='USD')
    created_at = Column(DateTime, default=datetime.now)
    paid_at = Column(DateTime)
    status = Column(Integer, nullable=False, default=PaymentStatus.NOT_PAID)
    subscription_period = Column(String, nullable=False)
