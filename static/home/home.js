const startChat = (userone) => {
    let usertwo = document.getElementById("start-chat-modal-input").value
    let err = document.getElementById("start-chat-error")
    let message = document.getElementById("start-chat-message")

    err.innerHTML = ""
    message.innerHTML = ""

    fetch(`/chat/create/${userone}/${usertwo}`, {
        method: "POST",
        cors: "no-cors"
    }).then((resp) => {
        if (resp.status === 200) {
            message.innerHTML = "chat created"

            let chatsListDiv = document.getElementById("chats-list")
            const a = document.createElement("a")
            a.className = "list-group-item list-group-item-action d-flex align-items-center chat"
            a.innerHTML = `
                        <img src="https://via.placeholder.com/50" alt="Profile" class="profile-pic me-3">
                        <div class="flex-grow-1">
                            <h5 class="mb-1">${usertwo}</h5>
                            <small>Última mensagem recebida...</small>
                        </div>
                        <small class="text-muted">12:45</small>
      `
            chatsListDiv.append(a)

        } else if (resp.status === 400) {
            resp.text().then((text) => {
                err.innerHTML = text
            })
        } else {
            resp.text().then((text) => {
                err.innerHTML = "unexpected error" + text
                console.log("unexpected error: " + text)
            })
        }
    })
}

let chat = 0

const createWebsocket = (target) => {
    chat = new WebSocket('ws://' + window.location.host + `/websocket/create?target=${target}`);
    //chat = new WebSocket('ws://' + window.location.host + `/echo`);
    console.log("starting websocket")

    const chatBox = document.getElementById("chat-box")

    chat.onmessage = (e) => {
        const now = new Date()
        const div = document.createElement("div")
        div.className = "message received align-self-start"
        div.innerHTML = `
                        <p class="mb-0">${e.data}</p>
                        <small class="text-muted">${now.getHours()}</small>
        `
        chatBox.append(div)
        console.log(e.data)
    };

    chat.onclose = (e)  => {
        console.error(`Chat socket closed. Status ${e.code}. Message: ${e.reason}`);
    };
}
