document.addEventListener('DOMContentLoaded', () => {

    // Init socketIO
    let socket = io();
    let room = 'Lounge'; // default room
    joinRoom(room); // join after login in

    // Display connect status message
    socket.on('connect', function() {
        document.querySelector('#display-message-section').append('Connected!');
    });

    // Display received data aka messages
    socket.on('message', data => {

        // Create paragraph, break, username element
        const p = document.createElement('p');
        const br = document.createElement('br');
        const span_username = document.createElement('span');
        const span_timestamp = document.createElement('span');

        // Check if message is normal message or a SysMsg
        if (data.username){
            // Set the inner html to the message text, username & timestamp
            span_username.innerHTML = data.username;
            span_timestamp.innerHTML = data.time_stamp;
            p.innerHTML = span_username.outerHTML + br.outerHTML +  data.msg + br.outerHTML + span_timestamp.outerHTML;

            // Append the text to the area where the messages are displayed
            document.querySelector('#display-message-section').append(p);
        } else {
            printSysMsg(data.msg);
        }
    });

    // Send message
    document.querySelector('#send_message').onclick = () => {
        socket.send({'msg': document.querySelector('#user_message').value,
            'username': username, 'time_stamp': "", 'room': room});

        // Clear input area
        document.querySelector('#user_message').value = '';
    }

    // Room selection
    document.querySelectorAll('#select-room').forEach(p => {
        p.onclick = () => {

            // Room the user wants to join
            let newRoom = p.innerHTML;
            console.log(newRoom);
            console.log(room)
            // Check if user is already in the selected room
            if (newRoom == room){
                // Error notification
                msg = `You are already in ${room} room.`
                printSysMsg(msg);

            } else {
                // Leave current room: msg to server leave()
                leaveRoom(room);
                // Join new room: msg to server join()
                joinRoom(newRoom);
                room = newRoom;
            }
        }
    });

    // Leave room
    function leaveRoom(room) {
        // msg to server: leave()
        socket.emit('leave', {'username': username, 'room': room});
    }

    // Join the room
    function joinRoom(room) {
        // msg to server: join()
        socket.emit('join', {'username': username, 'room': room});

        // Clear message area
        document.querySelector('#display-message-section').innerHTML = '';

        // Autofocus on input box
        document.querySelector('#user_message').focus();
    }

    // Print system messages
    function printSysMsg(msg) {
        const p = document.createElement('p');
        p.innerHTML = msg;
        document.querySelector('#display-message-section').append(p);
    }
})