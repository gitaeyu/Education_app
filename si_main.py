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

class MessageSignal(QObject):
    show_message = pyqtSignal(str)


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
        self.btn_logout.clicked.connect(self.btn_logout_clicked)
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
        # Q&A
        self.tw_qna_list.cellDoubleClicked.connect(self.show_qna)
        self.btn_question_finish.clicked.connect(self.question_Completed)
        # ----------------------------------------------------------
        # 메시지 박스
        self.message_signal = MessageSignal()
        self.message_signal.show_message.connect(self.show_message_slot)
        # 로그아웃 확인값
        self.logout_bool = False
        # 초대장
        self.gb_invite.hide()
        self.lw_online_teacher_.itemDoubleClicked.connect(self.invite_teacher)
        self.btn_invite_Ok.clicked.connect(self.invite_OK)
        self.btn_invite_No.clicked.connect(self.invite_No)
    def invite_teacher(self):  # ["채팅초대", 보낸사람, 받는사람]
        teacher_name = self.lw_online_teacher_.currentItem().text()
        ans = QMessageBox.question(self, '채팅', f'{teacher_name}님을 초대하시겠습니까?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if ans == QMessageBox.Yes:
            invite_temp = ['채팅초대', self.login_user[3], teacher_name]
            invite_msg = json.dumps(invite_temp)
            print('json 변환')
            self.parent.client_socket.sendall(invite_msg.encode())
            print('sendall')
        else :
            return



    def show_qna(self):
        select_question = self.tw_qna_list.selectedItems()
        question_num = select_question[0].text()
        question_user_name = select_question[1].text()
        self.tb_qna.clear()
        for i in self.qna_list:
            if question_num == str(i[0]) and question_user_name == self.login_user[3]:
                self.tb_qna.append(f"문의번호: {i[0]}\n제목: {i[3]}\t작성자: {i[1]}\n내용: {i[4]}\n")
                if i[5]!= None:
                    self.tb_qna.append(f"답변\n>>{i[1]}님 안녕하세요.\n{i[5]}")
                break
    def question_Completed(self):
        title = self.le_question_title.text()
        question_contents = self.te_question.toPlainText()
        date = self.lb_date.text()
        if title == "" or question_contents == "":
            if title =="":
                self.message_signal.show_message.emit("제목을 입력해주세요.")
            else: self.message_signal.show_message.emit("내용을 입력해주세요.")
        else:
            question_temp = ['SCDB 문의추가',self.login_user[3],date,title,question_contents] # question_temp = ['SCDB 문의추가',이름,날짜,문의제목,문의내용]
            question_msg = json.dumps(question_temp)
            self.parent.client_socket.sendall(question_msg.encode())
            self.le_question_title.clear()
            self.te_question.clear()
            self.message_signal.show_message.emit("문의가 등록되었습니다.")
    def show_message_slot(self, message):
        title = self.parent.signal[0]
        if message == "입력하신 정보가 맞지 않습니다.":
            self.le_input_ID.clear()
            self.le_input_PW.clear()
            self.stw_login_join.setCurrentIndex(0)
        else:
            title = message[0:2]
        QMessageBox.information(self, title, message)
    def btn_logout_clicked(self):
        self.stw_main_stack.setCurrentIndex(0)
        self.stw_login_join.setCurrentIndex(0)
        logout_temp=['로그아웃',self.login_user[1],self.login_user[3], self.login_user[-1]] # logout_temp = ['로그아웃', ID, 이름, 학생]
        logout_msg = json.dumps(logout_temp)
        self.parent.client_socket.sendall(logout_msg.encode())
        self.logout_bool = True
    def login_msg_send(self):
        id = self.le_input_ID.text()
        pw = self.le_input_PW.text()
        self.le_input_ID.clear()
        self.le_input_PW.clear()
        self.le_show_ID.clear()
        login_temp = ['로그인',id,pw,'학생'] # login_temp = ['로그인', ID, PW, '학생']
        login_msg = json.dumps(login_temp)
        self.parent.client_socket.sendall(login_msg.encode())
    def login_result(self):
        self.stw_main_stack.setCurrentIndex(1)
        self.login_user = self.parent.signal[1::]
        self.setup_label()
        self.logout_bool = False
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
            conn = pymysql.connect(host='192.168.219.109', port=3306, user='root', password='00000000',
                                  db='education_app',
                                  charset='utf8')
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
        conn = pymysql.connect(host='192.168.219.109', port=3306, user='root', password='00000000', db='education_app',
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
            self.DB_request_QNA()
            self.stw_contents.setCurrentIndex(3)
        elif item_txt == "상담":
            self.stw_contents.setCurrentIndex(4)
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
    def DB_request_QNA(self):
        QNA_temp = ['SCDB요청 Q&A', self.login_user[1], self.login_user[3], self.login_user[-1]]  # logout_temp = ['로그아웃', ID, 이름, 학생]
        QNA_msg = json.dumps(QNA_temp)
        self.parent.client_socket.sendall(QNA_msg.encode())
        print(QNA_temp,'보냄')
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
            now = datetime.datetime.now()
            date_str = now.strftime('%Y-%m-%d')
            time_str = now.strftime('%H:%M:%S')
            self.lb_date.setText(date_str)
            self.lb_time.setText(time_str)
            time.sleep(1)
    def problem_solving(self, item, column):
        print('함수들어옴')
        question_name = item.text(column)
        print(question_name)
        self.lb_question_name_.setText(f"{question_name} 문제풀이")
    def closeEvent(self, QCloseEvent):
        ans = QMessageBox.question(self, "종료 확인", "종료 하시겠습니까?",
                                   QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if ans == QMessageBox.Yes:
            if not self.logout_bool:
                logout_temp = ['로그아웃', self.login_user[1], self.login_user[3], self.login_user[-1]]  # logout_temp = ['로그아웃', ID, 이름, 학생]
                logout_msg = json.dumps(logout_temp)
                self.parent.client_socket.sendall(logout_msg.encode())
            close_temp = ['종료', self.login_user[1], self.login_user[3], self.login_user[-1]]
            close_msg = json.dumps(close_temp)
            print('어디까지')
            self.parent.client_socket.sendall(close_msg.encode())
            QCloseEvent.accept()  # 이건 QCloseEvent가 발생하면 그렇게 행하라는 거다.
        else:
            print('취소')
            QCloseEvent.ignore()  # 이건 QCloseEvent가 발생하면 무시하라는 거다.

    def online_user_update(self,signal):
        self.lw_online_teacher_.clear()
        self.lw_online_student_.clear()
        online_student = signal[1]
        online_teacher = signal[2]
        print('왜 안나오고 지랄임?',online_student)
        for i in online_student: # 테스트용
            print('이거나와라',i[1])
            self.lw_online_student_.addItem(i[1])
        for i in online_teacher:
            print('@@@나와라',i[1])
            self.lw_online_teacher_.addItem(i[1])
        print('온라인유저 목록 업데이트')
    def QNA_list_update(self):
        print('메서드 진입')
        self.qna_list = self.parent.signal[1::]
        self.tw_qna_list.setRowCount(len(self.qna_list))
        for i in range(len(self.qna_list)):
            for j in range(len(self.qna_list[i])-1):
                self.tw_qna_list.setItem(i,j, QTableWidgetItem(str(self.qna_list[i][j])))
    def recv_invite(self): # signal = ["채팅초대", 보낸사람, 받는사람, 보낸사람 소켓]
        self.lb_invite_message.setText(f"{self.signal[1]}님이 상담을\n신청했습니다.")
        self.invite_sender = self.signal[1]
        self.gb_invite.show()
    def invite_OK(self):
        self.stw_contents.setCurrentIndex(4) # signal = ['채팅수락', 수락메시지, 받은 사람, 보낸사람]
        invite_OK_temp= ['채팅수락', "대화가 시작됩니다.", self.login_user[3],self.invite_sender]
        invite_accept_msg = json.dumps(invite_OK_temp)
        self.parent.client_socket.sendall(invite_accept_msg.encode())
        self.gb_invite.hide()

    def invite_No(self):
        self.gb_invite.hide()
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
                print('self.signal:',self.signal)
            except Exception as er:
                print(er)
                break
            else:
                if self.signal[0] == "로그인 완료":  #signal = ["로그인", [학생ID, 학생이름, 학생], [교사ID, 교사이름, 교사]]
                    self.contents.login_result()
                elif self.signal[0] == "로그인 실패":
                    self.contents.message_signal.show_message.emit("입력하신 정보가 맞지 않습니다.")
                elif self.signal[0] == "로그인":
                    self.contents.online_user_update(self.signal)
                elif self.signal[0] == "로그아웃":
                    self.contents.online_user_update(self.signal)
                elif self.signal[0] == "DB설명반환":  # signal = ["DB설명반환",생태,일반,이미지]
                    print("DB설명반환 메세지 받음")
                elif self.signal[0] == 'SC Q&A DB반환':
                    self.contents.QNA_list_update()
                    print("QNA DB 반환")
                elif self.signal[0] == "채팅초대":  #signal = ["채팅초대", 보낸사람, 받는사람]
                    self.contents.recv_invite()
                elif self.signal[0] == "채팅수락": # signal = ['채팅수락', 수락메시지, 수락한 사람, 보낸 사람]
                    self.contents.lw_chat.addItem(self.signal[1])

if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = QtWidgets.QStackedWidget()
    # 클래스의 객체 만들기
    # login = Login()
    student = Student()
    # contents = Contents(student)
    # 프로그램 화면을 보여주는 코드
    app.exec_()