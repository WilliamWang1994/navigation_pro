import socket
import time


def end(conn):
    message = 'end'
    try:
        conn.sendall(message.encode())
    finally:
        print("finally")
        conn.close()


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 10000)
    sock.connect(server_address)
    start_time = time.time()
    message = 'begin'
    sock.sendall(message.encode())
    while time.time() - start_time < 5:
        data = sock.recv(1024).decode()
        print(data)
    end(sock)


if __name__ == '__main__':
    while 1:
        main()
# try:
#     # Look for the response
#     while 1:
#         data = sock.recv(1024).decode()
#         print(data)
# finally:
#     sock.close()