
async function sendMessage() {
    const userInput = document.getElementById('chat-input').value; 
    const chatOutput = document.getElementById('chat-output');   
  
    if (userInput.trim() === '') {
      alert('Please type a message.');
      return;
    }
  

    const userMessage = document.createElement('p');
    userMessage.textContent = `You: ${userInput}`;
    userMessage.style.color = 'blue';
    chatOutput.appendChild(userMessage);
  
    try {
      const response = await fetch('http://localhost:5000/response', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query: userInput }),
      });
  
      const data = await response.json();
      const botMessage = document.createElement('p');
  
      // Display the bot's response or error message
      if (data.response) {
        botMessage.textContent = `Bot: ${data.response}`;
      } else {
        botMessage.textContent = 'Bot: Something went wrong.';
      }
  
      chatOutput.appendChild(botMessage);
    } catch (error) {
      const errorMessage = document.createElement('p');
      errorMessage.textContent = 'Error: Unable to connect to the server.';
      chatOutput.appendChild(errorMessage);
    }
  
    // Scroll to the bottom of the chat area
    chatOutput.scrollTop = chatOutput.scrollHeight;
  
    // Clear the input field
    document.getElementById('chat-input').value = '';
  }
  
  // Attach event listener to the "Send" button
  document.getElementById('send-btn').addEventListener('click', sendMessage);
  

/*This code belongs to Priyanshi Sinha*/
