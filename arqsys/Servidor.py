from socket import *
from threading import *
from wget import *


# # # REGISTRA NOVO USUARIO # # #
def registro(client_socket):
    print("\033[1;33mregistro()")
    usrnm = client_socket.recv(MAX_BYTES).decode()
    pswrd = client_socket.recv(MAX_BYTES)
    print("\033[1;33mUsuario: %s\t| Senha: %s" % (usrnm, pswrd))
    pswrd = str(pswrd)
    usuario = {usrnm: {"usrnm": usrnm, "pswrd": pswrd}}
    with open("usuarios.txt", "a") as lista_usuarios:
        write(usuario, lista_usuarios)


# # # CHECA CREDENCIAIS DO USUARIO # # #
def autenticacao(client_socket):
    print("\033[1;33m autenticacao()")
    usrnm = client_socket.recv(MAX_BYTES).decode()
    pswrd = client_socket.recv(MAX_BYTES)
    print("\033[1;33mUsuario: %s\t| Senha: %s" % (usrnm, pswrd))

    usuario = {usrnm: {"usrnm": usrnm, "pswrd": str(pswrd)}}

    try:
        with open("usuarios.json", "r") as lista_usuarios:
            usuarios = load(lista_usuarios)
            if usrnm in usuarios:
                if usuarios[usrnm]["pswrd"] == pswrd:
                    client_socket.send("{LOGIN_SUCCESS}".encode())
                else:
                    client_socket.send("{LOGIN_FAILED}".encode())
            else:
                client_socket.send("{ACCOUNT_NOT_FOUND}".encode())
    except FileNotFoundError:
        client_socket.send("{ACCOUNT_NOT_FOUND}".encode())


def aguarda_requisicao(client_socket):
    while True:
        request = client_socket.recv(MAX_BYTES).decode()
        print("\033[1;33m" + request)

        if request == "{LOGIN_REQUEST}":
            print("\033[1;33m" + request)
            client_socket.send("{REQUEST_ACCEPTED}".encode())
            autenticacao(client_socket)
        elif request == "{SIGN_IN_REQUEST}":
            print("\033[1;33m" + request)
            client_socket.send("{REQUEST_ACCEPTED}".encode())
            registro(client_socket)


# # # CONECTA COM VARIOS CLIENTES # # #
def espera_conexao():
    while True:
        client_socket, client_address = server_socket.accept()
        print("\033[1;33mConectado com", client_address)

        t = Thread(target=lambda: (aguarda_requisicao(client_socket)))
        t.start()


# # # MAIN # # #
if __name__ == '__main__':
    SERVER_ADDRESS = (gethostname(), 54321)
    MAX_BYTES = 1024

    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.bind(SERVER_ADDRESS)
    server_socket.listen(5)
    print("\033[1;33mEm espera...")

    espera_conexao()
