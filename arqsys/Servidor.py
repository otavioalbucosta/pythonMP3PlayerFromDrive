from socket import *
from threading import *
from wget import *
from pickle import *


# # # REGISTRA NOVO USUARIO # # #
def registro(client_socket):
    print("\033[1;33mregistro()")
    usrnm = client_socket.recv(MAX_BYTES).decode()
    pswrd = client_socket.recv(MAX_BYTES)
    print("\033[1;33mUsuario: %s\t| Senha: %s" % (usrnm, pswrd))
    pswrd = str(pswrd)
    usuario = {usrnm: pswrd}
    print("\033[1;31mD: ", usuario)
    with open("usuarios.pickle", "ab") as lista_usuarios:
        dump(usuario, lista_usuarios)


# # # CHECA CREDENCIAIS DO USUARIO # # #
def autenticacao(client_socket):
    print("\033[1;33m autenticacao()")
    usrnm = client_socket.recv(MAX_BYTES).decode()
    pswrd = client_socket.recv(MAX_BYTES)
    print("\033[1;33mUsuario: %s\t| Senha: %s" % (usrnm, pswrd))

    usuarios = {}
    try:
        with open("usuarios.pickle", "rb") as lista_usuarios:
            while True:
                try:
                    usuarios.update(load(lista_usuarios))
                except EOFError:
                    break
            
            try:
                print("\033[1;31mpswrd = ", pswrd)
                print("\033[1;31musuarios[usrnm] = ", usuarios[usrnm])
                print("\033[1;31mpswrd == usuarios[usrnm] ? ",pswrd == usuarios[usrnm])
                if pswrd  == usuarios[usrnm]:
                    print("\033[1;33ma")
                    client_socket.send("{LOGIN_SUCCESS}".encode())
                else:
                    print("\033[1;33mb")
                    client_socket.send("{LOGIN_FAILED}".encode())
            except KeyError:
                print("\033[1;33mc")
                client_socket.send("ACCOUNT_NOT_FOUND}".encode())
    except FileNotFoundError:
        print("\033[1;33md")
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
