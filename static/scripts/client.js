// client.js
const socket = new WebSocket('ws://127.0.0.1:55555');

socket.onmessage = function(event) {
    const messageBox = document.getElementById('chat-box');
    messageBox.innerHTML += `<div>${event.data}</div>`;
    messageBox.scrollTop = messageBox.scrollHeight;
};



function sendMessage() {
    // Get the message input element
    var messageInput = document.getElementById("message-input");

    // Get the value of the input field
    var message = messageInput.value;

    // Create a new div element to display the message
    var messageDiv = document.createElement("div");
    messageDiv.textContent = message;

    // Append the message div to the chat box
    var chatBox = document.getElementById("chat-box");
    chatBox.appendChild(messageDiv);

    // Clear the input field after sending the message
    messageInput.value = "";
}
