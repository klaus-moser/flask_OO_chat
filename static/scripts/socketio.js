document.addEventListener('DOMContentLoaded', () => {
    var socket = io();

    socket.on('connect', function() {
        socket.send("LOL");
    });

    socket.on('message', data => {
        console.log(`Message received: ${data}`)
    })
})