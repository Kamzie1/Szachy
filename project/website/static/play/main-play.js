let socket = io();

const leave = document.getElementById('leave');

leave.addEventListener('click', function(){
    socket.emit('cancel');
    window.location.href = '/'
}); 