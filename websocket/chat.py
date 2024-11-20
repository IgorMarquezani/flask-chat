import models.chat.repository as chat_repo
from multiprocessing import Process

chats: dict[str, dict[str, list[str]]] = {}

def handle_connection(ws, sender: str, target: str, repo: chat_repo.Repository):
    while True:
        data = ws.receive(timeout=2)
        if data is not None:
            repo.create_message(sender, target, data)

            if chats.get(sender + ":" + target) is None:
                chats[sender + ":" + target] = {}
            if chats.get(sender + ":" + target).get(target) is None:
                chats[sender + ":" + target][target] = []

            chats[sender + ":" + target][target].append(data)

        chat: dict[str, list[str]] = chats.get(sender + ":" + target)
        if chat is None:
            continue

        data = chat.get(target)
        if len(data) < 1:
            continue

        for message in data:
            ws.send(message)
            data.pop()