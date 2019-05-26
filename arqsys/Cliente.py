from socket import *
from tkinter import *
from hashlib import *
from logging import *

# # # CADASTRO # # #
def cadastro():
    usrnm = usrnm_entry.get()
    pswrd = sha256()
    pswrd.update(pswrd_entry.get().encode())
    pswrd = pswrd.digest()
    print("\033[1;33m------CADASTRO------")
    print("\033[1;33mUsuario: ", usrnm)
    print("\033[1;33mSenha: ", pswrd_entry.get())
    print("\033[1;33mHash: ", pswrd)
    client_socket.send("{SIGN_IN_REQUEST}".encode())
    answr = client_socket.recv(1024).decode()
    print("\033[1;33m" + answr)
    if answr == "{REQUEST_ACCEPTED}":
        client_socket.send(usrnm.encode())
        client_socket.send(pswrd)


# # # LOGIN # # #
# envia as informacoes de login para o servidor
def login():
    usrnm = usrnm_entry.get()
    pswrd = sha256()
    pswrd.update(pswrd_entry.get().encode())
    pswrd = pswrd.digest()
    print("\033[1;33m------LOGIN------")
    print("\033[1;33mUsuario: ", usrnm)
    print("\033[1;33mSenha: ", pswrd_entry.get())
    print("\033[1;33mHash: ", pswrd)
    client_socket.send("{LOGIN_REQUEST}".encode())
    answr = client_socket.recv(MAX_BYTES).decode()
    if answr == "{REQUEST_ACCEPTED}":
        client_socket.send(usrnm.encode())
        client_socket.send(pswrd)

        answr = client_socket.recv(MAX_BYTES).decode()
        if answr == "{LOGIN_SUCCESS}":
            print("\033[1;32mvdc, brother")
        elif answr == "{LOGIN_FAILED}":
            print("\033[1;31msem tempo, irmão")
        elif answr == "{ACCOUNT_NOT_FOUND}":
            print("\033[1;31mtu não é meu brother")
        else:
            print("\033[1;31mque porra é essa")


# # # MAIN # # #
if __name__ == '__main__':

    SERVER_ADDRESS = (gethostname(), 54321)
    MAX_BYTES = 1024

    # # # SOCKET CLIENTE # # #
    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect(SERVER_ADDRESS)

    # # # JANELA LOGIN # # #
    login_window = Tk()
    login_window.title("Login")
    login_window.resizable(False, False)

    usrnm_lbl = Label(login_window, text="Usuário:", width=10)
    usrnm_lbl.grid(row=0, column=0)
    usrnm_entry = Entry(login_window, width=12)
    usrnm_entry.grid(row=0, column=1)

    pswrd_lbl = Label(login_window, text="Senha", width=10)
    pswrd_lbl.grid(row=1, column=0)
    pswrd_entry = Entry(login_window, show="*", width=12)
    pswrd_entry.grid(row=1, column=1)

    login_btn = Button(login_window, text="Entrar", command=lambda: (login()), width=10)
    login_btn.grid(row=2, column=0)

    signup_btn = Button(login_window, text="Cadastrar", command=lambda: (cadastro()), width=10)
    signup_btn.grid(row=2, column=1)

login_window.mainloop()
