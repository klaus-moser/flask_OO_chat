document.addEventListener('DOMContentLoaded', () => {
    // Init socketIO
    let socket = io();

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
        const span_timestamp = document.createElement('span');

        // Set the inner html to the message text, username & timestamp
        span_username.innerHTML = data.username;
        span_timestamp.innerHTML = data.time_stamp;
        p.innerHTML = span_username.outerHTML + br.outerHTML +  data.msg + br.outerHTML + span_timestamp.outerHTML;

        // Append the text to the area where the messages are displayed
        document.querySelector('#display-message-section').append(p);
    })

    // Event listener for clicks
    document.querySelector('#send_message').onclick = () => {
        // Send message
        socket.send({'msg': document.querySelector('#user_message').value,
            'username': username, 'time_stamp': ""});
    }
})