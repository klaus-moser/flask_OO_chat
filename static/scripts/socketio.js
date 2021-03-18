document.addEventListener('DOMContentLoaded', () => {
    var socket = io();

    // Display connect status message
    socket.on('connect', function() {
        document.querySelector('#display-message-section').append('Connected!');
    });

    // Display received data aka text
    socket.on('message', data => {

        // Create paragraph, break, username element
        const p = document.createElement('p');
        const br = document.createElement('br');
        const span_username = document.createElement('span');

        // Set the inner html to the message text & username
        span_username.innerHTML = data.username;
        p.innerHTML = span_username.outerHTML + br.outerHTML +  data.msg + br.outerHTML;

        // Append the text to the area where the messages are displayed
        document.querySelector('#display-message-section').append(p);
    })

    // Event listener for clicks
    document.querySelector('#send_message').onclick = () => {
        // Send message
        socket.send({'msg': document.querySelector('#user_message').value,
            'username': username});
    }
})