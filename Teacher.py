import sys
from socket import *
from threading import *

from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import *
import urllib.request
from PyQt5.QtWidgets import *
from PyQt5 import uic
from os import environ
import time
import datetime
import json
import requests
import xmltodict
import pandas as pd
import bs4


encoding = '11xBqPRCrKxDRnzolBiWVGwhexbmYELfieu%2BGvVw7z2HYGWD67SB2EGIMJHoG8KYEvkNOd3LaHsvIp7cDZPhzg%3D%3D'
decoding = '11xBqPRCrKxDRnzolBiWVGwhexbmYELfieu+GvVw7z2HYGWD67SB2EGIMJHoG8KYEvkNOd3LaHsvIp7cDZPhzg=='
form_class = uic.loadUiType('./Teacher.ui')[0]


class MessageSignal(QObject):
    show_message = pyqtSignal(str)


class Main(QMainWindow, form_class):
    Client_socket = None

    def __init__(self, ip, port):
        super().__init__()
        self.setupUi(self)
        self.initialize_socket(ip, port)
        self.listen_thread()
        self.message_signal = MessageSignal()
        self.message_signal.show_message.connect(self.show_message_slot)
        self.login_stack.setCurrentIndex(0)
        self.mainstack.setCurrentIndex(0)
        self.test_update_search.clicked.connect(self.search_test_items)
        self.test_item_list_widget.itemClicked.connect(self.test_items_description)
        self.Test_Update_entry_btn.clicked.connect(self.entry_test)
        self.treeWidget.itemClicked.connect(self.on_item_clicked)
        self.item = ''
        self.test_update_search_LE.setText('')
        # ----------------------------------------------------------
        # 페이지 이동
        self.btn_next.clicked.connect(self.login_move_next)
        self.btn_prev.clicked.connect(self.login_move_prev)
        # ----------------------------------------------------------
        # ID 입력
        self.le_input_ID.returnPressed.connect(self.login_move_next)
        # ----------------------------------------------------------
        # 로그인 체크
        self.le_input_PW.returnPressed.connect(self.login_check)
        self.btn_move_main.clicked.connect(self.login_check)
        self.btn_logout.clicked.connect(self.btn_logout_clicked)
        self.logout_bool = False
        # 회원가입
        self.btn_check_id.clicked.connect(self.check_id)
        self.le_input_id.returnPressed.connect(self.check_id)
        self.le_input_id.textChanged.connect(self.change_id)
        self.btn_join_finish.clicked.connect(self.check_sign_up)
        self.btn_cancle.clicked.connect(self.move_login)
        self.btn_join.clicked.connect(self.move_join)
        self.btn_join2.clicked.connect(self.move_join)
        # QNA
        self.tw_qna_list.cellDoubleClicked.connect(self.show_qna)
        self.QnA_register_btn.clicked.connect(self.answer_register)
        self.consulting = False
        self.btn_consult_end.clicked.connect(self.consult_end)
        # 시간 스레드
        td_time = Thread(target=self.time_thread, daemon=True)  # 시간쓰레드
        td_time.start()

        # 실시간 채팅 초대
        self.gb_invite.hide()
        self.client_list_widget.itemDoubleClicked.connect(self.invite_student)
        self.btn_invite_Ok.clicked.connect(self.invite_OK)
        self.btn_invite_No.clicked.connect(self.invite_No)
        # 실시간 채팅 송신
        self.consult_chat_le.returnPressed.connect(self.send_chat)
        self.consult_chat_send.clicked.connect(self.send_chat)
        # 학생 시험 결과 불러오기
        self.test_result_groupbox.hide()
        self.student_list_lw.itemClicked.connect(self.call_student_test_result)

        pixmap = QPixmap("bg.jpg")
        pixmap = pixmap.scaled(1130, 840)
        self.background_label.setPixmap(pixmap)

    def btn_logout_clicked(self):
        self.mainstack.setCurrentIndex(0)
        self.login_stack.setCurrentIndex(0)
        logout_temp=['로그아웃',self.login_user[1],self.login_user[3], self.login_user[-1]] # logout_temp = ['로그아웃', ID, 이름, 학생]
        logout_msg = json.dumps(logout_temp)
        self.client_socket.sendall(logout_msg.encode())
        self.logout_bool = True

    def call_student_test_result(self):
        self.test_result_groupbox.show()
        # information ["TC시험결과요청",학생번호]
        student_name = self.student_list_lw.currentItem().text()
        for i in self.student_client_list:
            if student_name == i[3] :
                student_num= i[0]
                break
        information = ["TC시험결과요청", student_num]
        message = json.dumps(information)
        self.client_socket.sendall(message.encode())

    def consult_end(self):
        if self.consulting:
            self.Consult_chat_lw.clear()
            self.btn_consult_end.hide()
            self.consulting = False
        if self.signal[0] != '상담종료':
            consult_end_temp = ['상담종료', self.login_user[3], self.chat_partner]
            consult_end_msg = json.dumps(consult_end_temp)
            self.client_socket.sendall(consult_end_msg.encode())

    def time_thread(self):
        while True:
            time.sleep(1)
            now = datetime.datetime.now()
            date_str = now.strftime('%Y-%m-%d')
            time_str = now.strftime('%H:%M:%S')
            self.lb_date.setText(date_str)
            self.lb_time.setText(time_str)

    def send_chat(self):
        # information = ["실시간채팅",보낸사람,받는사람,메세지,시간]
        time = self.lb_time.text()
        send_message = self.consult_chat_le.text()
        information = ["실시간채팅", self.login_user[3], self.invite_sender, send_message, time]
        message = json.dumps(information)
        self.client_socket.sendall(message.encode())
        self.consult_chat_le.clear()

    def invite_student(self):  # ["채팅초대", 보낸사람, 받는사람]

        if self.consulting == False:
            student_name = self.client_list_widget.currentItem().text()
            ans = QMessageBox.question(self, '채팅', f'{student_name}님을 초대하시겠습니까?', QMessageBox.Yes | QMessageBox.No,
                                       QMessageBox.No)
            if ans == QMessageBox.Yes:
                invite_temp = ['채팅초대', self.login_user[3], student_name]
                invite_msg = json.dumps(invite_temp)
                self.client_socket.sendall(invite_msg.encode())

        else:
            QMessageBox.information(self, '초대', '상담중에는 다른 사람을 초대 할 수 없습니다.')

    def recv_invite(self):  # signal = ["채팅초대", 보낸사람, 받는사람, 보낸사람 소켓]
        if self.consulting == False:
            self.lb_invite_message.setText(f"{self.signal[1]}님이 상담을\n신청했습니다.")
            self.invite_sender = self.signal[1]
            self.gb_invite.show()
        else:
            invite_temp = ['이미 채팅중', f"{self.login_user[3]}님은\n이미 상담중입니다.", self.login_user[3], self.invite_sender]
            invite_already_msg = json.dumps(invite_temp)
            self.client_socket.sendall(invite_already_msg.encode())

    def invite_OK(self):
        self.stackedWidget.setCurrentIndex(4)  # signal = ['채팅수락', 수락메시지, 받은 사람, 보낸사람]
        invite_OK_temp = ['채팅수락', f"{self.lb_time.text()}\n대화가 시작됩니다.", self.login_user[3], self.invite_sender]
        invite_accept_msg = json.dumps(invite_OK_temp)
        self.client_socket.sendall(invite_accept_msg.encode())
        self.gb_invite.hide()
        self.btn_consult_end.show()
        self.consulting = True

    def invite_No(self):
        self.gb_invite.hide()
        self.consulting = False

    def answer_register(self):
        select_question = self.tw_qna_list.selectedItems()
        print(select_question)
        question_num = select_question[0].text()
        answer = self.QnA_linedit.text()
        answer_user_name = self.login_user[3]
        information = ["TC답변등록", question_num, answer, answer_user_name]
        message = json.dumps(information)
        self.client_socket.send(message.encode())
        self.QnA_linedit.clear()
        QMessageBox.information(self, "등록", "등록되었습니다")

    def move_join(self):
        self.login_stack.setCurrentIndex(2)

    def move_login(self):
        self.le_input_id.clear()
        self.le_input_pw.clear()
        self.le_check_pw.clear()
        self.le_input_name.clear()
        self.le_phonenum.clear()
        self.login_stack.setCurrentIndex(0)

    # 회원가입
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
            # DB 요청
            information = ["ID중복확인", id]
            message = json.dumps(information)
            self.client_socket.send(message.encode())

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
                information = ["회원가입", id, pw, name, '선생']
                message = json.dumps(information)
                self.client_socket.send(message.encode())
        else:
            QMessageBox.information(self, 'ID', 'ID 중복확인을 해주세요.')

    def sign_up_clear(self):
        self.le_input_id.clear()
        self.le_input_pw.clear()
        self.le_check_pw.clear()
        self.le_input_name.clear()
        self.le_phonenum.clear()

    def login_check(self):
        # signal = ["로그인", ID, PW]
        ID = self.le_show_ID.text()
        password = self.le_input_PW.text()
        information = ["로그인", ID, password, '선생']
        message = json.dumps(information)
        self.client_socket.send(message.encode())

    def login_move_next(self):
        input_id = self.le_input_ID.text()
        self.le_show_ID.setText(input_id)
        if input_id == "":
            QMessageBox.warning(self, 'ID 입력 오류', 'ID를 입력해주세요.')
        else:
            self.login_stack.setCurrentIndex(1)

    def login_move_prev(self):
        self.login_stack.setCurrentIndex(0)
        self.le_input_ID.clear()
        self.le_input_PW.clear()





    def on_item_clicked(self, item, column):
        self.item = item.text(column)

        actions = {"점수/통계확인(학생별)": (1, self.request_student_list),
                   "통계확인(문제별)": (2, self.request_test_statistics),
                   "Q&A": (3, self.DB_request_QNA),
                   "상담": (4, None)}
        a = item.parent()
        if a and a.text(column) == "문제 업데이트":
            self.stackedWidget.setCurrentIndex(0)
            self.clear_test_update()
        elif self.item in actions:
            index, func = actions[self.item]
            self.stackedWidget.setCurrentIndex(index)
            if func:
                func()
    def request_test_statistics(self):
        self.test_statistics.clearContents()
        self.test_statistics_2.clearContents()
        information = ["TC문제통계요청"]
        message = json.dumps(information)  # 제이슨 변환
        self.client_socket.send(message.encode())  # 서버에 정보 전달

    def request_student_list(self):
        self.student_list_lw.clear()
        information = ["TC학생DB요청"]
        message = json.dumps(information)  # 제이슨 변환
        self.client_socket.send(message.encode())  # 서버에 정보 전달

    def entry_test(self):
        if self.item == '':
            self.item = '포유류'
        test_contents = self.test_contents.text()  # 문제 내용
        test_correct_answer = self.test_answer.text()  # 문제 정답
        test_contents_name = self.test_item_list_widget.currentItem().text()
        if test_contents == "문제 내용을 입력해주세요":
            return
        if test_correct_answer == "정답을 입력해주세요":
            return
        information = ["TC문제등록", test_contents, self.img_URL, test_correct_answer, self.item,
                       test_contents_name]  # 문제내용, URL , 정답, 분류, 항목이름
        message = json.dumps(information)  # 제이슨 변환
        self.clear_test_update()  # 문제 등록 UI 초기화 메서드 호출
        self.client_socket.send(message.encode())  # 서버에 정보 전달

    def clear_test_update(self):
        self.test_update_search_LE.clear()
        self.test_item_list_widget.clear()
        self.textBrowser.clear()
        self.test_contents.setText("문제 내용을 입력해주세요")

    def chat_update(self):
        if self.consulting:
            chat_message = f"{self.signal[1]} : {self.signal[3]}"
            self.Consult_chat_lw.addItem(self.signal[4])
            self.Consult_chat_lw.addItem(chat_message)

    def show_qna(self):
        select_question = self.tw_qna_list.selectedItems()
        print(select_question)
        question_num = select_question[0].text()
        question_user_name = select_question[1].text()
        self.tb_qna.clear()
        for i in self.qna_list:
            if question_num == str(i[0]):
                self.tb_qna.append(f"문의번호: {i[0]}\n제목: {i[3]}\t작성자: {i[1]}\n내용: {i[4]}\n")
                if i[5] != None:
                    self.tb_qna.append(f"답변\n>>{i[1]}님 안녕하세요.\n{i[6]}입니다.\n{i[5]}")
                break

    def QNA_list_update(self):
        print('메서드 진입')
        self.qna_list = self.signal[1:]
        self.tw_qna_list.setRowCount(len(self.qna_list))
        for i in range(len(self.qna_list)):
            for j in range(len(self.qna_list[i]) - 1):
                self.tw_qna_list.setItem(i, j, QTableWidgetItem(str(self.qna_list[i][j])))

    def DB_request_QNA(self):
        # self.login_user = [1, 'ksi', '1234', '김성일', 0, '4', '학생']
        QNA_temp = ['SCDB요청 Q&A', self.login_user[1], self.login_user[3], self.login_user[-1]]
        QNA_msg = json.dumps(QNA_temp)
        self.client_socket.sendall(QNA_msg.encode())
        print(QNA_temp, '보냄')



    def receive_message(self, socket):
        """
        서버에서 전달하는 메시지를 수신하는 스레드
        """

        while True:
            try:
                incoming_message = socket.recv(8192)
                self.signal = json.loads(incoming_message.decode())
                print(self.signal)
            except Exception as e:
                print(e)
                print("오류남")
                break
            else:
                if self.signal[0] == "DB검색반환":  # signal = ["DB검색반환",1,2,3,4 ....]
                    print("검색반환메세지받음")
                    self.update_test_item_widget_db()
                elif self.signal[0] == "DB설명반환":  # signal = ["DB설명반환",생태,일반,이미지]
                    print("DB설명반환 메세지 받음")
                    self.update_description_db()
                elif self.signal[0] == "로그인 완료":  # signal = ['로그인 완료', 3, 'lsb', '1234', '이상복', 0, '0', '선생']
                    self.move_main()
                elif self.signal[0] == "로그인 실패":
                    self.message_signal.show_message.emit("잘못 입력했습니다.\n다시 입력해주세요.")
                elif self.signal[0] == "로그인":  # signal = ['로그인', self.student_list, self.teacher_list]
                    self.client_list_widget.clear()
                    for i in self.signal[1]:
                        self.client_list_widget.addItem(i[1])
                elif self.signal[0] == "로그아웃":  # signal = ['로그아웃', self.student_list, self.teacher_list]
                    self.client_list_widget.clear()
                    for i in self.signal[1]:
                        self.client_list_widget.addItem(i[1])
                elif self.signal[0] == "중복 없음":
                    self.message_signal.show_message.emit("사용가능한 ID 입니다.")
                    self.use_id = True
                    self.btn_check_id.setEnabled(False)
                elif self.signal[0] == "ID 중복":
                    self.message_signal.show_message.emit("이미 사용중인 ID 입니다.")
                elif self.signal[0] == "가입 완료":
                    self.message_signal.show_message.emit("회원가입이 완료되었습니다")
                    self.login_stack.setCurrentIndex(0)
                    self.sign_up_clear()
                elif self.signal[0] == 'SC Q&A DB반환':
                    self.QNA_list_update()
                elif self.signal[0] == '학생DB반환':
                    self.student_list_update()
                elif self.signal[0] == "채팅초대":  # signal = ["채팅초대", 보낸사람, 받는사람]
                    self.recv_invite()
                elif self.signal[0] == "채팅수락":  # signal = ['채팅수락', 수락메시지, 수락한 사람, 보낸 사람]
                    self.Consult_chat_lw.addItem(self.signal[1])
                    if self.signal[2] == self.login_user[3] :
                        self.invite_sender = self.signal[3]
                    else :
                        self.invite_sender = self.signal[2]
                    self.btn_consult_end.show()
                    self.consulting = True
                elif self.signal[0] == "실시간채팅":  # signal = ["실시간채팅",보낸사람,받는사람,메세지,시간]
                    self.chat_update()
                elif self.signal[0] == "이미 채팅중":  # signal= ['이미 채팅중', '000님은\n이미 상담중입니다.', 초대받은사람, 초대한사람]
                    self.message_signal.show_message.emit("이미 상담중입니다")
                elif self.signal[0] == "학생성적반환":
            # information = ["학생성적반환",correct_test_question_num,Total_test_question_num,insect_correct_question_num,
            # insect_question_num,mammal_correct_question_num,mammal_question_num,bird_correct_question_num,bird_question_num]
                    self.call_student_test_record()
                elif self.signal[0] == "TC문제통계반환" : # signal = ["TC문제통계반환" , 리스트1(정답률) , 리스트2(소요시간)]
                    self.update_test_statistics()
                elif self.signal[0] == "상담종료": # signal = ["상담종료"]
                    self.consult_end()
    def update_test_statistics(self):
        rate_list = self.signal[1]
        time_list = self.signal[2]
        self.test_statistics.clearContents()
        self.test_statistics_2.clearContents()
        self.test_statistics.setRowCount(len(rate_list))
        self.test_statistics.setColumnCount(len(rate_list[0]))
        for j in range(len(rate_list)):
            for k in range(len(rate_list[j])):
                self.test_statistics.setItem(j, k, QTableWidgetItem(str(rate_list[j][k])))

        self.test_statistics.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.test_statistics.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.test_statistics.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.test_statistics.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)
        self.test_statistics.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeToContents)

        self.test_statistics_2.setRowCount(len(time_list))
        self.test_statistics_2.setColumnCount(len(time_list[0]))
        for j in range(len(time_list)):
            for k in range(len(time_list[j])):
                self.test_statistics_2.setItem(j, k, QTableWidgetItem(str(time_list[j][k])))
        for i in range(len(time_list[0])):
            self.test_statistics_2.horizontalHeader().setSectionResizeMode(i, QHeaderView.Stretch)

    def call_student_test_record(self):
        self.test_record = self.signal[1:]
        print(self.test_record)
        self.correct_lbl.setText(str(self.test_record[0]))
        self.all_lbl.setText(str(self.test_record[1]))
        self.insect_correct_lbl.setText(str(self.test_record[2]))
        self.insect_all_lbl.setText(str(self.test_record[3]))
        self.mammal_correct_lbl.setText(str(self.test_record[4]))
        self.mammal_all_lbl.setText(str(self.test_record[5]))
        self.bird_correct_lbl.setText(str(self.test_record[6]))
        self.bird_all_lbl.setText(str(self.test_record[7]))
        try :
            a = round(self.test_record[0]/self.test_record[1]*100,3)
            print(a)
            self.correct_rate_lbl.setText(str(a)+'%')
        except ZeroDivisionError :
            self.correct_rate_lbl.setText('')
        try :
            a = round(self.test_record[2]/self.test_record[3]*100,3)
            print(a)
            self.insect_correct_rate_lbl.setText(str(a)+'%')
        except ZeroDivisionError :
            self.insect_correct_rate_lbl.setText('')
        try :
            a = round(self.test_record[4]/self.test_record[5]*100,3)
            print(a)
            self.mammal_correct_rate_lbl.setText(str(a)+'%')
        except ZeroDivisionError :
            self.mammal_correct_rate_lbl.setText('')
        try :
            a = round(self.test_record[6]/self.test_record[7]*100,3)
            print(a)
            self.bird_correct_rate_lbl.setText(str(a)+'%')
        except ZeroDivisionError :
            self.bird_correct_rate_lbl.setText('')


    def student_list_update(self):
        self.student_client_list = self.signal[1:]
        print(self.student_client_list)
        for i in self.student_client_list:
            self.student_list_lw.addItem(i[3])

    def show_message_slot(self, message):
        QMessageBox.information(self, "정보", message)

    def move_main(self):
        # login_info = ['로그인 완료', 1, 'ksi', '1234', '김성일', 0, '4', '학생']
        self.login_user = self.signal[1:]
        # print(self.login_user)
        self.mainstack.setCurrentIndex(1)
        self.user_name_label.setText(f"{self.signal[4]}님 안녕하세요")

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
        self.df = pd.DataFrame(result, columns=['insctPilbkNo', 'insctofnmkrlngnm'])
        for i in range(len(self.df)):
            self.test_item_list_widget.addItem(self.df.iloc[i]['insctofnmkrlngnm'])

    def test_items_description(self):
        self.textBrowser.clear()
        if self.item == '포유류':
            try:
                self.test_items_description_mammal()
            except:
                self.test_items_description_db()

        elif self.item == '곤충':
            try:
                self.test_items_description_insect()
            except:
                self.test_items_description_db()
        elif self.item == '조류':
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
        information = ["DB설명요청", self.item, selected_item]
        message = json.dumps(information)
        self.client_socket.send(message.encode())
    def closeEvent(self, QCloseEvent):
        ans = QMessageBox.question(self, "종료 확인", "종료 하시겠습니까?",
                                   QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if ans == QMessageBox.Yes:
            # if not self.logout_bool:
            #     logout_temp = ['로그아웃', self.login_user[1], self.login_user[3], self.login_user[-1]]  # logout_temp = ['로그아웃', ID, 이름, 학생]
            #     logout_msg = json.dumps(logout_temp)
            #     self.client_socket.sendall(logout_msg.encode())
            if self.login_user :
                close_temp = ['종료', self.login_user[1], self.login_user[3], self.login_user[-1]]
            else :
                close_temp = ["종료",'-','-','-']
            close_msg = json.dumps(close_temp)
            print('어디까지')
            self.client_socket.sendall(close_msg.encode())
            QCloseEvent.accept()  # 이건 QCloseEvent가 발생하면 그렇게 행하라는 거다.
        else:
            print('취소')
            QCloseEvent.ignore()  # 이건 QCloseEvent가 발생하면 무시하라는 거다.

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
