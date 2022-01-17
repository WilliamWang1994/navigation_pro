import socket
import sys
import asyncio


class ServerProcess:
    def __init__(self):
        self.ipaddr = "localhost"
        self.port = 10000
        self.num = 2
        self.send_flag = False

    async def server_link(self, conn, addr):
        while self.send_flag:
            try:
                data = conn.recv(1024)
                if data:
                    print("from {0}:".format(addr), data.decode('utf-8'))
                else:
                    break
            except Exception:
                break

        conn.close()

    async def listen_command(self, conn, addr):

    def server_start(self):
        s_pro = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s_pro.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s_pro.bind((self.ipaddr, self.port))
        s_pro.listen(self.num)
        print('Waiting link...')
        while True:
            conn, addr = s_pro.accept()
            print("Success connect from ", addr)
            loop = asyncio.get_event_loop()
            loop.run_until_complete(self.server_link(conn, addr))
            print("end")


if __name__ == '__main__':
    server = ServerProcess()
    server.server_start()