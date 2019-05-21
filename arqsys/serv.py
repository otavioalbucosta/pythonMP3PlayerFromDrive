import wget
import os
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
clients = {}
addresses = {}

HOST = ''
PORT = 33000
BUFSIZ = 1024
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

def accept_incoming_connections():
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s se conectou." % client_address)
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()


def handle_client(client):
    name = client.recv(BUFSIZ).decode("utf-8")
    clients[client] = name
    while True:
        opt = client.recv(1024)
        opt = opt.decode('utf-8')
        print(opt)
        if opt == "1":
            wget.download('https://i.kym-cdn.com/photos/images/newsfeed/000/754/550/1a0.jpg', '/Users/Alunos/PycharmProjects/arqsys/DIO.jpg')
            f = open('DIO.jpg', 'rb')
            l = f.read(1024)
            while l:
                client.send(l)
                l = f.read(1024)
            f.close()
            print('Enviado com sucesso!!!')

        elif opt == "2":
            wget.download(
                'https://doc-00-4k-docs.googleusercontent.com/docs/securesc/r6somki3js115ngsdfp23uhgimhvv1br/fpski8amotihtlc2dg20jk65a4lq274c/1558454400000/03820570921577112760/03820570921577112760/1m6L-sPlERy3C_a68EhcvRqShsoypg5vp?e=download&nonce=s1p5jhh36fmri&user=03820570921577112760&hash=sm90keq9v1n3gd9c3rc0jm6h6oirntc3',
                '/Users/Alunos/PycharmProjects/arqsys/summer.mp3')
            print('Conectado a {}'.format(ADDR))
            f = open('summer.mp3', 'rb')
            l = f.read(1024)
            while l:
                client.send(l)
                l = f.read(1024)
            f.close()
            print('Enviado com sucesso!!!')

#def broadcast():









if __name__ == "__main__":
    SERVER.listen(5)
    print('Servidor de arquivos disponível. Aguardando conexão do cliente ...')
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()
    conn, addr = s.accept()


#exists = os.path.isfile('/path/to/file')