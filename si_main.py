from socket import *
from threading import *
import time
import datetime
import sys
import pymysql
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5 import uic
import requests
import xmltodict
import json

#이미지
import urllib.request
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import *
#서버에 전송할때 ['식별자',요청할 것들]

contents_form_class = uic.loadUiType("si_contents.ui")[0]
class Contents(QWidget, contents_form_class):
    def __init__(self,parent):
        super().__init__()
        self.parent = parent
        self.setupUi(self)
        self.stw_main_stack.setCurrentIndex(0)
        self.stw_contents.setCurrentIndex(0)
        self.btn_show_menu_.clicked.connect(self.show_menu)
        self.btn_hide_menu_.clicked.connect(self.hide_menu)
        self.tw_menu_.itemClicked.connect(self.show_contents)
        self.lw_learning_list_.itemClicked.connect(self.clicked_contents)
        # ----------------------------------------------------------
        # 로그인 Ui
        self.stw_login_join.setCurrentIndex(0)
        # ----------------------------------------------------------
        # 페이지 이동
        self.btn_next.clicked.connect(self.move_next)
        self.btn_prev.clicked.connect(self.move_prev)
        # ----------------------------------------------------------
        # ID 입력
        self.le_input_ID.returnPressed.connect(self.move_next)
        # ----------------------------------------------------------
        self.btn_join.clicked.connect(self.move_join)
        self.btn_join2.clicked.connect(self.move_join)
        self.le_input_PW.returnPressed.connect(self.login_msg_send)
        self.btn_move_main.clicked.connect(self.login_msg_send)
        # ----------------------------------------------------------
    def login_msg_send(self):
        id = self.le_show_ID.text()
        pw = self.le_input_PW.text()
        login_temp = ['로그인',id,pw,'학생']
        login_msg = json.dumps(login_temp)
        self.parent.client_socket.sendall(login_msg.encode())
    def login_result(self):
        if self.parent.signal[0] == '로그인 완료':
            self.stw_main_stack.setCurrentIndex(1)
            self.login_user = self.parent.signal[1::]
            self.setup_label()

    def move_next(self):
        input_id = self.le_input_ID.text()
        self.le_show_ID.setText(input_id)
        if input_id=="":
            QMessageBox.warning(self, 'ID 입력 오류', 'ID를 입력해주세요.')
        else:
            self.stw_login_join.setCurrentIndex(1)
    def move_prev(self):
        self.stw_login_join.setCurrentIndex(0)
        self.le_input_ID.clear()
        self.le_input_PW.clear()
    def move_join(self):
        self.stw_login_join.setCurrentIndex(2)
    def move_login(self):
        self.sign_up_clear()
        self.stw_login_join.setCurrentIndex(0)
    def change_id(self):
        self.use_id = False
        self.btn_check_id.setEnabled(True)
    def check_id(self):
        id = self.le_input_id.text()
        self.serviceable = False
        self.use_id = False
        if len(id) < 3:
            self.le_input_id.clear()
            QMessageBox.information(self, "ID", "ID가 너무 짧습니다.\n3자 이상으로 입력해주세요")
        else:
            # conn = pymysql.connect(host='10.10.21.103', port=3306, user='root', password='00000000', db='education_app',
            #                        charset='utf8')
            conn = pymysql.connect(host='localhost', port=3306, user='root', password='00000000', db='education_app', charset='utf8')
            cursor = conn.cursor()
            cursor.execute(f"select ID from memberinfo where ID='{id}'")
            a = cursor.fetchone()
            print(a)
            conn.close()
            if a == None:
                self.use_id = True
                QMessageBox.information(self, 'ID', '사용가능한 ID 입니다.')
                self.btn_check_id.setEnabled(False)
            else:
                QMessageBox.critical(self, "ID", "이미 사용중인 ID 입니다.")
    def check_sign_up(self):
        # conn = pymysql.connect(host='10.10.21.103', port=3306, user='root', password='00000000', db='education_app',
        #                        charset='utf8')
        conn = pymysql.connect(host='localhost', port=3306, user='root', password='00000000', db='education_app',
                               charset='utf8')
        cursor = conn.cursor()
        id = self.le_input_id.text()
        pw = self.le_input_pw.text()
        chk_pw = self.le_check_pw.text()
        name = self.le_input_name.text()
        phonenum = self.le_phonenum.text()
        self.join=[id, pw, chk_pw, name, phonenum]
        what_NULL=['ID','PW','이름','휴대폰번호']
        print(self.join)
        for line_edit in self.join:
            if line_edit =="":
                NULL_index = self.join.index(line_edit)
                QMessageBox.information(self, "NULL", f"{what_NULL[NULL_index]}를 입력해주세요.")
                return
        if self.use_id:
            if self.join[1] == self.join[2]:
                cursor.execute(f"insert into memberinfo (ID,Password,User_Name,Division) values('{self.join[0]}','{self.join[1]}','{self.join[3]}','학생')")
                conn.commit()
                conn.close()
                QMessageBox.information(self, "ID", "회원가입이 완료되었습니다.", QMessageBox.Ok)
                self.stw_login_join.setCurrentIndex(0)
                self.sign_up_clear()
        else: QMessageBox.information(self, 'ID', 'ID 중복확인을 해주세요.')
    def sign_up_clear(self):
        self.le_input_id.clear()
        self.le_input_pw.clear()
        self.le_check_pw.clear()
        self.le_input_name.clear()
        self.le_phonenum.clear()

    def setup_label(self):
        print('!!!!!',self.login_user)
        self.lb_check_name.setText(f'{self.login_user[3]}님 안녕하세요.')
        self.lb_user_name_.setText(self.login_user[3])
        td_time = Thread(target=self.time_thread, daemon=True)  # 시간쓰레드
        td_time.start()
        print('쓰레드')


    def show_menu(self):
        self.stw_menu.setCurrentIndex(1)
    def hide_menu(self):
        self.stw_menu.setCurrentIndex(0)
    def show_contents(self, item, column):
        item_txt = item.text(column)

        if item_txt == "개인정보":
            print('개인정보')
            self.stw_contents.setCurrentIndex(0)
        elif item_txt == "Q&A":
            print('Q&A')
            self.stw_contents.setCurrentIndex(3)
        elif item_txt == "상담":
            print('상담하기')
            self.stw_contents.setCurrentIndex(4)
            self.consulting_request()
        else:
            a = item.parent()
            if a:
                menu = a.text(column)
                if menu == "학습":
                    print('학습')
                    self.stw_contents.setCurrentIndex(1)
                    self.learning(item,column)
                elif menu == "문제풀이":
                    print('문제풀이')
                    self.stw_contents.setCurrentIndex(2)
                    self.problem_solving(item,column)
    def consulting_request(self):
        temp = ['SC온라인교사목록',self.login_user[3]]
        requests_msg = json.dumps(temp)
        self.client_socket.sendall(requests_msg.encode())

    def learning(self, item, column):
        self.learning_name = item.text(column)
        self.lb_learning_name_.setText(f"{self.learning_name} 학습자료")
        print(self.learning_name)

        self.learning_name_code = []
        key = '3R%2BSur%2BruWT%2F2MXwVvEJR5V39S2A5QoImBYPWyzEESJt5WwC4MEVIV5JacV50D97kscWEykWIPpB08XmaHpgnA%3D%3D'
        if self.learning_name== '곤충':
            url = f'http://openapi.nature.go.kr/openapi/service/rest/InsectService/isctPrtctList?serviceKey={key}'
            self.url_2 = 'http://openapi.nature.go.kr/openapi/service/rest/InsectService/isctIlstrInfo'
        elif self.learning_name== '포유류':
            url = f'http://apis.data.go.kr/1400119/MammService/mammIlstrSearch?serviceKey={key}'
            self.url_2 = 'http://apis.data.go.kr/1400119/MammService/mammIlstrInfo'
        elif self.learning_name == '조류':
            url = f'http://apis.data.go.kr/1400119/BirdService/birdIlstrSearch?serviceKey={key}'
            self.url_2 = 'http://apis.data.go.kr/1400119/BirdService/birdIlstrInfo'
        content = requests.get(url).content  # request 모듈을 이용해서 정보 가져오기(byte형태로 가져와지는듯)
        dict = xmltodict.parse(content)  # xmltodict 모듈을 이용해서 딕셔너리화 & 한글화
        jsonString = json.dumps(dict, ensure_ascii=False)  # json.dumps를 이용해서 문자열화(데이터를 보낼때 이렇게 바꿔주면 될듯)
        jsonObj = json.loads(jsonString)  # 데이터 불러올 때(딕셔너리 형태로 받아옴)
        self.lw_learning_list_.clear()
        if self.learning_name == '곤충':
            for item in jsonObj['response']['body']['items']['item']:
                temp_list = [item['insctofnmkrlngnm'],item['insctPilbkNo'],item['imgUrl']]
                self.learning_name_code.append(temp_list)
                self.lw_learning_list_.addItem(item['insctofnmkrlngnm'])
        else:           #조류, 포유류일 경우
            for item in jsonObj['response']['body']['items']['item']:
                temp_list = [item['anmlGnrlNm'],item['anmlSpecsId'],'']
                self.learning_name_code.append(temp_list)
                self.lw_learning_list_.addItem(item['anmlGnrlNm'])
    def clicked_contents(self):
        item = self.lw_learning_list_.currentItem().text()
        self.lb_learning_img_name_.setText(f"<{item}>")

        # key = '3R%2BSur%2BruWT%2F2MXwVvEJR5V39S2A5QoImBYPWyzEESJt5WwC4MEVIV5JacV50D97kscWEykWIPpB08XmaHpgnA%3D%3D'
        key = '3R+Sur+ruWT/2MXwVvEJR5V39S2A5QoImBYPWyzEESJt5WwC4MEVIV5JacV50D97kscWEykWIPpB08XmaHpgnA=='
        for i in self.learning_name_code:
            if item == i[0]:
                params = {'serviceKey': key, 'q1': i[1]}
                content = requests.get(self.url_2, params=params).content
                dict = xmltodict.parse(content)  # xmltodict 모듈을 이용해서 딕셔너리화 & 한글화
                jsonString = json.dumps(dict, ensure_ascii=False)  # json.dumps를 이용해서 문자열화(데이터를 보낼때 이렇게 바꿔주면 될듯)
                jsonObj = json.loads(jsonString)
                #이미지 불러오기
                if i[2]!='':
                    img_url = i[2]
                else:
                    img_url = jsonObj['response']['body']['item']['imgUrl']
                if self.learning_name == '곤충':           #곤충
                    general_features = jsonObj['response']['body']['item']['cont1']
                    ecological_features = jsonObj['response']['body']['item']['cont7']
                else:                                     #포유류, 조류일 경우
                    general_features = jsonObj['response']['body']['item']['gnrlSpftrCont']
                    ecological_features = jsonObj['response']['body']['item']['eclgDpftrCont']
                break
        imageFromWeb = urllib.request.urlopen(img_url).read()
        qPixmapVar = QPixmap()
        qPixmapVar.loadFromData(imageFromWeb)
        qPixmapVar = qPixmapVar.scaled(self.lb_img_.width(), self.lb_img_.height(), Qt.KeepAspectRatio,
                                       Qt.SmoothTransformation)
        self.lb_img_.setPixmap(qPixmapVar)
        #일반 특징 불러오기
        self.tb_learning_content_.clear()
        self.tb_learning_content_.append(f'<<{item}의 일반적인 특징>>')
        self.tb_learning_content_.append(general_features)
        #생태 특징 불러오기
        self.tb_learning_content_.append(f'\n<<{item}의 생태적인 특징>>')
        if ecological_features==None:
            self.tb_learning_content_.append('일반적인 생태적 특징은 잘 알려지지 않았다.')
        else: self.tb_learning_content_.append(ecological_features)
    def time_thread(self):
        while True:
            time.sleep(1)
            now = datetime.datetime.now()
            date_str = now.strftime('%Y-%m-%d')
            time_str = now.strftime('%H:%M:%S')
            self.lb_date.setText(date_str)
            self.lb_time.setText(time_str)
    def problem_solving(self, item, column):
        print('함수들어옴')
        question_name = item.text(column)
        print(question_name)
        self.lb_question_name_.setText(f"{question_name} 문제풀이")

    def online_user(self):
        self.lw_online_teacher_.clear()
        online_student = self.signal[1]
        online_teacher = self.signal[2]
        for i in online_student: # 테스트용
            print(i[1])
            self.lw_online_student_.addItem(i[1])
        self.lw_online_student_.scrollToBottom()
        for i in online_teacher:
            print(i[1])
            self.lw_online_teacher_.addItem(i[1])
        self.lw_online_teacher_.scrollToBottom()
        print('온라인유저 목록 업데이트')

class Student:
    def __init__(self):
        ip = '127.0.0.1'
        port = 9048
        self.initialize_socket(ip, port)
        self.listen_thread()
        self.contents = Contents(self)
        self.contents.show()
    def initialize_socket(self, ip, port):
        """
        클라이언트 소켓을 열고 서버 소켓과 연결해준다.
        """
        self.client_socket = socket(AF_INET, SOCK_STREAM)
        remote_ip = ip
        remote_port = port
        self.client_socket.connect((remote_ip, remote_port))
        #소켓이 연결되면 로그인 정보를 서버에 전송한다.

    def listen_thread(self):
        """
        서버에서의 신호를 수신받는 스레드 시작
        """
        t = Thread(target=self.receive_message, args=(self.client_socket,), daemon=True)
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
            except Exception as er:
                print(er)
                break
            else:
                if self.signal[0] == "로그인 완료":  #signal = ["로그인", [학생ID, 학생이름, 학생], [교사ID, 교사이름, 교사]]
                    self.contents.login_result()
                elif self.signal[0] == "로그인":
                    print('시그널은 로그인')
                elif self.signal[0] == "DB설명반환":  # signal = ["DB설명반환",생태,일반,이미지]
                    print("DB설명반환 메세지 받음")
if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = QtWidgets.QStackedWidget()
    # 클래스의 객체 만들기
    # login = Login()
    student = Student()
    # contents = Contents(student)
    # 프로그램 화면을 보여주는 코드
    app.exec_()