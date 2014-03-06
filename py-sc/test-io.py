from socketIO_client import SocketIO

with SocketIO('localhost', 3002) as socketIO:
    socketIO.emit('event',"moi moi moui")
    socketIO.wait(seconds=1)
