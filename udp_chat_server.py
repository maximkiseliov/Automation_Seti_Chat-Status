import socket
import time

host = '127.0.0.1'
port = 5000

clients = []
alias_status = []

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((host, port))
s.setblocking(0) #выключаем блокировку

quitting = False
print("Server started...")

while not quitting:
    try:
        data, addr = s.recvfrom(1024)
        alias = str(data.decode('utf-8')).split(":: ")
                  
        if addr not in clients:
            clients.append(addr)
                   
            
        if "Leave" in alias[1]:
            print (time.ctime(time.time()) + str(addr) + ": :" + str(alias[0]) + " LEAVES THE CHAT")
            alias_status.remove(alias[0])
            alias_online = ', '.join(alias_status)
            data = (str(alias[0]) + " LEAVES THE CHAT\n" + "Online users:\n" + str(alias_online))
        elif  alias[0] not in alias_status:
            alias_status.append(alias[0])
            alias_online = ', '.join(alias_status)
            print (time.ctime(time.time()) + str(addr) + ": :" + str(alias[0]) + " JOINS THE CHAT")
            print (time.ctime(time.time()) + str(addr) + ": :" + str(data.decode('utf-8')))
            data = (str(alias[0]) + " JOINS THE CHAT\n" + "Online users:\n" + str(alias_online)+ "\n" + str('@') + data.decode('utf-8'))
            
        else:
            print (time.ctime(time.time()) + str(addr) + ": :" + str(data.decode('utf-8')))
            data = (str('@') + data.decode('utf-8'))
                
        for client in clients:
            s.sendto(data.encode('utf-8'), client)

    except:
        pass
s.close()
            
