import socket
import time

host = "192.168.123.12"   #ip address of the robot's pi
port = 61626        #this number does not matter just needs to be the same across server and client

# set up socket connection, server needs to be started first**
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))

# send handshake to the server
s.sendall(b'socket connected!')
data = s.recv(1024)
#print out data recieved
print(data)

while True:
    #get input here
    #for now will simulate as a while look that prints 1 out ten times

    data = [0,1,2,3,4,5,6,7,8,9]

    for i in data:
        #send string, notice string needs to be in bytes form, this is the simplest way to do this
        #can probably find a better way to convert, especially if we want to use a preset variable
        s.sendall(b"1")

        #collect and print data recieved
        data = s.recv(1024)
        print(data)

        # arbitrary wait time for ease of testing can delete later if needed
        time.sleep(2)
    break

#close connection
s.close()
