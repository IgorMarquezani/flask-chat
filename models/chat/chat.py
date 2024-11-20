from sqlalchemy import Integer, String, Column, ForeignKey
from database.database import db

class PrivateChat(db.Model):
    userone = Column(String, ForeignKey('user.username'), primary_key=True, nullable=False)
    usertwo = Column(String, ForeignKey('user.username'), primary_key=True, nullable=False)

class PrivateMessage(db.Model):
    id = Column(Integer, primary_key=True)
    user = Column(String, ForeignKey("user.username"), nullable=False)
    target = Column(String, ForeignKey("user.username"), nullable=False)
    data = Column(String, nullable=False)