import sys
from socket import *
from threading import *
import json
from PyQt5.QtWidgets import *
from PyQt5 import uic
from os import environ
from game import *


import requests
import pprint
import pandas as pd
import bs4


encoding = '11xBqPRCrKxDRnzolBiWVGwhexbmYELfieu%2BGvVw7z2HYGWD67SB2EGIMJHoG8KYEvkNOd3LaHsvIp7cDZPhzg%3D%3D'
decoding = '11xBqPRCrKxDRnzolBiWVGwhexbmYELfieu+GvVw7z2HYGWD67SB2EGIMJHoG8KYEvkNOd3LaHsvIp7cDZPhzg=='
form_class = uic.loadUiType('./Teacher.ui')[0]



class Main(QMainWindow, form_class):
    Client_socket = None

    def __init__(self, ip, port):
        super().__init__()
        self.setupUi(self)
        # self.initialize_socket(ip, port)
        # self.listen_thread()
        self.test_update_search.clicked.connect(self.search_test_items)
        self.test_item_list_widget.itemClicked.connect(self.test_items_description)

    def test_items_description(self,row):
        temp = self.test_item_list_widget.currentRow()
        q1 = self.df.iloc[temp]['anmlSpecsId']

        url = 'http://apis.data.go.kr/1400119/MammService/mammIlstrInfo'
        params = {'serviceKey': decoding, 'q1': q1}

        response = requests.get(url, params=params)
        print(response.content)
        # xml 내용
        content = response.text

        # bs4 사용하여 item 태그 분리

        xml_obj = bs4.BeautifulSoup(content, 'lxml-xml')
        rows = xml_obj.findAll('item')
        # xml 안의 데이터 수집
        row_list = []  # 행값
        name_list = []  # 열이름값
        value_list = []  # 데이터값
        for i in range(0, len(rows)):
            columns = rows[i].find_all()
            # 첫째 행 데이터 수집
            for j in range(0, len(columns)):
                if i == 0:
                    # 컬럼 이름 값 저장
                    name_list.append(columns[j].name)
                if j == 6 or j == 15 or j == 16 or j == 17:  # 원하는 컬럼 데이터
                    # 컬럼의 각 데이터 값 저장
                    value_list.append(columns[j].text)
                    # 각 행의 value값 전체 저장
                    row_list.append(value_list)
            # 데이터 리스트 값 초기화
            value_list = []
        print(name_list)
        pd.set_option('display.width', 1000)
        pd.set_option('display.max_rows', None)
        pd.set_option('display.max_columns', None)
        # xml값 DataFrame으로 만들기
        df = pd.DataFrame(row_list, columns=['anmlGnrlNm', 'eclgDpftrCont', 'gnrlSpftrCont', 'imgUrl'])
        # print(df.head(10))
        self.textBrowser.append(df.iloc[0]['eclgDpftrCont'])
        self.textBrowser.append('\n')
        self.textBrowser.append(df.iloc[0]['gnrlSpftrCont'])

        print(df.iloc[0]['eclgDpftrCont'])
        print("나이스")
        print(df.iloc[0]['gnrlSpftrCont'])
        print(df.iloc[0]['imgUrl'])


    def search_test_items(self):
        self.test_item_list_widget.clear()
        a = self.test_update_search_LE.text()
        url = 'http://apis.data.go.kr/1400119/MammService/mammIlstrSearch'
        params = {'serviceKey': '11xBqPRCrKxDRnzolBiWVGwhexbmYELfieu+GvVw7z2HYGWD67SB2EGIMJHoG8KYEvkNOd3LaHsvIp7cDZPhzg==',
                  'st': '1', 'sw': a, 'numOfRows': '10', 'pageNo': '1'}
        response = requests.get(url, params=params)
        # xml 내용
        content = response.text
        xml_obj = bs4.BeautifulSoup(content, 'lxml-xml')
        rows = xml_obj.findAll('item')
        # 컬럼 값 조회용
        columns = rows[0].find_all()
        # 각 행의 컬럼, 이름, 값을 가지는 리스트 만들기
        row_list = []  # 행값
        name_list = []  # 열이름값
        value_list = []  # 데이터값
        # xml 안의 데이터 수집
        for i in range(0, len(rows)):
            columns = rows[i].find_all()
            # 첫째 행 데이터 수집
            for j in range(0, len(columns)):
                if i == 0:
                    # 컬럼 이름 값 저장
                    name_list.append(columns[j].name)
                if j == 0 or j == 2:
                    # 컬럼의 각 데이터 값 저장
                    value_list.append(columns[j].text)
                    # 각 행의 value값 전체 저장
                    row_list.append(value_list)
            # 데이터 리스트 값 초기화
            value_list = []

        # xml값 DataFrame으로 만들기
        self.df = pd.DataFrame(row_list, columns=['anmlGnrlNm', 'anmlSpecsId'])
        self.test_item_list_widget.addItem(self.df.iloc[0]['anmlGnrlNm'])
        self.test_item_list_widget.addItem(self.df.iloc[1]['anmlGnrlNm'])


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
