from datetime import datetime

from sqlalchemy import Integer, String, Column, ForeignKey, Time, Boolean, func
from database.database import db

class PrivateChat(db.Model):
    userone = Column(String, ForeignKey('user.username'), primary_key=True, nullable=False)
    usertwo = Column(String, ForeignKey('user.username'), primary_key=True, nullable=False)

class PrivateMessage(db.Model):
    id = Column(Integer, primary_key=True)
    sender = Column(String, ForeignKey("user.username"), nullable=False)
    target = Column(String, ForeignKey("user.username"), nullable=False)
    data = Column(String, nullable=False)
    time = Column(Time, nullable=False, server_default=func.current_time())
    read = Column(Boolean, nullable=False, default=False)

    def __init__(self, sender: str | None, target: str | None, data: str | None):
        self.sender = sender
        self.target = target
        self.data = data