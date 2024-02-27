function handleKeyPress(event) {
    // Check if the pressed key is Enter (key code 13)
    if (event.keyCode === 13) {
        // Prevent the default Enter key behavior (new line)
        event.preventDefault();
        // Simulate a click on the send button
        sendMessage();
    }
}
function sendMessage() {
    // Update the dynamic suggestions in the HTML
    var suggestionButtons = document.querySelectorAll('.d-flex.flex-column.align-items-start .suggestion-btn');

    // Remove each suggestion button
    suggestionButtons.forEach(function(button) {
        button.remove();
    });

    // Apply CSS to #chatOutput
    var chatOutput = document.getElementById('chatOutput');
        chatOutput.classList.add('afterSendMessage'); // Add class afterSendMessage
    
   

    var userMessage = document.getElementById("userMessage").value;
    var chatOutput = document.getElementById("chatOutput");
    var placeholderText = document.querySelector('.placeholder-text');
    if (placeholderText) {
        placeholderText.remove(); // Remove the placeholder text
    }

    // Create a container for the user message
    var userMessageContainer = document.createElement("div");
    userMessageContainer.classList.add("message-container");

    // Create a strong element for the "You" label
    var youLabel = document.createElement("strong");
    youLabel.classList.add("user-message");
    youLabel.innerHTML = "You";

    // Create a span element for the user message
    var userMessageSpan = document.createElement("span");
    userMessageSpan.classList.add("message");
    userMessageSpan.innerHTML = userMessage;

    // Append the "You" label and the user message to the userMessageContainer
    userMessageContainer.appendChild(youLabel);
    userMessageContainer.appendChild(document.createElement("br")); // Add line break
    userMessageContainer.appendChild(userMessageSpan);

    // Create a container for the loading message
    var loadingMessageContainer = document.createElement("div");
    loadingMessageContainer.classList.add("message-container");
    loadingMessageContainer.innerHTML = '<strong class="message">Ruedex is typing</strong>';

    // Append the user message container to the chat output
    chatOutput.appendChild(userMessageContainer);
    // Append the loading message to the chat output
    chatOutput.appendChild(loadingMessageContainer);

    // Function to add dots to the loading message
    function addDots() {
        // Get the message span element
        var messageSpan = loadingMessageContainer.querySelector('.message');
        
        // Get the current text content
        var currentText = messageSpan.textContent;
        
        // Limit the dots to three
        if (currentText.endsWith('....')) {
            // Reset text content if it already ends with four dots
            messageSpan.innerHTML = '<strong class="message">Ruedex is typing</strong>';
        } else {
            // Add a dot to the text content
            messageSpan.innerHTML += '<strong style="font-size: 1.2em;">.</strong>';
        }
    }
    
    // Interval to add dots every second (adjust interval as needed)
    var dotInterval = setInterval(addDots, 1000);

    // Append the user message container to the chat output
    chatOutput.appendChild(userMessageContainer);
    // Append the loading message to the chat output
    chatOutput.appendChild(loadingMessageContainer);

    // Make an API request to get AI response
    fetch('/get_ai_response', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ userMessage: userMessage })
    })
    .then(response => response.json())
    .then(data => {
        // Remove the loading message
        chatOutput.removeChild(loadingMessageContainer);

        var aiMessageContainer = document.createElement("div");
        aiMessageContainer.classList.add("message-container");

        // Create a strong element for the AI message label
        var aiLabel = document.createElement("strong");
        aiLabel.classList.add("ai-message");
        aiLabel.innerHTML = "&#129302; RUEDEX-AI";

        // Create a span element for the AI response
        var aiResponseSpan = document.createElement("span");
        aiResponseSpan.classList.add("message");
        aiResponseSpan.innerHTML = data.aiResponse;

        // Append the AI message label and the AI response to the aiMessageContainer
        aiMessageContainer.appendChild(aiLabel);
        
        aiMessageContainer.appendChild(document.createElement("br")); // Add line break
        aiMessageContainer.appendChild(aiResponseSpan);
        aiMessageContainer.appendChild(document.createElement("hr"));
        // Append the AI message container to the chat output
        chatOutput.appendChild(aiMessageContainer);
        

        // Scroll to the bottom of the chat
        chatOutput.scrollTop = chatOutput.scrollHeight;
    })
    .catch(error => console.error('Error:', error));

    
    // Scroll to the bottom of the chat
    chatOutput.scrollTop = chatOutput.scrollHeight;

    // Clear the input field
    document.getElementById("userMessage").value = '';
}


function openChat(topic) {
    var chatContainerId = 'chat' + topic.replace(/[^a-zA-Z0-9]/g, '');
    var chatContainer = document.getElementById(chatContainerId);

    console.log('Chat Container ID:', chatContainerId); // Log the generated ID
    console.log('Chat Container:', chatContainer); // Log the chat container to the console

    if (chatContainer) {
        // Toggle visibility of chat container
        chatContainer.style.display = chatContainer.style.display === 'block' ? 'none' : 'block';

        // If the chat container is visible, trigger the chatbot
        if (chatContainer.style.display === 'block') {
            console.log('Opening chat for topic:', topic);
            initChatBot(chatContainerId, topic);
        }
    } else {
        console.error('Chat Container not found for ID:', chatContainerId);
    }
}


function selectSuggestion(userMessage) {
    
    // Update the dynamic suggestions in the HTML
    var suggestionButtons = document.querySelectorAll('.d-flex.flex-column.align-items-start .suggestion-btn');

    // Remove each suggestion button
    suggestionButtons.forEach(function(button) {
        button.remove();
    });
    // Apply CSS to #chatOutput
    var chatOutput = document.getElementById('chatOutput');
        chatOutput.classList.add('afterSendMessage'); // Add class afterSendMessage
    
    var chatOutput = document.getElementById("chatOutput");
    var placeholderText = document.querySelector('.placeholder-text');
    if (placeholderText) {
        placeholderText.remove(); // Remove the placeholder text
    }
    
    var userMessageContainer = document.createElement("div");
    userMessageContainer.classList.add("message-container");

    // Create a strong element for the "You" label
    var youLabel = document.createElement("strong");
    youLabel.classList.add("user-message");
    youLabel.textContent = "You";

    // Create a span element for the user message
    var userMessageSpan = document.createElement("span");
    userMessageSpan.classList.add("message");
    userMessageSpan.textContent = userMessage;

    // Append the "You" label and the user message to the userMessageContainer
    userMessageContainer.appendChild(youLabel);
    userMessageContainer.appendChild(document.createElement("br")); // Add line break
    userMessageContainer.appendChild(userMessageSpan);

    // Create a container for the loading message
    var loadingMessageContainer = document.createElement("div");
    loadingMessageContainer.classList.add("message-container");
    loadingMessageContainer.innerHTML = '<span class="message">Ruedex is typing....</span>';

    // Append the user message container to the chat output
    chatOutput.appendChild(userMessageContainer);
    // Append the loading message to the chat output
    chatOutput.appendChild(loadingMessageContainer);
    // Make an API request to get AI response
    fetch('/get_ai_response', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ section: userMessage })
    })
    .then(response => response.json())
    .then(data => {
        // Remove the loading message
        chatOutput.removeChild(loadingMessageContainer);

        // Create a container for the AI message
    var aiMessageContainer = document.createElement("div");
    aiMessageContainer.classList.add("message-container");

    // Create a strong element for the AI message label
    var aiLabel = document.createElement("strong");
    aiLabel.classList.add("ai-message");
    aiLabel.innerHTML = "&#129302; RUEDEX-AI";

    // Create a span element for the AI response
    var aiResponseSpan = document.createElement("span");
    aiResponseSpan.classList.add("message");
    aiResponseSpan.innerHTML = data.aiResponse;

    // Append the AI message label and the AI response to the aiMessageContainer
    aiMessageContainer.appendChild(aiLabel);
    
    aiMessageContainer.appendChild(document.createElement("br")); // Add line break
  
    aiMessageContainer.appendChild(aiResponseSpan);
    aiMessageContainer.appendChild(document.createElement("hr"));
    // Append the AI message container to the chat output
    chatOutput.appendChild(aiMessageContainer);

        // Scroll to the bottom of the chat
        chatOutput.scrollTop = chatOutput.scrollHeight;
    })
    .catch(error => console.error('Error:', error));

    
    // Scroll to the bottom of the chat
    chatOutput.scrollTop = chatOutput.scrollHeight;

    // Clear the input field
    document.getElementById("userMessage").value = '';
}

document.addEventListener("DOMContentLoaded", function() {
    // Add the 'bubble-up' class to each button group
    document.getElementById("button-group-1").classList.add("bubble-up");
    document.getElementById("button-group-2").classList.add("bubble-up");
});


// Add event listener for page refresh
window.onbeforeunload = function() {
    // Send request to clear session
    fetch('/clear_session', {
        method: 'GET'
    })
    .then(response => response.json())
    .then(data => console.log(data.message))
    .catch(error => console.error('Error:', error));
};