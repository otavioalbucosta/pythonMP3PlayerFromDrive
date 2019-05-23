from socket import *
from threading import *
from wget import *
from hashlib import *
from json import *


# # # CHECA CREDENCIAIS DO USUARIO # # #
def autenticacao(client_socket, client_address):
    msg = client_socket.recv(MAX_BYTES).decode().split()
    usrnm = msg[0]
    pswrd = msg[1]
    print(usrnm, "está conectado(o)")

    usuario = {usrnm: {"usrnm": usrnm, "pswrd": pswrd}}
    try:
        with open("usuarios.json", "r") as lista_usuarios:
            usuarios = load(lista_usuarios)
            if usrnm in lista_usuarios:
                if lista_usuarios[usrnm]["pswrd"] == pswrd:
                    print("acertô, mizerávi")
                else:
                    print("ta errado, otário!")
            else:
                with open("usuarios.json", "r") as lista_usuarios:
                    dump(usuario, lista_usuarios)
    except FileNotFoundError:
        with open("usuarios.json", "w") as lista_usuarios:
            dump(usuario, lista_usuarios)

# # # CONECTA COM VARIOS CLIENTES # # #
def espera_conexao():
    while True:
        client_socket, client_address = server_socket.accept()
        print("Conectado com", client_address)

        t = Thread(target=lambda: (autenticacao(client_socket, client_address)))
        t.start()


# # # MAIN # # #
if __name__ == '__main__':
    SERVER_ADDRESS = (gethostname(), 54321)
    MAX_BYTES = 1024

    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.bind(SERVER_ADDRESS)
    server_socket.listen(5)

    espera_conexao()
