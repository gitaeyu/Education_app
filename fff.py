# from PyQt5.QtWidgets import QApplication, QMainWindow, QTreeWidget, QTreeWidgetItem, QVBoxLayout, QWidget,Q
#
# app = QApplication([])
# window = QMainWindow()
#
# # Create the central widget and layout
# central_widget = QWidget(window)
# layout = QVBoxLayout(central_widget)
#
# # Create the QTreeWidget
# tree = QTreeWidget(central_widget)
#
# # Adding some top-level items to the tree
# for i in range(3):
#     top_item = QTreeWidgetItem(tree)
#     top_item.setText(0, f"Top Level Item {i}")
#
#     # Adding some child items to each top-level item
#     for j in range(3):
#         child_item = QTreeWidgetItem(top_item)
#         child_item.setText(0, f"Child Item {j}")
#         top_item.addChild(child_item)
#
#
# def on_item_clicked(item, column):
#     top_item = item.parent()
#     if top_item:
#         print(f"Top-level item text: {top_item.text(0)}")
#
#
# tree.itemClicked.connect(on_item_clicked)
#
# # Add the QTreeWidget to the layout
# layout.addWidget(tree)
#
# # Set the central widget and show the window
# window.setCentralWidget(central_widget)
# window.show()
#
# app.exec_()
import pymysql
# class Login(QWidget, login_form_class):
#     def __init__(self):
#         super().__init__()
#         # ui 불러오기, 객체 생성
#         self.setupUi(self)
#         self.login_stack.setCurrentIndex(0)
#         # ----------------------------------------------------------
#         # 페이지 이동
#         self.btn_next.clicked.connect(self.move_next)
#         self.btn_prev.clicked.connect(self.move_prev)
#         # ----------------------------------------------------------
#         # ID 입력
#         self.le_input_ID.returnPressed.connect(self.move_next)
#         # ----------------------------------------------------------
#         self.btn_join.clicked.connect(self.move_join)
#         self.btn_join2.clicked.connect(self.move_join)
#         self.le_input_PW.returnPressed.connect(self.move_main)
#         self.btn_move_main.clicked.connect(self.move_main)
#         # 회원가입
#         self.btn_check_id.clicked.connect(self.check_id)
#         self.le_input_id.returnPressed.connect(self.check_id)
#         self.le_input_id.textChanged.connect(self.change_id)
#         self.btn_join_finish.clicked.connect(self.check_sign_up)
#         self.btn_cancle.clicked.connect(self.move_login)
#
#     def move_main(self):
#         id = self.le_show_ID.text()
#         pw = self.le_input_PW.text()
#         # conn = pymysql.connect(host='10.10.21.103', port=3306, user='root', password='00000000', db='education_app',
#         #                        charset='utf8')
#         conn = pymysql.connect(host='localhost', port=3306, user='root', password='00000000', db='education_app',
#                                charset='utf8')
#         cursor = conn.cursor()
#         cursor.execute(f"select * from memberinfo where ID='{id}' and Password='{pw}'")
#         self.login_user = cursor.fetchone()
#         if self.login_user == None:
#             QMessageBox.information(self, "로그인", "잘못 입력했습니다.\n다시 입력해주세요.")
#         else:
#
#             content = Contents(self)
#             content.show()
#             self.close()
#
#     def move_next(self):
#         input_id = self.le_input_ID.text()
#         self.le_show_ID.setText(input_id)
#         if input_id=="":
#             QMessageBox.warning(self, 'ID 입력 오류', 'ID를 입력해주세요.')
#         else:
#             self.login_stack.setCurrentIndex(1)
#
#     def move_prev(self):
#         self.login_stack.setCurrentIndex(0)
#         self.le_input_ID.clear()
#         self.le_input_PW.clear()
#     def move_join(self):
#         self.login_stack.setCurrentIndex(2)
#     def change_id(self):
#         self.use_id = False
#         self.btn_check_id.setEnabled(True)
#
#     def check_id(self):
#         id = self.le_input_id.text()
#         self.serviceable = False
#         self.use_id = False
#         if len(id) < 3:
#             self.le_input_id.clear()
#             QMessageBox.information(self, "ID", "ID가 너무 짧습니다.\n3자 이상으로 입력해주세요")
#         else:
#             # conn = pymysql.connect(host='10.10.21.103', port=3306, user='root', password='00000000', db='education_app',
#             #                        charset='utf8')
#             conn = pymysql.connect(host='localhost', port=3306, user='root', password='00000000', db='education_app', charset='utf8')
#             cursor = conn.cursor()
#             cursor.execute(f"select ID from memberinfo where ID='{id}'")
#             a = cursor.fetchone()
#             print(a)
#             conn.close()
#             if a == None:
#                 self.use_id = True
#                 QMessageBox.information(self, 'ID', '사용가능한 ID 입니다.')
#                 self.btn_check_id.setEnabled(False)
#             else:
#                 QMessageBox.critical(self, "ID", "이미 사용중인 ID 입니다.")
#     def check_sign_up(self):
#         # conn = pymysql.connect(host='10.10.21.103', port=3306, user='root', password='00000000', db='education_app',
#         #                        charset='utf8')
#         conn = pymysql.connect(host='localhost', port=3306, user='root', password='00000000', db='education_app',
#                                charset='utf8')
#         cursor = conn.cursor()
#         id = self.le_input_id.text()
#         pw = self.le_input_pw.text()
#         chk_pw = self.le_check_pw.text()
#         name = self.le_input_name.text()
#         phonenum = self.le_phonenum.text()
#         self.join=[id, pw, chk_pw, name, phonenum]
#         what_NULL=['ID','PW','이름','휴대폰번호']
#         print(self.join)
#         for line_edit in self.join:
#             if line_edit =="":
#                 NULL_index = self.join.index(line_edit)
#                 QMessageBox.information(self, "NULL", f"{what_NULL[NULL_index]}를 입력해주세요.")
#                 return
#         if self.use_id:
#             if self.join[1] == self.join[2]:
#                 cursor.execute(f"insert into memberinfo (ID,Password,User_Name,Division) values('{self.join[0]}','{self.join[1]}','{self.join[3]}','학생')")
#                 conn.commit()
#                 conn.close()
#                 QMessageBox.information(self, "ID", "회원가입이 완료되었습니다.", QMessageBox.Ok)
#                 self.login_stack.setCurrentIndex(0)
#                 self.sign_up_clear()
#         else: QMessageBox.information(self, 'ID', 'ID 중복확인을 해주세요.')
#
#     def sign_up_clear(self):
#         self.le_input_id.clear()
#         self.le_input_pw.clear()
#         self.le_check_pw.clear()
#         self.le_input_name.clear()
#         self.le_phonenum.clear()
#
#
#
#     def move_login(self):
#         self.le_input_id.clear()
#         self.le_input_pw.clear()
#         self.le_check_pw.clear()
#         self.le_input_name.clear()
#         self.le_phonenum.clear()
#         self.login_stack.setCurrentIndex(0)


conn = pymysql.connect(host='10.10.21.103', port=3306, user='root', password='00000000', db='education_app',
                       charset='utf8')
# conn = pymysql.connect(host='localhost', port=3306, user='root', password='00000000', db='education_app',
#                        charset='utf8')
cursor = conn.cursor()
cursor.execute(f"select * from memberinfo where ID='ksi' and Password='1234'")
login_user = cursor.fetchone()
print(login_user)
conn.close()
