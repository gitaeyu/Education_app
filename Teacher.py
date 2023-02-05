import sys
from socket import *
from threading import *
import json
from PyQt5.QtWidgets import *
from PyQt5 import uic
from os import environ
from game import *

form_class = uic.loadUiType('./Teacher.ui')[0]



class Main(QMainWindow, form_class):
    Client_socket = None

    def __init__(self, ip, port):
        super().__init__()
        self.setupUi(self)
        # self.initialize_socket(ip, port)
        # self.listen_thread()


    def initialize_socket(self, ip, port):
        """
        클라이언트 소켓을 열고 서버 소켓과 연결해준다.
        """
        self.client_socket = socket(AF_INET, SOCK_STREAM)
        remote_ip = ip
        remote_port = port
        self.client_socket.connect((remote_ip, remote_port))

    def send_chat_gt(self):
        """
        끝말잇기 게임 대기방에서의 채팅을 보내주는 메서드
        """
        senders_name = self.id
        data = self.game_lineEdit.text()
        message = (senders_name + ': ' + data + '123456').encode('utf-8')
        self.client_socket.send(message)
        self.game_lineEdit.clear()
        return 'break'

    def listen_thread(self):
        """
        서버에서의 신호를 수신받는 스레드 시작
        """
        t = Thread(target=self.receive_message, args=(self.client_socket,))
        t.daemon = True
        t.start()

    def receive_message(self, so):
        """
        서버에서 전달하는 메시지를 수신하는 스레드
        """
        while True:
            try:
                print("스레드 시작")
                buf = so.recv(1024)
                text = buf.decode('utf-8')
                print(text)
            except:
                break
            else:
                if not buf:  # 연결 종료 됨
                    print("연결종료됨")
                    break
                if text[-3:] == '000':  # 메시지 송수신
                    self.chat_view_list.addItem(text[:-3])



if __name__ == "__main__":
    ip = '127.0.0.1'
    port = 9048

    environ["QT_DEVICE_PIXEL_RATIO"] = "0"
    environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    environ["QT_SCREEN_SCALE_FACTORS"] = "1"
    environ["QT_SCREEN_FACTOR"] = "1"

    app = QApplication(sys.argv)
    mainWindow = Main(ip, port)
    mainWindow.show()
    app.exec_()
