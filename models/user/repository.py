import sqlalchemy

from models.user.user import User

class Repository():
    db: sqlalchemy.orm.Session

    def __init__(self, db: sqlalchemy.orm.Session):
        self.db = db

    def create(self, user: User):
        self.db.add(user)
        self.db.commit()

    def get_by_name(self, name: str) -> User:
        return self.db.query(User).filter_by(username=name).first()

