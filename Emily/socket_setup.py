import socket

host = socket.gethostname()
port = 61626        #this number does not matter just needs to be the same across server and client

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))
s.sendall(b'Hello, world')
data = s.recv(1024)
s.close()
print(Received, repr(data))

