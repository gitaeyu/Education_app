import sys
from socket import *
from threading import *
from PyQt5.QtWidgets import *
from PyQt5 import uic
from os import environ

import json
import requests
import xmltodict
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
        self.initialize_socket(ip, port)
        self.listen_thread()
        self.test_update_search.clicked.connect(self.search_test_items)
        self.test_item_list_widget.itemClicked.connect(self.test_items_description)
        self.Test_Update_entry_btn.clicked.connect(self.entry_test)
        self.treeWidget.itemClicked.connect(self.on_item_clicked)
        self.item = ''
        self.test_update_search_LE.setText('')

    def search_test_items(self):
        self.test_item_list_widget.clear()
        self.searchitem = self.test_update_search_LE.text()
        try:  # API 오류 날때를 대비해서 오류시 서버에 DB 요청

            if self.item == '포유류':
                self.search_test_items_mammal()
            elif self.item == '곤충':
                self.search_test_items_insect()
            elif self.item == '조류':
                self.search_test_items_bird()

        except Exception as e:
            print(e)
            information = ["DB검색요청", self.item, self.searchitem]
            print(information)
            message = json.dumps(information)
            self.clear_test_update()
            self.client_socket.send(message.encode())

    def search_test_items_mammal(self):
        url = 'http://apis.data.go.kr/1400119/MammService/mammIlstrSearch'
        params = {
            'serviceKey': '11xBqPRCrKxDRnzolBiWVGwhexbmYELfieu+GvVw7z2HYGWD67SB2EGIMJHoG8KYEvkNOd3LaHsvIp7cDZPhzg==',
            'st': '1', 'sw': self.searchitem, 'numOfRows': '20', 'pageNo': '1'}
        response = requests.get(url, params=params)
        # xml 내용
        content = response.text
        xml_obj = bs4.BeautifulSoup(content, 'lxml-xml')
        rows = xml_obj.findAll('item')
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
                if j == 0 or j == 2:  # 0번째 2번쨰 컬럼값을 가지고 옵니다.
                    # 컬럼의 각 데이터 값 저장
                    value_list.append(columns[j].text)
                    # 각 행의 value값 전체 저장
                    row_list.append(value_list)
            # 데이터 리스트 값 초기화
            value_list = []
        result = []
        # 중복을 제거해줍니다.
        for value in row_list:
            if value not in result:
                result.append(value)

        # xml값 DataFrame으로 만들기
        self.df = pd.DataFrame(result, columns=['anmlGnrlNm', 'anmlSpecsId'])
        for i in range(len(self.df)):
            self.test_item_list_widget.addItem(self.df.iloc[i]['anmlGnrlNm'])
    def search_test_items_bird(self):
        url = 'http://apis.data.go.kr/1400119/BirdService/birdIlstrSearch'
        params = {
            'serviceKey': '11xBqPRCrKxDRnzolBiWVGwhexbmYELfieu+GvVw7z2HYGWD67SB2EGIMJHoG8KYEvkNOd3LaHsvIp7cDZPhzg==',
            'st': '1', 'sw': '', 'numOfRows': '10', 'pageNo': '1'}
        response = requests.get(url, params=params)
        # xml 내용
        content = response.text
        xml_obj = bs4.BeautifulSoup(content, 'lxml-xml')
        rows = xml_obj.findAll('item')
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
                if j == 0 or j == 2:  # 0번째 2번쨰 컬럼값을 가지고 옵니다.
                    # 컬럼의 각 데이터 값 저장
                    value_list.append(columns[j].text)
                    # 각 행의 value값 전체 저장
                    row_list.append(value_list)
            # 데이터 리스트 값 초기화
            value_list = []
        result = []
        # 중복을 제거해줍니다.
        for value in row_list:
            if value not in result:
                result.append(value)

        # xml값 DataFrame으로 만들기
        self.df = pd.DataFrame(result, columns=['anmlGnrlNm', 'anmlSpecsId'])
        for i in range(len(self.df)):
            self.test_item_list_widget.addItem(self.df.iloc[i]['anmlGnrlNm'])
    def search_test_items_insect(self):
        url = 'http://openapi.nature.go.kr/openapi/service/rest/InsectService/isctPrtctList'
        params = {
            'serviceKey': '11xBqPRCrKxDRnzolBiWVGwhexbmYELfieu+GvVw7z2HYGWD67SB2EGIMJHoG8KYEvkNOd3LaHsvIp7cDZPhzg=='}
        response = requests.get(url, params=params)
        # xml 내용
        content = response.text
        xml_obj = bs4.BeautifulSoup(content, 'lxml-xml')
        rows = xml_obj.findAll('item')
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
                if j == 5 or j == 6:  # 8번째 10번쨰 컬럼값을 가지고 옵니다.
                    # 컬럼의 각 데이터 값 저장
                    value_list.append(columns[j].text)
                    # 각 행의 value값 전체 저장
                    row_list.append(value_list)
            # 데이터 리스트 값 초기화
            value_list = []
        result = []
        # 중복을 제거해줍니다.
        for value in row_list:
            if value not in result:
                result.append(value)

        # xml값 DataFrame으로 만들기
        self.df = pd.DataFrame(result, columns=['insctPilbkNo','insctofnmkrlngnm'])
        for i in range(len(self.df)):
            self.test_item_list_widget.addItem(self.df.iloc[i]['insctofnmkrlngnm'])
    def test_items_description(self):
        self.textBrowser.clear()
        if self.item == '포유류' :
            try :
                self.test_items_description_mammal()
            except :
                self.test_items_description_db()

        elif self.item == '곤충' :
            try:
                self.test_items_description_insect()
            except:
                self.test_items_description_db()
        elif self.item == '조류' :
            try:
                self.test_items_description_bird()
            except Exception as e:
                print(e)
                self.test_items_description_db()

    def test_items_description_mammal(self):
        self.textBrowser.clear()
        temp = self.test_item_list_widget.currentRow()
        q1 = self.df.iloc[temp]['anmlSpecsId']

        url = 'http://apis.data.go.kr/1400119/MammService/mammIlstrInfo'
        params = {'serviceKey': decoding, 'q1': q1}

        response = requests.get(url, params=params)
        content = response.content  # request 모듈을 이용해서 정보 가져오기(byte형태로 가져와지는듯)
        dict = xmltodict.parse(content)  # xmltodict 모듈을 이용해서 딕셔너리화 & 한글화
        jsonString = json.dumps(dict, ensure_ascii=False)  # json.dumps를 이용해서 문자열화(데이터를 보낼때 이렇게 바꿔주면 될듯)

        self.jsonObj = json.loads(jsonString)  # 데이터 불러올 때(딕셔너리 형태로 받아옴)
        self.img_URL = self.jsonObj['response']['body']['item']['imgUrl']
        self.textBrowser.append(self.jsonObj['response']['body']['item']['eclgDpftrCont'])
        self.textBrowser.append('\n')
        self.textBrowser.append(self.jsonObj['response']['body']['item']['gnrlSpftrCont'])
    def test_items_description_bird(self):
        self.textBrowser.clear()
        temp = self.test_item_list_widget.currentRow()
        q1 = self.df.iloc[temp]['anmlSpecsId']

        url = 'http://apis.data.go.kr/1400119/BirdService/birdIlstrInfo'
        params = {'serviceKey': decoding, 'q1': q1}

        response = requests.get(url, params=params)
        content = response.content  # request 모듈을 이용해서 정보 가져오기(byte형태로 가져와지는듯)
        dict = xmltodict.parse(content)  # xmltodict 모듈을 이용해서 딕셔너리화 & 한글화
        jsonString = json.dumps(dict, ensure_ascii=False)  # json.dumps를 이용해서 문자열화(데이터를 보낼때 이렇게 바꿔주면 될듯)

        self.jsonObj = json.loads(jsonString)  # 데이터 불러올 때(딕셔너리 형태로 받아옴)
        self.img_URL = self.jsonObj['response']['body']['item']['imgUrl']
        self.textBrowser.append(self.jsonObj['response']['body']['item']['eclgDpftrCont'])
        self.textBrowser.append('\n')
        self.textBrowser.append(self.jsonObj['response']['body']['item']['gnrlSpftrCont'])
    def test_items_description_insect(self):
        self.textBrowser.clear()
        temp = self.test_item_list_widget.currentRow()
        q1 = self.df.iloc[temp]['insctPilbkNo']

        url = 'http://openapi.nature.go.kr/openapi/service/rest/InsectService/isctIlstrInfo'
        params = {'serviceKey': decoding, 'q1': q1}

        response = requests.get(url, params=params)
        content = response.content  # request 모듈을 이용해서 정보 가져오기(byte형태로 가져와지는듯)
        dict = xmltodict.parse(content)  # xmltodict 모듈을 이용해서 딕셔너리화 & 한글화
        jsonString = json.dumps(dict, ensure_ascii=False)  # json.dumps를 이용해서 문자열화(데이터를 보낼때 이렇게 바꿔주면 될듯)

        self.jsonObj = json.loads(jsonString)  # 데이터 불러올 때(딕셔너리 형태로 받아옴)
        self.img_URL = self.jsonObj['response']['body']['item']['imgUrl']
        self.textBrowser.append(self.jsonObj['response']['body']['item']['cont1'])
        self.textBrowser.append('\n')
        self.textBrowser.append(self.jsonObj['response']['body']['item']['cont7'])
    def test_items_description_db(self):
        selected_item = self.test_item_list_widget.currentItem().text()
        information = ["DB설명요청",self.item,selected_item]
        message = json.dumps(information)
        self.client_socket.send(message.encode())
    def on_item_clicked(self,item,column):

        self.item = item.text(column)

        if self.item == "Q&A":
            print('Q&A')
            self.stw_contents.setCurrentIndex(3)
        elif self.item == "상담":
            print('상담하기')
            self.stw_contents.setCurrentIndex(4)
        else:
            a = item.parent()
            if a:
                menu = a.text(column)
                if menu == "문제 업데이트":
                    print('학습')
                    self.stackedWidget.setCurrentIndex(0)
                    self.clear_test_update()
                elif menu == "점수/통계확인(학생별)":
                    self.stw_contents.setCurrentIndex(1)
                    print('문제풀이')
        print(self.item)
    def entry_test(self):
        if self.item == '' :
            self.item = '동물'
        test_contents = self.test_contents.text()
        test_correct_answer = self.test_answer.text()
        if test_contents == "문제 내용을 입력해주세요" :
            return
        information = ["문제등록", test_contents,self.img_URL,test_correct_answer,self.item]
        print(information)
        message = json.dumps(information)
        self.clear_test_update()
        self.client_socket.send(message.encode())

    def clear_test_update(self):
        self.test_update_search_LE.clear()
        self.test_item_list_widget.clear()
        self.textBrowser.clear()
        self.test_contents.setText("문제 내용을 입력해주세요")







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

    def receive_message(self, socket):
        """
        서버에서 전달하는 메시지를 수신하는 스레드
        """
        while True:
            try:
                incoming_message = socket.recv(8192)
                self.signal = json.loads(incoming_message.decode())
                print(self.signal)
            except:
                print("오류남")
                break
            else:
                if self.signal[0] == "DB검색반환":  # signal = ["DB검색반환",1,2,3,4 ....]
                    print("검색반환메세지받음")
                    self.update_test_item_widget_db()
                elif self.signal[0] == "DB설명반환":  # signal = ["DB설명반환",생태,일반,이미지]
                    print("DB설명반환 메세지 받음")
                    self.update_description_db()
    def update_description_db(self):
        self.signal.pop(0)
        self.img_URL = self.signal[2]
        self.textBrowser.append(self.signal[0])
        self.textBrowser.append('\n')
        self.textBrowser.append(self.signal[1])
    def update_test_item_widget_db(self):
        self.test_item_list_widget.clear()
        self.signal.pop(0)
        for i in self.signal:
            self.test_item_list_widget.addItem(i)



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
