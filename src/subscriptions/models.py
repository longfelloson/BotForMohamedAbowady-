from datetime import datetime

from typing import List

from sqlalchemy import Column, Integer, String, DateTime

from src.database import Base
from src.subscriptions.schemas import SubscriptionStatus


class Subscription(Base):
    __tablename__ = 'subscriptions'

    id_ = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    status = Column(String, default=SubscriptionStatus.ACTIVE)
    expires_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    subscription_time = Column(String)

    def to_dict(self, keys: List[str] = None) -> dict:
        if keys:
            return {k: getattr(self, k) for k in keys}
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}



