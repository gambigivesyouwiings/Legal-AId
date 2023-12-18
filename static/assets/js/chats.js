document.getElementById("messageForm").addEventListener("submit", function(event) {
    event.preventDefault();
    let currentDate = new Date();
    let cDay = currentDate.getDate()
    let cMonth = currentDate.getMonth() + 1
    let cYear = currentDate.getFullYear()
    let cHour = currentDate.getHours()
    let cMinute = currentDate.getMinutes()
    let daynight = "AM"
    if (cHour >= 12) {
        daynight = "PM"
        cHour = cHour - 12

    }
    time = cHour + ":" + cMinute + " " + daynight + " | " + cDay + "/" + cMonth + "/" + cYear
    var form = document.getElementById("messageForm");
    // Get the message content from the input field
    var messageContent = document.getElementsByName("messageContent")[0].value;
    console.log(messageContent);

    // Display the outgoing message in the chat container
    displayOutgoingMessage(messageContent);

    // Assuming you use AJAX to send the message to the server
    // Replace the following with your actual server-side logic
    // For demonstration, we'll just log the message content to the console
    const url = '/get_chat';
    let data = new FormData(form);
    //displayIncomingMessages('just a moment')
    fetch(url, {
  method: 'POST',
  body: data
  }).then(response => response.text())
  .then(response => displayIncomingMessages(response))
  .then(response => console.log(response))
  .catch(function(error) {
    console.log(error);
  });
    // Clear the input field after sending the message
    document.getElementsByName("messageContent")[0].value = "";
  })

  // Function to display outgoing messages in the chat container
function displayOutgoingMessage(content) {
    var chatContainer = document.querySelector(".chat-page .msg-inbox .chats .msg-page ");

    // Create elements for the outgoing message
    var outgoingMessageDiv = document.createElement("div");
    outgoingMessageDiv.className = "outgoing-chats";

    var outgoingImageDiv = document.createElement("div");
    outgoingImageDiv.className = "outgoing-chats-img";
    outgoingImageDiv.innerHTML = '<img src="static/assets/img/apple-touch-icon.png" />';

    var outgoingMsgDiv = document.createElement("div");
    outgoingMsgDiv.className = "outgoing-msg";
    outgoingMsgDiv.innerHTML = '<div class="outgoing-chats-msg"><p>' + content + '</p> <span class="time">' + time + '</span></div>';

    // Append elements to the chat container
    outgoingMessageDiv.appendChild(outgoingImageDiv);
    outgoingMessageDiv.appendChild(outgoingMsgDiv);
    chatContainer.appendChild(outgoingMessageDiv);
  }
  // Function to display incoming messages in the chat container
  function displayIncomingMessages(response) {
    var chatContainer = document.querySelector(".chats .msg-page");

    // Create elements for the incoming message
    var incomingMessageDiv = document.createElement("div");
    incomingMessageDiv.className = "received-chats";

    var incomingImageDiv = document.createElement("div");
    incomingImageDiv.className = "received-chats-img";
    incomingImageDiv.innerHTML = "<img src='static/assets/img/openai.jpg'/>" ;

    var incomingMsgDiv = document.createElement("div");
    incomingMsgDiv.className = "received-msg";
    incomingMsgDiv.innerHTML = '<div class="received-msg-inbox"><p>' + response + '</p> <span class="time">' + time + '</span></div>';

    // Append elements to the chat container
    incomingMessageDiv.appendChild(incomingImageDiv);
    incomingMessageDiv.appendChild(incomingMsgDiv);
    chatContainer.appendChild(incomingMessageDiv);
  }
  ;
