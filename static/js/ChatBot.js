const chatbotIcon = document.getElementById("chatbotIcon");
const chatbotModal = document.getElementById("chatbotModal");
const closeModal = document.getElementById("closeModal");
const userInput = document.getElementById("userInput");
const submitBtn = document.getElementById("submitBtn");

// Open modal when chatbot icon is clicked
chatbotIcon.onclick = function() {
    chatbotModal.style.display = "block"; // Use chatbotModal instead of modal
    userInput.value = ""; // Clear input field
    userInput.focus(); // Focus on input field
    loadRecentChats(); // Load recent chats when the modal opens
}

// Close modal when close button is clicked
closeModal.onclick = function() {
    chatbotModal.style.display = "none"; // Use chatbotModal instead of modal
}

// Close modal when clicking outside of the modal
window.onclick = function(event) {
    if (event.target === chatbotModal) {
        chatbotModal.style.display = "none"; // Use chatbotModal instead of modal
    }
}

function scrollToBottom() {
    const conversationHistory = document.querySelector('.conversation-history');
    conversationHistory.scrollTop = conversationHistory.scrollHeight;
}

// Function to add user and bot messages to the conversation history
function addMessage(userMessage, botResponse) {
    const conversationHistory = document.getElementById("conversationHistory");

    // Create user message element
    const userMessageElement = document.createElement('div');
    userMessageElement.className = 'user-query';
    userMessageElement.innerHTML = `<b>You</b><br><br> ${userMessage}`;

    // Create bot response element
    const botResponseElement = document.createElement('div');
    botResponseElement.className = 'bot-response';
    botResponseElement.innerHTML = `<b>AirBuddy </b><br><br>${botResponse}`; // Replace with actual bot response

    // Append messages to the conversation history
    conversationHistory.appendChild(userMessageElement);
    conversationHistory.appendChild(botResponseElement);

    // Scroll to the bottom
    scrollToBottom();
}

// Function to load recent chats from the server
function loadRecentChats() {
    fetch('/load_chats')
        .then(response => response.json())
        .then(data => {
            const { recent_chats } = data;
            const conversationHistory = document.getElementById("conversationHistory");
            conversationHistory.innerHTML = ''; // Clear current history

            recent_chats.forEach(chat => {
                const [userMessage, botResponse] = chat;
                addMessage(userMessage, botResponse);
            });
        })
        .catch(error => console.error('Error loading chats:', error));
}

// Handle user input on submit
submitBtn.onclick = function() {
    const userMessage = userInput.value;
    if (userMessage) {
        // Send message to server
        fetch('/send_message', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message: userMessage })
        })
        .then(response => response.json())
        .then(data => {
            const { response: botResponse } = data;
            addMessage(userMessage, botResponse); // Add user and bot messages
            userInput.value = ""; // Clear input field and refocus
            userInput.focus();
        })
        .catch(error => console.error('Error sending message:', error));
    }
}
