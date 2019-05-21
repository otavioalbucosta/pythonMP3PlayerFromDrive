from socket import *
from tkinter import *
from hashlib import *


# # # CADASTRO # # #
def cadastro():
    usrnm = usrnm_entry.get()
    pswrd = pswrd_entry.get()
    msg = usrnm + " " + pswrd
    client_socket.send(msg.encode())


# # # LOGIN # # #
# envia as informacoes de login para o servidor
def login():
    usrnm = usrnm_entry.get()
    pswrd = pswrd_entry.get()
    msg = usrnm + " " + pswrd
    client_socket.send(msg.encode())


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

    usrnm_lbl = Label(login_window, text="Usuário:")
    usrnm_lbl.grid(row=0, column=0)
    usrnm_entry = Entry(login_window)
    usrnm_entry.grid(row=0, column=1)

    pswrd_lbl = Label(login_window, text="Senha")
    pswrd_lbl.grid(row=1, column=0)
    pswrd_entry = Entry(login_window, show="*")
    pswrd_entry.grid(row=1, column=1)

    login_btn = Button(login_window, text="Entrar", command=lambda: (login()), width=10)
    login_btn.grid(row=2, column=0)

    signup_btn = Button(login_window, text="Cadastrar", command=lambda: (cadastro()), width=10)
    signup_btn.grid(row=2, column=1)

    login_window.mainloop()
