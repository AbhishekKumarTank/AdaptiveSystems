from socket import *

s = socket(AF_INET, SOCK_DGRAM)
s.bind(('192.168.1.79',12345)) #listener self's ip
s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)


while True:
    m = s.recvfrom(1024)
    print (m[0].decode('utf-8'))
    m=m[0].decode('utf-8')
    #if m == '1 talk to 2':
    s.sendto(b'1 received from 0',('192.168.1.253', 12345))
        #s.sendto(b'2 talk to 3',('192.168.1.224', 12345))

