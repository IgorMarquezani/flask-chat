from datetime import datetime

from sqlalchemy import or_, select, update
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

    def create_message(self, pm: PrivateMessage) -> int:
        self.db.add(pm)
        self.db.commit()
        return pm.id

    def select_user_chats(self, username: str) -> list[PrivateChat]:
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

    def select_chat_messages(self, userone: str, usertwo: str) -> list[PrivateMessage]:
        stmt = select(PrivateMessage).where(
            or_(
                PrivateMessage.sender == userone and PrivateMessage.target == usertwo ,
                PrivateMessage.target == usertwo and PrivateMessage.sender == userone,
            )
        )

        result = self.db.execute(stmt)

        messages: list[PrivateMessage] = []
        for obj in result.scalars():
            obj.time = obj.time.strftime('%H:%M')
            messages.append(obj)

        return messages

    def update_read(self, id: int, read: bool) -> None:
        stmt = update(PrivateMessage).where(PrivateMessage.id == id).values(read=read)
        self.db.execute(stmt)
