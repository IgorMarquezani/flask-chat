const sendMessage = (e) => {
    if (e.type === "keypress" && e.key !== "Enter") {
        return
    }

    const messageInput = document.getElementById("message-input")
    const text = messageInput.value
    if (text.length < 1) {
        return
    }

    chat.send(text)
    messageInput.value = ""

    const chatBox = document.getElementById("chat-box")
    const now = new Date()
    const div = document.createElement("div")
    div.className = "message sent align-self-end"
    div.innerHTML = `
                        <p class="mb-0">${text}</p>
                        <small class="text-muted">${now.getHours()}</small>
        `
    chatBox.append(div)
}

document.getElementById("send-message-btn").addEventListener("click", sendMessage)
document.getElementById("message-text-field").addEventListener("keypress", sendMessage)