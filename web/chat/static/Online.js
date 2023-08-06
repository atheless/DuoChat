console.log("Loaded Online.js.");

const onlineSocket = new WebSocket(
    `wss://` + window.location.host + '/ws/onlinestatus/'
);

onlineSocket.onopen = function (e) {
    console.log("Successfully connected to the OnlineStatus.");
}


onlineSocket.onclose = function (e) {
    console.error('Online socket closed unexpectedly with error:', e);
};
