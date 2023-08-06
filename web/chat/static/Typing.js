
    var typingSocket = new WebSocket(
        `wss://` + window.location.host + '/ws/typing/'
    );
    typingSocket.onmessage = function(e) {
        const data = JSON.parse(e.data);
        if(data.reciever_is_typing && data.is_typing){
            document.querySelector('#reciever-status').innerHTML =
            `
                <span class="font-weight-bold text-warning font-size-sm">typing...</span>
            `
        }
    };

    typingSocket.onclose = function(e) {
        console.error('Chat socket closed unexpectedly with error:', e);
    };