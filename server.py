import asyncio
import time
from xml.dom import minidom
import cv2
import distance_estimate
import lane_dete


class Algorithm:
    def __init__(self):
        file = minidom.parse('config/config.xml')
        self.rtsp_address = file.getElementsByTagName('rtsp_address')[0].firstChild.data
        self.fps = file.getElementsByTagName('fps')[0].firstChild.data
        self.cap = None
        self.current_image = None

    async def start_stream(self):
        self.cap = cv2.VideoCapture(self.rtsp_address)
        while self.cap.isOpened():
            start_time = time.time()
            ret, frame = self.cap.read()
            self.current_image = frame
            await asyncio.sleep(1/self.fps - (time.time() - start_time))

    def release_stream(self):
        self.cap.release()

    def get_lane(self):
        return lane_dete.get_lane(self.current_image)

    def get_distance(self):
        return distance_estimate.get_distance(self.current_image)

    def __call__(self):
        return {"lane": self.get_lane(), "distance": self.get_distance()}


class ServerProcess:
    def __init__(self):
        self.ipaddr = "localhost"
        self.port = 10000
        self.num = 2
        self.send_flag = False
        self.algor = Algorithm()

    def __call__(self):
        asyncio.run(self.wait_connect())

    async def wait_connect(self):
        while 1:
            server = await asyncio.start_server(self.task_distribute, self.ipaddr, self.port)
            async with server:
                await server.serve_forever()

    async def send_msg(self, conn):
        while 1:
            if self.send_flag:
                try:
                    conn.write(self.algor().encode())
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
                await self.algor.start_stream()
            if message == "end":
                self.send_flag = False
                self.algor.release_stream()

    async def task_distribute(self, reader, sender):
        task1 = asyncio.ensure_future(self.send_msg(sender))
        task2 = asyncio.ensure_future(self.listen_command(reader, sender))
        try:
            await asyncio.gather(task1, task2)
        except ConnectionError:
            task1.cancel()
            task2.cancel()


if __name__ == '__main__':
    se = ServerProcess()
    se()
