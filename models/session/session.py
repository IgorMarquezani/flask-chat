from sqlalchemy import String, Column, ForeignKey

from database.database import db

class Session(db.Model):
    key_access = Column(String, unique=True)
    username = Column(String, ForeignKey('user.username'), primary_key=True)
    ip_address = Column(String, nullable=False)
    last_chat = Column(String)

    def __init__(self, key_access: str, username: str, ip_address: str):
        self.key_access = key_access
        self.username = username
        self.ip_address = ip_address