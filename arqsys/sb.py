import socket

SERVER_ADDRESS = (socket.gethostname(), 54321)
MAX_BYTES = 1024

# # # SOCKET CLIENTE # # #
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(SERVER_ADDRESS)
with open("ClientSongs/atlas.mp3", "wb") as f:
    print('file opened')
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        f.write(data)
    f.close()