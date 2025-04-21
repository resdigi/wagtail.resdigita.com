document.addEventListener("DOMContentLoaded", function () {
    const chatBox = document.getElementById("chat-box");
    const chatInput = document.getElementById("chat-input");
    const sendBtn = document.getElementById("send-btn");
    const chatClose = document.getElementById("chat-close");
    const chatContainer = chatBox.parentElement;

    function appendMessage(sender, text) {
        const messageElement = document.createElement("p");
        messageElement.className = "text-sm text-gray-300 mt-2";
        messageElement.innerHTML = `<strong>${sender}:</strong> ${text}`;
        chatBox.appendChild(messageElement);
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    sendBtn.addEventListener("click", function () {
        const userMessage = chatInput.value.trim();
        if (userMessage) {
            appendMessage("You", userMessage);
            chatInput.value = "";

            // Send message to Django backend
            fetch("{% url 'chat' %}", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": "{{ csrf_token }}",
                },
                body: JSON.stringify({ message: userMessage }),
            })
            .then(response => response.json())
            .then(data => {
                if (data.response) {
                    appendMessage("Bot", data.response);
                } else {
                    appendMessage("Bot", "Oops! Something went wrong.");
                }
            })
            .catch(error => {
                appendMessage("Bot", "Error connecting to chat.");
            });
        }
    });

    chatInput.addEventListener("keypress", function (event) {
        if (event.key === "Enter") {
            sendBtn.click();
        }
    });

    // Close chat
    chatClose.addEventListener("click", function () {
        chatContainer.style.display = "none";
    });
});

  