console.log("Sanity check from DuoChat.js.");

const UUID = JSON.parse(document.getElementById('DuoChat').textContent);

const userThis = JSON.parse(document.getElementById('User').textContent);

let chatLog = document.querySelector("#chatLog");
let chatMessageInput = document.querySelector("#chatMessageInput");
let chatMessageSend = document.querySelector("#chatMessageSend");
let onlineUsersSelector = document.querySelector("#onlineUsersSelector");


// focus 'chatMessageInput' when user opens the page
chatMessageInput.focus();

// submit if the user presses the enter key
chatMessageInput.onkeyup = function (e) {
    if (e.keyCode === 13) {  // enter key
        chatMessageSend.click();
    }
};

// clear the 'chatMessageInput' and forward the message
chatMessageSend.onclick = function () {
    if (chatMessageInput.value.length === 0) return;
    chatSocket.send(JSON.stringify({
        "message": chatMessageInput.value,
    }));
    chatMessageInput.value = "";
};

let chatSocket = null;

function connect() {

    chatSocket = new WebSocket("wss://" + window.location.host + "/ws/duochat/" + UUID + "/");

    chatSocket.onopen = function (e) {
        console.log("Successfully connected to the DuoChat.");
    }

    chatSocket.onclose = function (e) {
        console.log("WebSocket connection closed unexpectedly. Trying to reconnect in 4s...");
        setTimeout(function () {
            console.log("Reconnecting...");
            connect();
        }, 4000);
    };

    chatSocket.onmessage = function (e) {
        const data = JSON.parse(e.data);

        // console.log(data); // DEBUG

        switch (data.type) {
            case "chat_message":
                // chatLog.value += data.user + ": " + data.message + "\n";
                const chatMessageClass = data.user === userThis ? 'right mb-4' : 'left pb-4';
                console.log(chatMessageClass + "    userThis:" + userThis + "   data:   " + data.user)
                const messageHtml = `
                <div class="chat-message-${chatMessageClass}">
                    <div>
                        <img src="https://robohash.org/${data.user === userThis ? userThis : data.user}.png?gravatar=yes"
                             class="rounded-circle mr-1" alt="${data.user}" width="50" height="50">
                        <div class="text-muted small text-nowrap mt-2">${new Date().toLocaleTimeString()}</div>
                    </div>
                    
                    <div class="flex-shrink-1 bg-light rounded py-2 px-3 mr-3">
                        <div class="fw-bold mb-2">${data.user === userThis ? userThis + ' (You)' : data.user}</div>
                        ${data.message}
                    </div>
                    
                </div>
            `;
                chatLog.innerHTML += DOMPurify.sanitize(messageHtml);
                break;


            case "previous_messages":
                for (let i = 0; i < data.messages.length; i++) {
                    var TimeStamp = new Date(data.messages[i].timestamp)
                    const weekday = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];

                    // chatLog.value += "[" + Date("c.timestamp").toString() + "] " + c.user + ": " + c.content + "\n";
                    const chatMessageClass = data.messages[i].author === userThis ? 'right mb-4' : 'left pb-4';
                    const messageHtml = `
                <div class="chat-message-${chatMessageClass}">
                    <div>
                        <img src="https://robohash.org/${data.messages[i].author}.png?gravatar=yes"
                             class="rounded-circle mr-1" alt="${data.messages[i].author}" width="60" height="60">
                    </div>
                    
                    <div class="flex-shrink-1 bg-light rounded py-2 px-3 mr-3">
                        <div class="fw-bold mb-2">${data.messages[i].author === userThis ? userThis + ' (You)' : data.messages[i].author}</div>
                        ${data.messages[i].content}
                        <div class="text-muted small text-nowrap mt-2">${''.concat(weekday[TimeStamp.getDay()], ' ', TimeStamp.getHours(), ':', TimeStamp.getMinutes(), ':', TimeStamp.getSeconds(), '  ', TimeStamp.getDate(), '/', TimeStamp.getMonth(), '/', TimeStamp.getFullYear())}</div>
                    </div>
                    
                    
                </div>
            `;

                    chatLog.innerHTML += messageHtml;


                }
                chatLog.innerHTML += `<div class="hr-sect">Previous messages</div>`;


                break;
            case "chat_typing":
                if (data.user !== userThis) {
                    document.querySelector('#typingID').innerHTML = 'Typing...'
                }

                break;

            case "chat_stop_typing":
                if (data.user !== userThis) {
                    document.querySelector('#typingID').innerHTML = ' '
                }
                break;
            default:
                console.error("Unknown message type!");
                break;
        }

        // scroll 'chatLog' to the bottom
        chatLog.scrollTop = chatLog.scrollHeight;
    };

    chatSocket.onerror = function (err) {
        console.log("WebSocket encountered an error: " + err.message);
        console.log("Closing the socket.");
        chatSocket.close();
    }


    const input = document.getElementById('chatMessageInput');
    let timeout;
    const delay = 900;


    setTimeout(() => {
        input.addEventListener('keyup', () => {
            console.log('Typing');


            chatSocket.send(JSON.stringify({
                "message": "typing",
                "user": userThis,
            }));


            clearTimeout(timeout);
            timeout = setTimeout(() => {
                console.log('User stopped typing');

                chatSocket.send(JSON.stringify({
                    "message": "stop_typing",
                    "user": userThis,
                }));

            }, delay);
        });

    }, 1000);


}


connect();





