const form = document.querySelector(".chat-form");
const chatHistory = document.querySelector(".chat-history");
const serverURL = "https://cognicoach-v2.carterleffen.repl.co"; // Replace this with the appropriate URL for your server
let chat_id = null;

form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const input = form.querySelector("input");
    const userMessage = input.value.trim();
    
    if (userMessage) {
        displayMessage(userMessage, "user");
        input.value = "";
        const chatbotResponse = await sendMessageToServer(userMessage);
        displayMessage(chatbotResponse, "chatbot");
    }
});

function displayMessage(message, sender) {
    const messageElement = document.createElement("li");
    messageElement.classList.add(sender === "user" ? "text-right" : "text-left");

    const emoji = sender === "user" ? "🙂" : "🤖";
    messageElement.innerHTML = `<span>${emoji} ${message}</span>`;
    chatHistory.appendChild(messageElement);
    chatHistory.scrollTop = chatHistory.scrollHeight;
}

async function sendMessageToServer(message) {
  if(chat_id == null) {
    console.log('Session not started... Cannot send to server');
    return;
  }
    try {
        const response = await fetch(serverURL + '/v1/chat/complete', {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message, chat_id})
        });
        if (!response.ok) {
            throw new Error("Failed to send message to the server");
        }
        const jsonResponse = await response.json();
        return jsonResponse.message;
    } catch (error) {
        console.error(error);
        return "Sorry, there was an error processing your message.";
    }
}

async function createNewChatSession() {
    try {
        const response = await fetch(serverURL + '/v1/chat/create', {
            method: "POST",
            headers: { "Content-Type": "application/json" },
        });
        if (!response.ok) {
            throw new Error("Failed to create a new chat session");
        }
        const jsonResponse = await response.json();
        chat_id = jsonResponse.chat_id;
        console.log("New chat session created:", chat_id);
    } catch (error) {
        console.log(error);
        alert("Sorry, there was an error creating a new chat session.");
    }
}

createNewChatSession();
