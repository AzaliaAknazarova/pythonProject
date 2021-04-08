import shelve
import keyboard
import rsa
import os
from Socket import Socket
from datetime import datetime
import asyncio
from os import system
import msvcrt


class Client(Socket):
    def __init__(self):
        super(Client, self).__init__()
        self.messages = ""
        self.friend_public_key = None

        # Ключи шифрования текущего клиента
        self.mypublickey = None
        self.myprivatekey = None

        # Проверка на наличие идентификатора собеседника
        if len(os.listdir('C:\\Users\\azali\\PycharmProjects\\pythonProject\\ttest\\friend_id')) != 0:
            pass
        else:
            print("Поместите идентификатор собеседника в friend_id")

        # Проверка создан ли личный идентификатор
        if not os.path.exists('C:\\Users\\azali\\PycharmProjects\\pythonProject\\ttest\\private'):
            print("Также необходимо сгенерировать свой идентификатор")

        if len(os.listdir('C:\\Users\\azali\\PycharmProjects\\pythonProject\\ttest\\friend_id')) != 0 and os.path.exists('C:\\Users\\azali\\PycharmProjects\\pythonProject\\ttest\\private'):
            # Подгрузка данных текущего клиента
            with shelve.open('C:\\Users\\azali\\PycharmProjects\\pythonProject\\ttest\\private') as file:
                self.mypublickey = file['pubkey']
                self.myprivatekey = file['privkey']

    def connected(self):
        try:
            self.socket.connect(("localhost", 8888))  # адрес подключения к серверу
            self.socket.setblocking(False)  # установка сокета на неблокирующее состояние

            # Проверка создан ли личный идентификатор
            if not os.path.exists('C:\\Users\\azali\\PycharmProjects\\pythonProject\\ttest\\private'):
                print("Нажмите Esc для генерации")
                while True:
                    if msvcrt.kbhit():  # Нажата ли клавиша?
                        key = ord(msvcrt.getch())  # Какая клавиша нажата?
                        #print(key)
                        if key == 27:  # если Enter:
                            (pubkey, privkey) = rsa.newkeys(512)

                            with shelve.open('pubkey') as file:
                                file['pubkey'] = pubkey
                            os.makedirs('C:\\Users\\azali\\PycharmProjects\\pythonProject\\ttest\\private')
                            with shelve.open('C:\\Users\\azali\\PycharmProjects\\pythonProject\\ttest\\private\\private') as file:
                                file['pubkey'] = pubkey
                                file['privkey'] = privkey
                            print("Генерация ключей прошла успешно")
                            print("Передайте его собеседнику и жмите в подтверждение клавишу TAB")

                    if msvcrt.kbhit():  # Нажата ли клавиша?
                        key = ord(msvcrt.getch())  # Какая клавиша нажата?
                        print(key)
                        if key == 9 and len(os.listdir('C:\\Users\\azali\\PycharmProjects\\pythonProject\\ttest\\friend_id')) != 0:
                            try:
                                # Подгрузка данных собеседника
                                with shelve.open('C:\\Users\\azali\\PycharmProjects\\pythonProject\\ttest\\friend_id\\pubkey') as file:
                                    self.friend_public_key = file['pubkey']
                            except:
                                print("friend_id не найдено")
                        if key != 9:
                            print('friend_id не найдено или попробуйте еще раз')
        except ConnectionRefusedError:
            print("-404, Server not found")
            exit(0)

    async def listen_socket(self, listened_socket=None):
        while True:
            data = await self.main_loop.sock_recv(self.socket, 2048)
            clean_data = rsa.decrypt(data, self.private_key)

            self.messages += f"{datetime.now().date()}: {clean_data.decode('utf-8')}\n"

            system("cls")
            print(self.messages)

    async def send_data(self, data=None):
        while True:
            data = await self.main_loop.run_in_executor(None, input)
            encrypted_data = rsa.encrypt(data.encode('utf-8'), self.friend_public_key)

            await self.main_loop.sock_sendall(self.socket, encrypted_data)

    async def main(self):
        await asyncio.gather(  # возвращает лист из тасок
            self.main_loop.create_task(self.listen_socket(self.myprivatekey)),
            self.main_loop.create_task(self.send_data())
        )


if __name__ == '__main__':
    client = Client()
    client.connected()

    client.start()
