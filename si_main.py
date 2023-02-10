from socket import *
from threading import *
import datetime
import time
import sys
import pymysql
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5 import uic
import requests
import xmltodict
import json
import urllib.request
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import *



# 메시지박스 클래스
class MessageSignal(QObject):
    show_message = pyqtSignal(str)

contents_form_class = uic.loadUiType("si_contents.ui")[0]
class Contents(QWidget, contents_form_class): # 학생 클라이언트 클래스
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
        self.btn_join.clicked.connect(self.move_prev)
        self.btn_join2.clicked.connect(self.move_prev)
        self.le_input_PW.returnPressed.connect(self.login_msg_send)
        self.btn_move_main.clicked.connect(self.login_msg_send)
        self.btn_check_id.clicked.connect(self.check_id)
        self.le_input_id.returnPressed.connect(self.check_id)
        self.le_input_id.textChanged.connect(self.change_id)
        self.btn_join_finish.clicked.connect(self.check_sign_up)
        self.btn_cancle.clicked.connect(self.move_login)
        # Q&A
        self.tw_qna_list.cellDoubleClicked.connect(self.show_qna)
        self.btn_question_finish.clicked.connect(self.question_Completed)
        # ----------------------------------------------------------
        # 메시지 박스
        self.message_signal = MessageSignal()
        self.message_signal.show_message.connect(self.show_message_slot)
        # 로그아웃 확인값
        self.logout_bool = False
        # 실시간 상담
        self.gb_invite.hide()
        self.lw_online_teacher_.itemDoubleClicked.connect(self.invite_teacher)
        self.btn_invite_Ok.clicked.connect(self.invite_OK)
        self.btn_invite_No.clicked.connect(self.invite_No)
        self.le_message.returnPressed.connect(self.send_chat)
        self.btn_send_message.clicked.connect(self.send_chat)
        self.btn_consult_end.hide()
        self.consulting = False
        self.btn_consult_end.clicked.connect(self.consult_end)
        # 문제풀이
        self.btn_test_start.clicked.connect(self.test_start)
        self.btn_submit.clicked.connect(lambda :self.test_submit(None))
        self.le_input_answer.returnPressed.connect(lambda :self.test_submit(None))
        self.btn_answer_O.clicked.connect(lambda :self.test_submit('O'))
        self.btn_answer_X.clicked.connect(lambda: self.test_submit('X'))
        # 학습
        self.btn_learning_finish_.clicked.connect(self.learning_completed)
        # 배경
        pixmap = QPixmap("bg.jpg")
        pixmap = pixmap.scaled(self.background_label.width(), self.background_label.height(), Qt.KeepAspectRatio,
                                       Qt.SmoothTransformation)
        self.background_label.setPixmap(pixmap)


        # 학습완료 DB요청 메서드
    def learning_completed(self): # completed_temp = ['학습완료', 1, '산굴뚝나비', '1산굴뚝나비']
        item = self.lw_learning_list_.currentItem().text()
        uniq_key = str(self.login_user[0]) + item
        print(uniq_key)
        completed_temp = ['학습완료', self.login_user[0], item, uniq_key]
        completed_msg = json.dumps(completed_temp)
        self.parent.client_socket.sendall(completed_msg.encode())
    # Q&A 리스트 클릭시 QNA 내용을 보여주는 메서드
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
    # 문의완료 메서드
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

    # 로그아웃시 서버에 로그아웃 메시지를 보냄
    def btn_logout_clicked(self):
        self.stw_main_stack.setCurrentIndex(0)
        self.stw_login_join.setCurrentIndex(0)
        logout_temp=['로그아웃',self.login_user[1],self.login_user[3], self.login_user[6]] # logout_temp = ['로그아웃', ID, 이름, 학생]
        logout_msg = json.dumps(logout_temp)
        self.parent.client_socket.sendall(logout_msg.encode())
        self.logout_bool = True
    # 로그인시에 로그인 한 값을 보내고 확인요청하는 메서드
    def login_msg_send(self):
        id = self.le_input_ID.text()
        pw = self.le_input_PW.text()
        login_temp = ['로그인',id,pw,'학생'] # login_temp = ['로그인', ID, PW, '학생']
        login_msg = json.dumps(login_temp)
        self.parent.client_socket.sendall(login_msg.encode())
    # 로그인 결과를 받는 메서드
    def login_result(self):
        self.login_user = self.parent.signal[1::]
        self.setup_label()
        self.stw_main_stack.setCurrentIndex(1)
        self.logout_bool = False
        self.le_input_ID.clear()
        self.le_input_PW.clear()
        self.le_show_ID.clear()
    # 로그인시 스택변경
    def move_next(self):
        input_id = self.le_input_ID.text()
        self.le_show_ID.setText(input_id)
        if input_id=="":
            QMessageBox.warning(self, 'ID 입력 오류', 'ID를 입력해주세요.')
        else:
            self.stw_login_join.setCurrentIndex(1)
    # 로그인시 스택변경
    def move_prev(self):
        self.stw_login_join.setCurrentIndex(0)
        self.le_input_ID.clear()
        self.le_input_PW.clear()
    # 회원가입 페이지로 스택변경
    def move_prev(self):
        self.stw_login_join.setCurrentIndex(2)
    # 회원가입 완료시 로그인페이지로 스택변경해주는 메서드
    def move_login(self):
        self.sign_up_clear()
        self.stw_login_join.setCurrentIndex(0)
    # 아이디 라인에디터의 값이 변경되면 다시 중복확인을 하게 하는 메서드
    def change_id(self):
        self.use_id = False
        self.btn_check_id.setEnabled(True)
    # 아이디 중복확인 메서드
    def check_id(self):
        print('체크아이디')
        id = self.le_input_id.text()
        self.use_id = False
        if len(id) < 3:
            self.le_input_id.clear()
            QMessageBox.information(self, "ID", "ID가 너무 짧습니다.\n3자 이상으로 입력해주세요")
        else:
            print('saddsa')
            # DB 요청
            information = ["ID중복확인", id]
            message = json.dumps(information)
            self.parent.client_socket.send(message.encode())
    # 회원가입시 입력값 확인하는 메서드
    def check_sign_up(self):
        id = self.le_input_id.text()
        pw = self.le_input_pw.text()
        chk_pw = self.le_check_pw.text()
        name = self.le_input_name.text()
        phonenum = self.le_phonenum.text()
        self.join = [id, pw, chk_pw, name, phonenum]
        what_NULL = ['ID', 'PW', '이름', '휴대폰번호']
        print(self.join)
        for line_edit in self.join:
            if line_edit == "":
                NULL_index = self.join.index(line_edit)
                QMessageBox.information(self, "NULL", f"{what_NULL[NULL_index]}를 입력해주세요.")
                return
        if self.use_id:
            if self.join[1] == self.join[2]:
                information = ["회원가입", id, pw, name, '학생']
                message = json.dumps(information)
                self.parent.client_socket.send(message.encode())
        else:
            QMessageBox.information(self, 'ID', 'ID 중복확인을 해주세요.')
    # 회원가입 창에 있는 라인에디터 클리어
    def sign_up_clear(self):
        self.le_input_id.clear()
        self.le_input_pw.clear()
        self.le_check_pw.clear()
        self.le_input_name.clear()
        self.le_phonenum.clear()
    # 로그인시 정보가 필요한 ui들 값을 넣어주는 메서드
    def setup_label(self):
        print('!!!!!',self.login_user)
        rank = 5 - (self.login_user[4]//3000)
        self.lb_check_name.setText(f'{self.login_user[3]}님 안녕하세요.')
        self.lb_user_name_.setText(self.login_user[3])
        self.lb_point_num.setText(str(self.login_user[4]))
        self.lb_rank_num.setText(str(rank))
        self.lb_question_num.setText(str(self.login_user[7][0]))
        self.lb_learning_num.setText(str(self.login_user[7][1]))
        td_time = Thread(target=self.time_thread, daemon=True)  # 시간쓰레드
        td_time.start()
        print('실시간 시간 쓰레드')
    # 메뉴 스택변경
    def show_menu(self):
        self.stw_menu.setCurrentIndex(1)
    # 메뉴 스택변경
    def hide_menu(self):
        self.stw_menu.setCurrentIndex(0)
    # 트리위젯 클릭시 선택한 메뉴의 값을 확인 시켜주는 메서드
    def show_contents(self, item, column):
        item_txt = item.text(column)
        if self.stw_test_timer.currentIndex() == 0:
            if item_txt == "개인정보":
                print('개인정보')
                self.stw_contents.setCurrentIndex(0)
                self.user_label_update()
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
        else: QMessageBox.information(self, '시험','시험중에는 이용할 수 없습니다.')
    # 개인정보를 눌렀을 때 업데이트된 유저 정보를 받기 위해 서버에 요청함
    def user_label_update(self):
        login_temp = ['로그인', self.login_user[1], self.login_user[2], '학생']  # login_temp = ['로그인', ID, PW, '학생']
        login_msg = json.dumps(login_temp)
        self.parent.client_socket.sendall(login_msg.encode())
    # 시험 시작시 문제요청하는 메서드
    def test_start(self):
        self.test_submit_list = []
        self.test_index = 0
        test_subject = self.lb_question_name_.text()[:2]
        request_temp = ['SCDB요청 문제', self.login_user[0],test_subject] #request_temp = ['SCDB요청 문제', ID_Num]
        request_test_msg = json.dumps(request_temp)
        self.parent.client_socket.sendall(request_test_msg.encode())
        print(request_test_msg, '보냄')
    # 서버에서 받아온 시험문제를 차례대로 보여주는 메서드
    def test_show(self, test_index): # ['SCDB요청 반환',[Test_num, Test_contents, Test_img_URL, Test_correct_answer, Test_subject, Test_contents_name]]
        self.test_list = self.parent.signal[1::]
        self.lb_test_num.setText(str(self.test_list[test_index][0]))
        self.tb_test_explanation.append(self.test_list[test_index][1])
        if self.test_list[test_index][3] == 'O' or self.test_list[test_index][3] == 'X':
            self.stw_answerpaper.setCurrentIndex(2)
        else: self.stw_answerpaper.setCurrentIndex(1)
        imageFromWeb = urllib.request.urlopen(self.test_list[test_index][2]).read()
        qPixmapVar = QPixmap()
        qPixmapVar.loadFromData(imageFromWeb)
        qPixmapVar = qPixmapVar.scaled(self.lb_test_img.width(), self.lb_test_img.height(), Qt.KeepAspectRatio,
                                       Qt.SmoothTransformation)
        self.lb_test_img.setPixmap(qPixmapVar)
        self.stw_test_timer.setCurrentIndex(1)
        self.stw_menu.setCurrentIndex(0)
        self.test_index += 1
        self.begin = time.time()
    # 정답 체점해서 차례대로 담고 끝났을 경우 test_result_request을 실행시키는 메서드
    def test_submit(self, answer):
        try:
            if answer == None:
                answer = self.le_input_answer.text()
            self.test_paper_clear()
            test_num = int(self.lb_test_num.text())
            end = time.time()
            insert_time = end - self.begin
            if answer == self.test_list[self.test_index-1][3]:
                result = 'correct'
            else: result = 'wrong'
            temp = [test_num, result, round(insert_time,2)]
            self.test_submit_list.append(temp)
            if self.test_index == len(self.test_list):
                self.test_paper_clear()
                self.test_stack_clear()
                marking= marking_paper(self)
                marking.exec_()
            else: self.test_show(self.test_index)
        except Exception as er:
            print('에러',er)
            self.test_paper_clear()
            self.test_stack_clear()
    # 서버에 체점한 값을 보내주는 메서드
    def test_result_request(self):
        request_temp = ['SCDB시험 결과', self.login_user[0]]  # request_temp = ['SCDB시험 결과', ID_Num,[[시험결과]]]
        for i in self.test_submit_list:
            request_temp.append(i)
        request_test_result_msg = json.dumps(request_temp)
        self.parent.client_socket.sendall(request_test_result_msg.encode())
        print('서버에 요청함(테스트 결과)')
    # 시험지 클리어
    def test_paper_clear(self):
        self.le_input_answer.clear()
        self.lb_test_img.clear()
        self.tb_test_explanation.clear()
    # 시험이 끝날 경우 실행되는 메서드
    def test_stack_clear(self):
        self.stw_answerpaper.setCurrentIndex(0)
        self.stw_test_timer.setCurrentIndex(0)
    # QNA DB 값을 요청하는 메서드
    def DB_request_QNA(self):
        QNA_temp = ['SCDB요청 Q&A', self.login_user[1], self.login_user[3], self.login_user[6]]  # QNA_temp = ['SCDB요청', ID, 이름, 학생]
        QNA_msg = json.dumps(QNA_temp)
        self.parent.client_socket.sendall(QNA_msg.encode())
        print(QNA_temp,'보냄')

    # QNA를 테이블 위젯에 넣어주는 메서드
    def QNA_list_update(self):
        print('메서드 진입')
        self.qna_list = self.parent.signal[1::]
        self.tw_qna_list.setRowCount(len(self.qna_list))
        for i in range(len(self.qna_list)):
            for j in range(len(self.qna_list[i]) - 1):
                self.tw_qna_list.setItem(i, j, QTableWidgetItem(str(self.qna_list[i][j])))
    # 어떤 학습자료인지 확인하고 해당 하는 자료의 API를 불러오는 메서드
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
    # API 자료를 가져와서 해당 동물의 이미지와 설명을 보여주는 메서드
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
    # 실시간 시간 띄워주는 쓰레드 메서드
    def time_thread(self):
        while True:
            now = datetime.datetime.now()
            date_str = now.strftime('%Y-%m-%d')
            time_str = now.strftime('%H:%M:%S')
            self.lb_date.setText(date_str)
            self.lb_time.setText(time_str)
            time.sleep(1)
    # 문제풀이 종류 확인하는 메서드
    def problem_solving(self, item, column):
        print('함수들어옴')
        question_name = item.text(column)
        print(question_name)
        self.lb_question_name_.setText(f"{question_name} 문제풀이")
    # 종료이벤트 로그아웃 하기전에 종료하면 로그아웃 부터 시키고 종료시킴
    def closeEvent(self, QCloseEvent):
        ans = QMessageBox.question(self, "종료 확인", "종료 하시겠습니까?",
                                   QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if ans == QMessageBox.Yes:
            if not self.logout_bool:
                logout_temp = ['로그아웃', self.login_user[1], self.login_user[3], self.login_user[6]]  # logout_temp = ['로그아웃', ID, 이름, 학생]
                logout_msg = json.dumps(logout_temp)
                self.parent.client_socket.sendall(logout_msg.encode())
            close_temp = ['종료', self.login_user[1], self.login_user[3], self.login_user[6]]
            close_msg = json.dumps(close_temp)
            self.parent.client_socket.sendall(close_msg.encode())
            QCloseEvent.accept()  # 이건 QCloseEvent가 발생하면 그렇게 행하라는 거다.
        else:
            print('취소')
            QCloseEvent.ignore()  # 이건 QCloseEvent가 발생하면 무시하라는 거다.
    # 유저 로그인/로그아웃시 온라인한 유저의 리스를 다시 업데이트 하는 메서드
    def online_user_update(self,signal):
        self.lw_online_teacher_.clear()
        self.lw_online_student_.clear()
        online_student = signal[1]
        online_teacher = signal[2]
        for i in online_student: # 테스트용
            self.lw_online_student_.addItem(i[1])
        for i in online_teacher:
            self.lw_online_teacher_.addItem(i[1])
        print('온라인유저 목록 업데이트')
    # 선생님에게 상담신청을 하면 서버에 메시지를 보내는 메서드

    def invite_teacher(self):  # ["채팅초대", 보낸사람, 받는사람]
        if not self.consulting:
            teacher_name = self.lw_online_teacher_.currentItem().text()
            ans = QMessageBox.question(self, '채팅', f'{teacher_name}님을 초대하시겠습니까?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if ans == QMessageBox.Yes:
                invite_temp = ['채팅초대', self.login_user[3], teacher_name]
                invite_msg = json.dumps(invite_temp)
                print(f"{teacher_name}님에게 상담을 신청합니다.")
                self.parent.client_socket.sendall(invite_msg.encode())
        else: QMessageBox.information(self, '초대', '상담중에는 다른사람을 초대 할 수 없습니다.')
    # 메시지박스 메서드
    def show_message_slot(self, message):
        title = self.parent.signal[0]
        if message == "입력하신 정보가 맞지 않습니다.":
            self.le_input_ID.clear()
            self.le_input_PW.clear()
            self.stw_login_join.setCurrentIndex(0)
        elif message == '사용가능한 ID 입니다.':
            title = '회원가입'
        elif '이미 상담중입니다' in message:
            title = '상담중'
        else:
            title = message[0:2]
        QMessageBox.information(self, title, message)
    # 메시지 전송 서버요청 메서드
    def send_chat(self):
        # information = ["실시간채팅",보낸사람,받는사람,메세지,시간]
        time = self.lb_time.text()
        send_message = self.le_message.text()
        information = ["실시간채팅", self.login_user[3], self.chat_partner, send_message, time]
        message = json.dumps(information)
        self.parent.client_socket.sendall(message.encode())
        self.le_message.clear()
    # 메시지를 보내거나 받았을 경우 업데이트 시켜주는 메서드
    def chat_update(self):
        if self.consulting:
            chat_message = f"{self.parent.signal[1]} : {self.parent.signal[3]}"
            self.lw_chat.addItem(self.parent.signal[4])
            self.lw_chat.addItem(chat_message)
    # 상담종료 메서드
    def consult_end(self):
        if self.consulting:
            self.lw_chat.clear()
            self.btn_consult_end.hide()
            self.consulting = False
        if self.parent.signal[0] != '상담종료':
            consult_end_temp = ['상담종료', self.login_user[3], self.chat_partner]
            consult_end_msg = json.dumps(consult_end_temp)
            self.parent.client_socket.sendall(consult_end_msg.encode())
    # 초대를 받았을 경우 실행되는 메서드

    def recv_invite(self): # signal = ["채팅초대", 보낸사람, 받는사람, 보낸사람 소켓]
        if not self.consulting:
            self.lb_invite_message.setText(f"{self.parent.signal[1]}님이 상담을\n신청했습니다.")
            self.invite_sender = self.parent.signal[1]
            self.gb_invite.show()
        else:
            invite_temp = ['이미 채팅중', f"{self.login_user[3]}님은\n이미 상담중입니다.", self.login_user[3], self.invite_sender]
            invite_already_msg = json.dumps(invite_temp)
            self.parent.client_socket.sendall(invite_already_msg.encode())
    # 초대수락 메서드
    def invite_OK(self):
        self.stw_contents.setCurrentIndex(4) # signal = ['채팅수락', 수락메시지, 받은 사람, 보낸사람]
        invite_OK_temp= ['채팅수락', f"{self.lb_time.text()}\n대화가 시작됩니다.", self.login_user[3],self.invite_sender]
        invite_accept_msg = json.dumps(invite_OK_temp)
        self.parent.client_socket.sendall(invite_accept_msg.encode())
        self.gb_invite.hide()
        self.consulting = True
    # 초대 거절 메서드
    def invite_No(self):
        self.gb_invite.hide()
class Student: # 서버와 연동되는 클래스
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
                elif self.signal[0] == "중복 없음":
                    self.contents.message_signal.show_message.emit("사용가능한 ID 입니다.")
                    self.contents.use_id = True
                    self.contents.btn_check_id.setEnabled(False)
                elif self.signal[0] == "ID 중복":
                    self.contents.message_signal.show_message.emit("이미 사용중인 ID 입니다.")
                elif self.signal[0] == "가입 완료":
                    self.contents.message_signal.show_message.emit("회원가입이 완료되었습니다")
                    self.contents.stw_login_join.setCurrentIndex(0)
                    self.contents.sign_up_clear()
                elif self.signal[0] == "DB설명반환":  # signal = ["DB설명반환",생태,일반,이미지]
                    print("DB설명반환 메세지 받음")
                elif self.signal[0] == 'SC Q&A DB반환':
                    self.contents.QNA_list_update()
                    print("QNA DB 반환")
                elif self.signal[0] == "채팅초대":  #signal = ["채팅초대", 보낸사람, 받는사람]
                    self.contents.recv_invite()
                    print(f"{self.signal[1]}님의 채팅초대")
                elif self.signal[0] == "채팅수락":  # signal = ['채팅수락', 수락메시지, 수락한 사람, 보낸 사람]
                    self.contents.lw_chat.addItem(self.signal[1])
                    if self.signal[2] == self.contents.login_user[3]:
                        self.contents.chat_partner = self.signal[3]
                    else:
                        self.contents.chat_partner = self.signal[2]
                    self.contents.consulting = True
                    self.contents.btn_consult_end.show()
                elif self.signal[0] == "상담종료": # signal = ["상담종료"]
                    self.contents.consult_end()
                elif self.signal[0] == "실시간채팅":  # signal = ["실시간채팅",보낸사람,받는사람,메세지,시간]
                    self.contents.chat_update()
                elif self.signal[0] == "이미 채팅중":  # signal= ['이미 채팅중', '000님은\n이미 상담중입니다.', 초대받은사람, 초대한사람]
                    self.contents.message_signal.show_message.emit(self.signal[1])
                elif self.signal[0] == "SCDB요청 반환": #signal = ['SCDB요청 반환',[Test_num, Test_contents, Test_img_URL, Test_correct_answer, Test_subject, Test_contents_name]
                    self.contents.test_show(self.contents.test_index)

marking_form_class = uic.loadUiType("marking.ui")[0]
class marking_paper(QDialog, marking_form_class):
    def __init__(self,parent):
        super().__init__()
        self.parent = parent
        self.setupUi(self)
        self.btn_ok.clicked.connect(self.button_clicked)
        for i in range(len(self.parent.test_submit_list)):
            for j in range(len(self.parent.test_submit_list[i])):
                self.tw_marking.setItem(i, j, QTableWidgetItem(str(self.parent.test_submit_list[i][j])))
    def button_clicked(self):
        self.close()
        self.parent.test_result_request()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = QtWidgets.QStackedWidget()
    # 클래스의 객체 만들기
    # login = Login()
    student = Student()
    # contents = Contents(student)
    # 프로그램 화면을 보여주는 코드
    app.exec_()