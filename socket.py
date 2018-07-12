from socket import *

s1=socket(AF_INET,SOCK_DGRAM)
s1.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
s1.bind(('192.168.1.253',12345))

import socket
s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s2.bind(('192.168.1.253',5204))
s2.listen(1)
conn, addr = s2.accept()
print('Connected by', addr)

while True:
    data = conn.recv(1024)
    if not data: break
    print(data.decode('utf-8'))   
    s1.sendto(b'0 talk to 1', ('192.168.1.79',12345))
    m=s1.recvfrom(1024)
    print(m[0].decode('utf-8'))
conn.close()
