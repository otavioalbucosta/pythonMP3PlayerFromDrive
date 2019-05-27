import socket
SERVER_ADDRESS = (socket.gethostname(), 54321)
MAX_BYTES = 1024
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(SERVER_ADDRESS)
server_socket.listen(5)
client_socket, client_address = server_socket.accept()
with open('Songs/atlas.mp3','rb') as f:
    data = f.read(1024)
    client_socket.send(data)
    while data:
        data=f.read(1024)
        client_socket.send(data)
    f.close()