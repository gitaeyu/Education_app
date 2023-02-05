import sys
import pymysql
import threading
import time
import pymysql
import time
import sys
import csv
import pymysql
from PyQt5 import QtWidgets
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5 import uic




login_form_class = uic.loadUiType("si_login.ui")[0]

class Login(QWidget, login_form_class):
    def __init__(self):
        super().__init__()
        # ui 불러오기, 객체 생성
        self.setupUi(self)
        self.stackedWidget.setCurrentIndex(0)
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
        self.le_input_PW.returnPressed.connect(self.move_main)
        self.btn_move_main.clicked.connect(self.move_main)
        # ----------------------------------------------------------
        # 로그인페이지 이미지
        # pixmap = QPixmap('login_img.png')
        # self.lb_login_img.setPixmap(pixmap)
        # self.lb_login_img.move(0,0)
        # ----------------------------------------------------------
        # 회원가입
        self.btn_check_id.clicked.connect(self.check_id)
        self.le_input_id.returnPressed.connect(self.check_id)
        self.le_input_id.textChanged.connect(self.change_id)
        self.btn_join_finish.clicked.connect(self.check_sign_up)
        self.btn_cancle.clicked.connect(self.move_login)

    def move_main(self):
        widget.setCurrentIndex(1)
        contents.show()
        self.close()

    def move_next(self):
        input_id = self.le_input_ID.text()
        self.le_show_ID.setText(input_id)
        if input_id=="":
            QMessageBox.warning(self, 'ID 입력 오류', 'ID를 입력해주세요.')
        else:
            self.stackedWidget.setCurrentIndex(1)

    def move_prev(self):
        self.stackedWidget.setCurrentIndex(0)
        self.le_input_ID.clear()
        self.le_input_PW.clear()


    def move_join(self):
        self.stackedWidget.setCurrentIndex(2)
    def change_id(self):
        self.use_id = False
        self.btn_check_id.setEnabled(True)

    def check_id(self):
        self.id = self.le_input_id.text()
        self.serviceable = False
        self.use_id = False

        if len(self.id) < 3:
            self.le_input_id.clear()
            QMessageBox.information(self, "ID", "ID가 너무 짧습니다.\n3자 이상으로 입력해주세요")
        else:
            self.conn = pymysql.connect(host='localhost', port=3306, user='root', password='00000000', db='roll_book', charset='utf8')
            self.cursor = self.conn.cursor()
            self.cursor.execute(f"select 번호,ID,비밀번호,이름,구분 from data_ai")
            self.a = self.cursor.fetchall()
            self.data=[]
            for line in self.a:
                self.data.append(line)
            self.conn.close()
            for line in self.data:
                if self.id == line[1]:
                    self.use_id=False
                    self.serviceable=True
                    break
            if self.serviceable == False:
                    self.use_id=True
                    QMessageBox.information(self, 'ID', '사용가능한 ID 입니다.')
                    self.btn_check_id.setEnabled(False)
            else:
                QMessageBox.critical(self, "ID", "이미 사용중인 ID 입니다.")

    def check_sign_up(self):
        self.conn = pymysql.connect(host='localhost', port=3306, user='root', password='00000000', db='roll_book',
                                    charset='utf8')
        self.cursor = self.conn.cursor()
        self.cursor.execute(f"select ID,비밀번호,이름,구분 from data_ai;")
        self.user_data=self.cursor.fetchall()

        self.id = self.le_input_id.text()
        self.pw = self.le_input_pw.text()
        self.chk_pw = self.le_check_pw.text()
        self.name = self.le_input_name.text()
        self.phonenum = self.le_phonenum.text()
        self.join=[self.id, self.pw, self.chk_pw, self.name, self.phonenum]
        self.what_NULL=['ID','PW','이름','휴대폰번호']
        self.le_NULL=False
        print(self.join)
        unconfirmed=True
        for line_edit in self.join:
            if line_edit =="":
                self.le_NULL=True
                self.NULL_index = self.join.index(line_edit)
                QMessageBox.information(self, "NULL", f"{self.what_NULL[self.NULL_index]}를 입력해주세요.")
                break
        for line in self.user_data:
            print(line)
            if line[2]==self.name:
                unconfirmed = False
        if unconfirmed:
            QMessageBox.information(self, "가입불가", "등록되지 않은 사용자입니다.")
            self.le_input_name.clear()
            return
        if not self.le_NULL:
            if self.use_id:
                if self.join[1] == self.join[2]:
                    self.cursor.execute(f"update data_ai set ID='{self.id}', 비밀번호='{self.pw}' where 이름='{self.name}'")
                    complete = QMessageBox.information(self, "ID", "회원가입이 완료되었습니다.", QMessageBox.Ok)
                    self.conn.commit()
                    self.close()
                    if complete == QMessageBox.Ok:
                        print('클로즈')

                else:
                    self.not_password()
                    self.le_input_pw.clear()
                    self.le_check_pw.clear()
                    self.conn.close()
            else:
                self.conn.close()
                QMessageBox.critical(self, "ID", "이미 사용중인 ID 입니다.")
        else:
            self.conn.close()

    def check_overlap_Id(self):
        QMessageBox.information(self, 'ID', 'ID 중복확인을 해주세요..')


    def move_login(self):
        self.le_input_id.clear()
        self.le_input_pw.clear()
        self.le_check_pw.clear()
        self.le_input_name.clear()
        self.le_phonenum.clear()
        self.stackedWidget.setCurrentIndex(0)

contents_form_class = uic.loadUiType("si_contents.ui")[0]

class Contents(QWidget, contents_form_class):
    def __init__(self):
        super().__init__()
        # ui 불러오기, 객체 생성
        self.setupUi(self)
        self.stw_contents.setCurrentIndex(0)
        self.btn_show_nenu.clicked.connect(self.show_menu)
        self.btn_hide_menu.clicked.connect(self.hide_menu)
        self.tw_menu.itemClicked.connect(self.show_contents)
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
        else:
            a = item.parent()
            if a:
                menu = a.text(column)
                if menu == "학습":
                    print('학습')
                    self.stw_contents.setCurrentIndex(1)
                    self.learning(item,column)
                elif menu == "문제풀이":
                    self.stw_contents.setCurrentIndex(2)
                    self.problem_solving(item,column)
                    print('문제풀이')


    def learning(self, item, column):
        learning_name = item.text(column)
        print(learning_name)
        self.lb_learning_name.setText(f"{learning_name} 학습자료")
    def problem_solving(self, item, column):
        print('함수들어옴')
        question_name = item.text(column)
        print(question_name)
        self.lb_question_name.setText(f"{question_name} 문제풀이")




if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = QtWidgets.QStackedWidget()
    # 클래스의 객체 만들기
    login = Login()
    contents = Contents()
    login.setFixedWidth(667)
    login.setFixedHeight(800)
    # 프로그램 화면을 보여주는 코드
    login.show()
    app.exec_()