// socket stuff



$(document).ready(function () {
    var socket = io.connect("http://127.0.0.1:5000/");
    console.log("connected")

    socket.on('connect', function () {
        socket.emit('my_event', "hello");
    });
});