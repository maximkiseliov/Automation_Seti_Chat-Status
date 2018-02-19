import socket
import threading #связывание
import time

tLock = threading.Lock()
shutdown = False

def receiving(name, sock):
    while not shutdown:
        try:
            tLock.acquire()
            while True:
                data, addr = sock.recvfrom(1024)
                print(str(data.decode('utf-8')))
        except:
            pass
        finally:
            tLock.release()

host = '127.0.0.1'
port = 0 # любой свободный порт

server = ('127.0.0.1', 5000)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((host, port))
s.setblocking(0) #выключаем блокировке

rT = threading.Thread(target = receiving, args=("RecvThread", s))
rT.start()

alias = str(input("Name: "))
message = str(input(alias + "-> "))
while True:
    if message != '':
        s.sendto(alias.encode('utf-8') + ":: ".encode('utf-8')+ message.encode('utf-8'), server)
    if message == "Leave":
        shutdown = True
        break
    tLock.acquire()
    message = str(input(alias + "-> "))
    tLock.release()
    time.sleep(0.1)
    
shutdown = True
rT.join()
s.close()
