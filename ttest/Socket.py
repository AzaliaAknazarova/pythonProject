import socket
import asyncio


class Socket:
    def __init__(self):
        # Создаем конструктор класса
        self.socket = socket.socket(
            socket.AF_INET,  # AF - address family
            socket.SOCK_STREAM,  # SOCK_STREAM - TCP/IP протокол
        )
        self.main_loop = asyncio.get_event_loop()

    async def send_data(self, data=None):
        # если юзер не переопределит метод в классе наследнике выпадет ошибка
        raise NotImplementedError()

    async def listen_socket(self, listened_socket=None):
        # если юзер не переопределит метод в классе наследнике выпадет ошибка
        raise NotImplementedError()

    async def main(self):
        raise NotImplementedError()

    def start(self):
        self.main_loop.run_until_complete(self.main())

    def connected(self):
        raise NotImplementedError()
