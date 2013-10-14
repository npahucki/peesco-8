import socket

#Open port and listen
#create an INET, STREAMing socket
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind((socket.gethostname(), 1335))
serversocket.listen(5)

client, address = serversocket.accept() 
while 1: 
    data = client.recv(1) 
    if data: 
        print data 
