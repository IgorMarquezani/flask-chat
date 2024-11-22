from sqlalchemy import update, Result, select
from sqlalchemy.orm import Session
from models.session.session import Session as UserSession


class Repository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, session: UserSession):
        self.db.add(session)
        self.db.commit()

    def select_last_chat(self, username: str) -> str:
        stmt = select(UserSession.last_chat).where(UserSession.username == username)
        with self.db.execute(stmt) as result:
            return result.first().last_chat

    def update_last_chat(self, username: str, chat: str):
        stmt = (update(UserSession).
                where(UserSession.username == username).
                values(last_chat=chat)
        )
        result = self.db.execute(stmt)
        result.close()
