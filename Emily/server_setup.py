import socket


host = ''
port = 61626

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))

print(host, port)

s.listen(1)
conn, addr = s.accept()
print('Connected by', addr)
while True:
    try:
        data = conn.recv(1024)

        if not data: break

        print("Client says:")
        print(data)
        conn.sendall(b"Server says: hi")

    except socket.error:
        print("Error Occured")
        break

conn.close()
