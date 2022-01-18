import asyncio


class ServerProcess:
    def __init__(self):
        self.ipaddr = "localhost"
        self.port = 10000
        self.num = 2
        self.send_flag = False

    async def send_msg(self, conn):
        while 1:
            if self.send_flag:
                try:
                    conn.write(self.get_data().encode())
                    await conn.drain()
                    await asyncio.sleep(1)
                except:
                    break
            else:
                await asyncio.sleep(0.1)

    async def listen_command(self, reader, writer):
        while 1:
            data = await reader.read(100)
            message = data.decode()
            if not message:
                writer.close()
                raise ConnectionError
            if message == "begin":
                self.send_flag = True
            if message == "end":
                self.send_flag = False

    def get_data(self):
        return 'hello'

    async def wait_connect(self):
        while 1:
            server = await asyncio.start_server(self.task_distribute, self.ipaddr, self.port)
            async with server:
                await server.serve_forever()

    async def task_distribute(self, reader, sender):
        task1 = asyncio.ensure_future(self.send_msg(sender))
        task2 = asyncio.ensure_future(self.listen_command(reader, sender))
        try:
            await asyncio.gather(task1, task2)
        except ConnectionError:
            task1.cancel()
            task2.cancel()

    def __call__(self):
        asyncio.run(self.wait_connect())


if __name__ == '__main__':
    se = ServerProcess()
    se()
