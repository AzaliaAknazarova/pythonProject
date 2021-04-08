from Socket import Socket
import asyncio


class Server(Socket):
    def __init__(self):
        super(Server, self).__init__()

        self.users = []  # массив подключенных пользователей

    def connected(self):
        self.socket.bind(("localhost", 8888))  # адрес подключения к серверу
        self.socket.listen()  # сервер готов к приему
        self.socket.setblocking(False)  # установка сокета на неблокирующее состояние
        print("Server is listening...")

    # для каждого подсоеденненого пользователя отправляем сообщения
    async def send_data(self, data=None):
        for user in self.users:
            await self.main_loop.sock_sendall(user, data)

    async def listen_socket(self, listened_socket=None):
        if not listened_socket:
            return

        while True:
            try:
                data = await self.main_loop.sock_recv(listened_socket, 2048)
                print(data)
                await self.send_data(data)

            except ConnectionResetError:
                self.users.remove(listened_socket)
                print("Client removed")
                return

    async def accept_sockets(self):
        while True:
            user_socket, address = await self.main_loop.sock_accept(self.socket)  # принимает входящее подключение
            # вывод подключенного пользователя, address - уникальный номер и ip,выводим ip
            print(f"User {address[0]} connected!")
            self.users.append(user_socket)  # добавляем подключенного пользователя в массив пользователей
            self.main_loop.create_task(self.listen_socket(user_socket))

    async def main(self):
        await self.main_loop.create_task(self.accept_sockets())


# вызываем запуск сервера (вызов как основной)
if __name__ == '__main__':
    server = Server()
    server.connected()

    server.start()
