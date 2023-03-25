from PyQt5 import QtWidgets, QtCore
from datetime import datetime
import Messenger
import requests


class ExampleApp(QtWidgets.QMainWindow, Messenger.Ui_MainWindow):
    def __init__(self, url):
        super().__init__()
        self.setupUi(self)
        self.url = url

        self.pushButton.pressed.connect(self.send_message)

        self.last_timestamp = 0
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_messages)
        self.timer.start(1000)

    def send_message(self):
        username = self.lineEdit.text()
        password = self.lineEdit_2.text()
        text = self.textEdit.toPlainText()

        if username and password and text:
            requests.get(self.url + '/send_messages',
                         json={'username': username,
                               'password': password, 'text': text})
        else:
            if not username:
                requests.get(self.url + '/send_messages',
                             json={'username': 'messenger',
                                   'password': 'messenger', 'text': 'Вы не ввели имя пользователя'})
            if not password:
                requests.get(self.url + '/send_messages',
                             json={'username': 'messenger',
                                   'password': 'messenger', 'text': 'Вы не ввели пароль'})
            if not text:
                requests.get(self.url + '/send_messages',
                             json={'username': 'messenger',
                                   'password': 'messenger', 'text': 'Вы не можете отправлять пустые сообщения'})

        self.textEdit.setText('')
        self.textEdit.repaint()

    def update_messages(self):
        response = requests.get(self.url + '/get_messages',
                                params={'after': self.last_timestamp})
        messages = response.json()['messages']

        if messages:
            for message in messages:
                dt = datetime.fromtimestamp(message['timestamp'])
                dt = dt.strftime("%H:%M:%S %d/%m/%y")
                self.textBrowser.append(dt + ' ' + message['username'])
                self.textBrowser.append(message['text'])
                self.textBrowser.append('')
                self.last_timestamp = message['timestamp']


app = QtWidgets.QApplication([])
window = ExampleApp('http://127.0.0.1:5000')  # вставить url
window.show()
app.exec_()
