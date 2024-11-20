const sendMessage = () => {
    const messageInput = document.getElementById("message-input")
    const text = messageInput.value
    if (text.length > 0) {
        chat.send(text)
    }
}

document.getElementById("send-message-btn").addEventListener("click", sendMessage)