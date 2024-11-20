from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from models.chat.chat import PrivateChat, PrivateMessage


class Repository:
    def __init__(self, db: Session):
        self.db = db

    def create_chat(self, userone: str, usertwo: str):
        cv = PrivateChat()
        cv.userone = userone
        cv.usertwo = usertwo
        self.db.add(cv)
        self.db.commit()

    def select_user_chats(self, username: str):
        stmt = select(PrivateChat).where(
            or_(
                PrivateChat.userone == username,
                PrivateChat.usertwo == username
            ))

        result = self.db.execute(stmt)

        chats = []
        for obj in result.scalars():
            chats.append(obj)

        return chats

    def create_message(self, sender: str, target: str, message: str):
        pm = PrivateMessage()
        pm.user = sender
        pm.target = target
        pm.data = message
        self.db.add(pm)
        self.db.commit()
