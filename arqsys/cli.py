import socket
host = '127.0.0.1'
port = 33000
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))
op=input("Digite 1 para receber foto, 2 para música")
s.send(op.encode('utf-8'))

if op=='1':

    with open('recebido.jpg', 'wb+') as f:
        print('file opened')
        while True:
            data = s.recv(1024)
            if not data:
                break
            f.write(data)
        f.close()
        print('Transferência completa!!!')
        s.close()
        print('Conexão encerrada.')
elif op=='2':

    with open('recebido.mp3', 'wb+') as f:
        print('file opened')
        while True:
            data = s.recv(1024)
            if not data:
                break
            f.write(data)
        f.close()
        print('Transferência completa!!!')
        s.close()
        print('Conexão encerrada.')