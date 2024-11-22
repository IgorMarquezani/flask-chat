from sqlalchemy.orm import Session

import models.chat.repository as chat_repo
from models.chat.chat import PrivateMessage
import models.session.repository as session_repo

private_message_queue: dict[str, list[PrivateMessage]] = {}

def private_chat(ws, sender: str, target: str, db_session: Session):
    chat_repository = chat_repo.Repository(db_session)
    session_repository = session_repo.Repository(db_session)

    while True:
        message = ws.receive(timeout=2)
        if message is not None:
            pm = PrivateMessage(sender, target, message)
            chat_repository.create_message(pm)

            if private_message_queue.get(target) is None:
                private_message_queue[target] = []

            private_message_queue[target].append(pm)

            try:
                session_repository.update_last_chat(sender, target)
            except Exception as e:
                print(e)

            print(message)

        chat = private_message_queue.get(sender)
        if chat is None or len(chat) == 0:
            continue

        for i, message in enumerate(chat):
            if message.sender == target:
                try:
                    ws.send(message.data)
                    chat_repository.update_read(message.id, True)
                    chat.pop(i)
                except Exception as e:
                    print(e)