import socket
import time


def begin(conn):
    message = 'begin'
    conn.sendall(message.encode())
    while 1:
        data = sock.recv(1024).decode()
        print(data)


def end(conn):
    message = 'end'
    conn.sendall(message.encode())
    conn.close()


if __name__ == '__main__':

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Connect the socket to the port where the server is listening
    server_address = ('localhost', 10000)
    sock.connect(server_address)
    begin(sock)
    time.sleep(10)
    end(sock)
# try:
#     # Look for the response
#     while 1:
#         data = sock.recv(1024).decode()
#         print(data)
# finally:
#     sock.close()