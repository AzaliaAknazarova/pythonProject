import os
import sys
import rsa
import time
import shelve
import socket
import threading
import keyboard


# Мониторинг входящих сообщений
class message_monitor:
    def __init__(self, server_socket, private_key, parent=None):
        self.server_socket = server_socket
        self.private_key = private_key
        self.message = None

    def run(self):
        while True:
            try: # Данные от собеседника (зашифрованные)
                self.message = self.server_socket.recv(1024)
                decrypt_message = rsa.decrypt(self.message, self.private_key)
                self.mysignal.emit(decrypt_message.decode('utf-8'))
            except: # Данные от сервера (не зашифрованные)
                self.mysignal.emit(self.message.decode('utf-8'))


    # Сохранить ник
    def connect_server(self):
        # Подключаемся к серверу
        try:
            self.tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.tcp_client.connect((self.ip, self.port)); time.sleep(2)

            # Запускаем мониторинг входящих сообщений
            self.message_monitor = message_monitor(self.tcp_client, self.myprivatekey)
            self.message_monitor.mysignal.connect(self.update_chat)
            self.message_monitor.start()

            # Производим действия с объектами
    # Отправить сообщение
    def send_message(self):
        try:
            if len(self.ui.lineEdit.text()) > 0:
                message = self.ui.lineEdit.text()
                crypto_message = rsa.encrypt(message.encode('utf-8'), self.friend_public_key)

                self.ui.plainTextEdit.appendPlainText(f'[Вы]: {message}')
                self.tcp_client.send(crypto_message)
                self.ui.lineEdit.clear()
        except:
            sys.exit()





    