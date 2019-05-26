import os
from socket import *
from tkinter import *
from hashlib import *
from logging import *
from tkinter import ttk

import pygame as pygame

import quickstarter


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

# AQUI TODA VEZ QUE VOCE CLICA NUMA MUSICA NO LISTBOX ELE VAI VER SE A MUSICA VAI ESTAR BAIXADA
# SE NAO ELE RECEBE DO SERVER
def onselect(*args, **kwargs):

    songname=temp[Listbox1.curselection()[0]]
    print(temp[Listbox1.curselection()[0]])
    if os.path.isfile('ClientSongs/{}.mp3'.format(songname)):
        pygame.mixer.music.load('ClientSongs/{}.mp3'.format(songname))
    else:
        client_socket.send("{}.mp3".format(songname).encode('utf-8'))
        with open("ClientSongs/{}.mp3".format(songname),"wb") as file:
            print('file opened')
            while True:
                data = client_socket.recv(1024)
                if not data:
                    break
                file.write(data)
        pygame.mixer.music.load('ClientSongs/{}.mp3'.format(songname))
        pygame.mixer.music.play()


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
            login_window.destroy() # ESSE DESTROY AQUI É O QUE FAZ IR PRO MP3
        elif answr == "{LOGIN_FAILED}":
            print("\033[1;31msem tempo, irmão")
        elif answr == "{ACCOUNT_NOT_FOUND}":
            print("\033[1;31mtu não é meu brother")
        else:
            print("\033[1;31mque porra é essa")


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
login_window.protocol("WM_DELETE_WINDOW", lambda :exit()) #caso você desligue a tela de login ele não vai pro mp3
login_window.mainloop()

# DAQUI PRA BAIXO É O TKINTER DO PLAYER DE MUSICA
root = Tk()
pygame.mixer.init()
root.geometry("600x450+445+140")
root.title("New Toplevel")
root.configure(background="#d9d9d9")
root.configure(highlightbackground="#d9d9d9")
root.configure(highlightcolor="black")

temp = []
for item in quickstarter.listFiles():
    if '.mp3' in item['name']:
        temp.append(item['name'].split(".")[0])
print(temp)
list = StringVar()
list.set(temp)
print(list.get())
'''This class configures and populates the toplevel window.
   top is the toplevel containing window.'''
_bgcolor = '#d9d9d9'  # X11 color: 'gray85'
_fgcolor = '#000000'  # X11 color: 'black'
_compcolor = '#d9d9d9'  # X11 color: 'gray85'
_ana1color = '#d9d9d9'  # X11 color: 'gray85'
_ana2color = '#ececec'  # Closest X11 color: 'gray92'
font9 = "-family {Segoe UI} -size 13 -weight normal -slant " \
        "roman -underline 0 -overstrike 0"
style = ttk.Style()
if sys.platform == "win32":
    style.theme_use('winnative')

style.configure('.', background=_bgcolor)
style.configure('.', foreground=_fgcolor)
style.configure('.', font="TkDefaultFont")
style.map('.', background=
[('selected', _compcolor), ('active', _ana2color)])

Label1 = Label(root)
Label1.place(relx=0.4, rely=-0.089, height=101, width=344)
Label1.configure(activebackground="#f9f9f9")
Label1.configure(activeforeground="black")
Label1.configure(background="#d9d9d9")
Label1.configure(disabledforeground="#a3a3a3")
Label1.configure(foreground="#000000")
Label1.configure(highlightbackground="#d9d9d9")
Label1.configure(highlightcolor="black")
Label1.configure(text='''Olá! Escolha na lista à sua esquerda a música que desejas tocar!''')

TScale1 = ttk.Scale(root, from_=0, to=100)
TScale1.place(relx=0.5, rely=0.667, relwidth=0.383, relheight=0.0
              , height=26, bordermode='ignore')
TScale1.configure(value="5")
TScale1.configure(takefocus="")

TFrame1 = ttk.Frame(root)
TFrame1.place(relx=0.517, rely=0.111, relheight=0.433
              , relwidth=0.358)
TFrame1.configure(relief='groove')
TFrame1.configure(borderwidth="2")
TFrame1.configure(relief="groove")
TFrame1.configure(width=215)
img = PhotoImage()

Button1 = Button(root)
Button1.place(relx=0.517, rely=0.756, height=34, width=41)
Button1.configure(activebackground="#ececec")
Button1.configure(activeforeground="#000000")
Button1.configure(background="#d9d9d9")
Button1.configure(disabledforeground="#a3a3a3")
Button1.configure(foreground="#000000")
Button1.configure(highlightbackground="#d9d9d9")
Button1.configure(highlightcolor="black")
Button1.configure(pady="0")
Button1.configure(text='''⧏⧏''')

Button2 = Button(root)
Button2.place(relx=0.65, rely=0.756, height=34, width=67)
Button2.configure(activebackground="#ececec")
Button2.configure(activeforeground="#000000")
Button2.configure(background="#d9d9d9")
Button2.configure(disabledforeground="#a3a3a3")
Button2.configure(font=font9)
Button2.configure(foreground="#000000")
Button2.configure(highlightbackground="#d9d9d9")
Button2.configure(highlightcolor="black")
Button2.configure(pady="0")
Button2.configure(text='''ll / ▷''')

Button3 = Button(root)
Button3.place(relx=0.833, rely=0.756, height=34, width=41)
Button3.configure(activebackground="#ececec")
Button3.configure(activeforeground="#000000")
Button3.configure(background="#d9d9d9")
Button3.configure(disabledforeground="#a3a3a3")
Button3.configure(foreground="#000000")
Button3.configure(highlightbackground="#d9d9d9")
Button3.configure(highlightcolor="black")
Button3.configure(pady="0")
Button3.configure(text='''⧐⧐''')

Listbox1 = Listbox(root)
Listbox1.place(relx=0.0, rely=0.0, relheight=0.982, relwidth=0.373)
Listbox1.configure(background="white")
Listbox1.configure(disabledforeground="#a3a3a3")
Listbox1.configure(font="TkFixedFont")
Listbox1.configure(foreground="#000000")
Listbox1.configure(takefocus="0")
Listbox1.configure(width=224)
Listbox1.configure(selectmode='browse')
sb = Scrollbar(Listbox1, orient="vertical")
sb.config(command=Listbox1.yview)
sb.pack(side='right', fill='y')
Listbox1.configure(listvariable=list)
Listbox1.bind('<<ListboxSelect>>', onselect)
root.mainloop()

