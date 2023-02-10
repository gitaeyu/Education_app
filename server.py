import socketserver
import pymysql
import time
import json



class MyTCPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        (ip, port) = self.client_address
        print(ip, ":", str(port), '가 연결되었습니다.')
        Multi_server.receive_messages(self.request)



class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


class StudentClass:
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

    def request_learning_completed(self):  # signal = ['학습완료', IDnum, contents, IDnum+contents]
        print('학습완료 메서드 진입')
        insert_db_contents = self.parent.signal[1::]
        print(insert_db_contents)
        con = pymysql.connect(host='10.10.21.103', user='root', password='00000000',
                              db='education_app', charset='utf8')
        with con:
            with con.cursor() as cur:
                sql = f"INSERT IGNORE INTO 학습진도 VALUES ('{insert_db_contents[0]}','{insert_db_contents[1]}','{insert_db_contents[2]}');"
                cur.execute(sql)
                con.commit()
    def request_test_result(self):  # signal = ['SCDB시험 결과', ID_Num,[[시험결과]]]
        print('DB 테스트 결과 메서스진입')
        test_ID_num = self.parent.signal[1]
        test_result = self.parent.signal[2::]
        print(test_result)
        point = 0
        con = pymysql.connect(host='10.10.21.103', user='root', password='00000000',
                              db='education_app', charset='utf8')
        with con:
            with con.cursor() as cur:
                for i in test_result:
                    point += i.count('correct')*30
                    sql = f"INSERT INTO member_test VALUES('{test_ID_num}','{i[0]}','{i[1]}','{i[2]}')"
                    cur.execute(sql)
                sql = f"UPDATE Memberinfo SET Point=Point+{point} WHERE IDnum='{test_ID_num}'"
                cur.execute(sql)
                con.commit()
        print('DB에 넣음')
    def request_DB_QNA(self, socket):
        print('DB_QNA 메서드진입')
        con = pymysql.connect(host='10.10.21.103', user='root', password='00000000',
                              db='education_app', charset='utf8')
        # con = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='00000000', db='education_app',
        #                       charset='utf8')
        if self.parent.signal[3] == '학생':
            sql = f"SELECT * FROM `q&a` WHERE User_Name='{self.parent.signal[2]}'"
        else:
            sql = f"SELECT * FROM `q&a` "
        with con:
            with con.cursor() as cur:
                cur.execute(sql)
                db_temp = cur.fetchall()
                temp = ['SC Q&A DB반환']
                for i in db_temp:
                    temp.append(i)
                request_db_msg = json.dumps(temp)
                socket.sendall(request_db_msg.encode())
                print('Q&A DB 전송완료')

    def request_add_QNA(self,socket):  #question = [이름,날짜,문의제목,문의내용]
        question= self.parent.signal[1::]
        # con = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='00000000', db='education_app',
        #                       charset='utf8')
        con = pymysql.connect(host='10.10.21.103', port=3306, user='root', password='00000000', db='education_app',
                              charset='utf8')
        with con:
            with con.cursor() as cur:
                sql = f"INSERT INTO `q&a` (User_Name,Date,Question,Question_contents) VALUES('{question[0]}','{question[1]}','{question[2]}','{question[3]}')"
                cur.execute(sql)
                con.commit()
                sql = f"SELECT * FROM `q&a` WHERE User_Name='{question[0]}'"
                cur.execute(sql)
                db_temp = cur.fetchall()
                temp = ['SC Q&A DB반환']
                for i in db_temp:
                    temp.append(i)
                request_db_msg = json.dumps(temp)
                socket.sendall(request_db_msg.encode())
                print('Q&A DB 전송완료')
    def request_test(self,socket):  #signal = ['SCDB요청 문제', ID_Num, Test_subject]
        ID_Num = self.parent.signal[1]
        test_subject = self.parent.signal[2]

        con = pymysql.connect(host='10.10.21.103', user='root', password='00000000',
                              db='education_app', charset='utf8')
        # con = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='00000000', db='education_app',
        #                        charset='utf8')
        with con:
            with con.cursor() as cur:
                sql= f"SELECT * FROM test where  Test_subject like '%{test_subject}%' order by rand() limit 5;"
                cur.execute(sql)
                test_temp = cur.fetchall()
                temp = ['SCDB요청 반환']
                for i in test_temp:
                    temp.append(i)
                request_db_msg = json.dumps(temp)
                socket.sendall(request_db_msg.encode())# ['SCDB요청 반환',[Test_num, Test_contents, Test_img_URL, Test_correct_answer, Test_subject, Test_contents_name]



class TeacherClass:
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

    def reqeuest_student_test_result(self,socket):
        con = pymysql.connect(host='10.10.21.103', user='root', password='00000000',
                              db='education_app', charset='utf8')
        with con:
            with con.cursor() as cur:
                Total_test_question_num = cur.execute(f"SELECT * FROM member_test as a inner join test as b  \
                on a.Test_num = b.Test_num where ID_Num = {self.parent.signal[1]}")
                correct_test_question_num = cur.execute(f"SELECT * FROM member_test as a inner join test as b  \
                on a.Test_num = b.Test_num where ID_Num = {self.parent.signal[1]} and Test_result = 'correct'")
                insect_correct_question_num = cur.execute(f"SELECT * FROM member_test as a inner join test as b  \
                on a.Test_num = b.Test_num where ID_Num = {self.parent.signal[1]} and \
                Test_result = 'correct' and Test_subject = '곤충'")
                insect_question_num = cur.execute(f"SELECT * FROM member_test as a inner join test as b  \
                on a.Test_num = b.Test_num where ID_Num = {self.parent.signal[1]} and \
                Test_subject = '곤충'")
                mammal_correct_question_num = cur.execute(f"SELECT * FROM member_test as a inner join test as b  \
                on a.Test_num = b.Test_num where ID_Num = {self.parent.signal[1]} and \
                Test_result = 'correct' and Test_subject = '포유류'")
                mammal_question_num = cur.execute(f"SELECT * FROM member_test as a inner join test as b  \
                on a.Test_num = b.Test_num where ID_Num = {self.parent.signal[1]} and \
                Test_subject = '포유류'")
                bird_correct_question_num = cur.execute(f"SELECT * FROM member_test as a inner join test as b  \
                on a.Test_num = b.Test_num where ID_Num = {self.parent.signal[1]} and \
                Test_result = 'correct' and Test_subject = '조류'")
                bird_question_num = cur.execute(f"SELECT * FROM member_test as a inner join test as b  \
                on a.Test_num = b.Test_num where ID_Num = {self.parent.signal[1]} and \
                Test_subject = '조류'")
                information = ["학생성적반환", correct_test_question_num, Total_test_question_num,
                               insect_correct_question_num,
                               insect_question_num, mammal_correct_question_num, mammal_question_num,
                               bird_correct_question_num, bird_question_num]
                message = json.dumps(information)
                socket.sendall(message.encode())
    def request_student_DB(self,socket):
        con = pymysql.connect(host='10.10.21.103', user='root', password='00000000',
                              db='education_app', charset='utf8')
        sql = f"SELECT * FROM `memberinfo` WHERE division='학생'"
        with con:
            with con.cursor() as cur:
                cur.execute(sql)
                db_temp = cur.fetchall()
                temp=['학생DB반환']
                for i in db_temp:
                    temp.append(i)
                request_db_msg = json.dumps(temp)
                socket.sendall(request_db_msg.encode())
                print('학생DB 전송완료')
    def entry_answer(self):
        print("답변등록")
        # self.parent.signal = ["답변등록" ,문제번호 ,답변,답변자]
        con = pymysql.connect(host='10.10.21.103', user='root', password='00000000',
                              db='education_app', charset='utf8')
        with con:
            with con.cursor() as cur:
                sql = f"update `q&a` set Answer = '{self.parent.signal[2]}', Answer_user = '{self.parent.signal[3]}'\
                        where Num = {int(self.parent.signal[1])} "
                cur.execute(sql)
                con.commit()
        print("답변등록 완료")

    def testentry(self):
        con = pymysql.connect(host='10.10.21.103', user='root', password='00000000',
                              db='education_app', charset='utf8')
        # con = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='00000000', db='education_app',
        #                        charset='utf8')
        with con:
            with con.cursor() as cur:
                sql = f"INSERT INTO test (Test_contents,Test_img_URL,Test_correct_answer,Test_subject,\
                Test_contents_name) values ('{self.parent.signal[1]}','{self.parent.signal[2]}',\
                '{self.parent.signal[3]}','{self.parent.signal[4]}','{self.parent.signal[5]}')"
                cur.execute(sql)
                con.commit()

    def request_db_name_list(self,socket):
        # signal = ["DB검색요청", 종류, 검색어]
        print(self.parent.signal)
        # con = pymysql.connect(host='10.10.21.103', user='root', password='00000000',
        #                       db='education_app', charset='utf8')
        con = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='00000000', db='education_app',
                               charset='utf8')
        with con:
            with con.cursor() as cur:
                sql = f"SELECT 이름 from 학습자료 where 분류 = '{self.parent.signal[1]}' \
                and 이름 like '%{self.parent.signal[2]}%'"
                print(sql)
                cur.execute(sql)
                name_list = cur.fetchall()
                print(name_list)
                information = ["DB검색반환"]
                for x in name_list:
                    information.append(x[0])
                print(information)
                message = json.dumps(information)
                socket.sendall(message.encode())
                print("ㅎㅇ")
    def request_db_description(self,socket):
        # signal = ["DB설명요청", 종류, 검색어]
        print(self.parent.signal)
        con = pymysql.connect(host='10.10.21.103', user='root', password='00000000',
                              db='education_app', charset='utf8')
        # con = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='00000000', db='education_app',
        #                        charset='utf8')
        with con:
            with con.cursor() as cur:
                sql = f"SELECT 생태특징,일반특징,이미지 from 학습자료 where 분류 = '{self.parent.signal[1]}' \
                and 이름 = '{self.parent.signal[2]}'"
                print(sql)
                cur.execute(sql)
                info_list = cur.fetchall()
                print(info_list)
                information = ["DB설명반환"]
                information.append(info_list[0][0])
                information.append(info_list[0][1])
                information.append(info_list[0][2])
                print(information)
                message = json.dumps(information)
                socket.sendall(message.encode())

    def request_test_stat(self, socket):
        # signal = ["TC문제통계요청"]
        print(self.parent.signal)
        con = pymysql.connect(host='10.10.21.103', user='root', password='00000000',
                              db='education_app', charset='utf8')
        # con = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='00000000', db='education_app',
        #                        charset='utf8')
        with con:
            with con.cursor() as cur:
                sql = "select *,CAST(ROUND((f.correct/f.cnt),3) AS cHAR(30)) as rate from \
                (select a.test_num,count(case when test_result = 'correct' then 'correct' end) as correct, \
                count(*)as cnt, b.test_contents  from member_test as a left join test as b on a.test_num = B.test_num \
                group by a.test_num) as f order by rate  limit 5"
                cur.execute(sql)
                rate_list = cur.fetchall()
                print(rate_list)
                sql = "select a.test_num,round(avg(a.consume_time),2) as consume_time , b.test_contents \
                from member_test as a left join test as b on a.test_num = B.test_num  group by a.test_num \
                order by consume_time  desc limit 5;"
                cur.execute(sql)
                time_list = cur.fetchall()
                print(time_list)
                information = ["TC문제통계반환",rate_list,time_list]
                message = json.dumps(information)
                socket.sendall(message.encode())


class MultiChatServer:

    # 소켓을 생성하고 연결되면 accept_client() 호출

    def __init__(self):
        self.idlist = []
        self.clients = []
        self.student_list=[]
        self.teacher_list = []
        self.signal = ''
        self.send_message = ""  # 최종 수신 메시지
        self.student = StudentClass(self)
        self.teacher = TeacherClass(self)


    def user_logout(self): # signal = ["로그아웃", ID, 이름, 학생/교사]
        logout_user = self.signal[1::]
        if logout_user[-1] == '학생':
            self.student_list.remove(logout_user)
        else:
            self.teacher_list.remove(logout_user)
        self.idlist.remove(logout_user)
        temp_msg = ['로그아웃', self.student_list, self.teacher_list]
        self.send_message = json.dumps(temp_msg)
        self.send_all_client()
    def new_login_user(self, socket):  # signal = ['로그인',ID, pw, 학생/교사]
        result = self.login_check()
        if result == "성공":
            if socket not in self.clients:
                self.clients.append(socket)
                print(self.clients)
            temp = [self.login_user[1],self.login_user[3],self.login_user[-1]]
            print(temp)
            if temp not in self.idlist:
                self.idlist.append(temp)
            self.student_list=[]
            self.teacher_list=[]
            for i in self.idlist:
                print(i)
                if i[2] == '학생' and i not in self.student_list:
                    self.student_list.append(i)
                elif i[2] == '선생' and i not in self.teacher_list:
                    self.teacher_list.append(i)
            temp_msg = ['로그인', self.student_list, self.teacher_list]
            print(temp_msg)
            self.send_message = json.dumps(temp_msg)
            self.send_all_client()
            time.sleep(0.2)
            login_info = ['로그인 완료'] # login_info = ['로그인 완료', 1, 'ksi', '1234', '김성일', 0, '4', '학생']
            for x in self.login_user:
                login_info.append(x)
            if self.login_user[6]=='학생': # login_info = ['로그인 완료', 1, 'ksi', '1234', '김성일', 0, '4', '학생', [문제, 학습진도]]
                login_info.append(self.label_update)
            message = json.dumps(login_info)
            socket.send(message.encode())
        elif result == "실패":
            information = ["로그인 실패"]
            message = json.dumps(information)
            socket.send(message.encode())

    def login_check(self):# signal = ["로그인", ID, pw, 학생/교사]
        id = self.signal[1]
        pw = self.signal[2]
        div = self.signal[3]
        conn = pymysql.connect(host='10.10.21.103', user='root', password='00000000',
                              db='education_app', charset='utf8')
        # conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='00000000', db='education_app',
        #                        charset='utf8')
        cursor = conn.cursor()
        cursor.execute(f"select * from memberinfo where ID='{id}' and Password='{pw}' and Division = '{div}'")
        self.login_user = cursor.fetchone()
        print(self.login_user)  # (1, 'ksi', '1234', '김성일', 0, '4', '학생')
        if div == '학생':
            count_test = cursor.execute(f"SELECT * FROM member_test where ID_Num='{self.login_user[0]}';")
            learning_num = cursor.execute(f"SELECT * FROM 학습진도 where IDnum='{self.login_user[0]}';")
            self.label_update = [count_test,learning_num]
        if self.login_user == None:
            return "실패"
        else:
            return "성공"
    def login_id_duplicate_check(self, socket):
        id = self.signal[1]
        conn = pymysql.connect(host='10.10.21.103', user='root', password='00000000',
                              db='education_app', charset='utf8')
        # conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='00000000', db='education_app',
        #                        charset='utf8')
        cursor = conn.cursor()
        cursor.execute(f"select ID from memberinfo where ID='{id}'")
        a = cursor.fetchone()
        conn.close()
        if a == None:
            information = ["중복 없음"]
            message = json.dumps(information)
            socket.send(message.encode())
        else:
            information = ["ID 중복"]
            message = json.dumps(information)
            socket.send(message.encode())

    def sign_up(self, socket):
        # signal = ["회원가입", id,pw,name,'선생']
        conn = pymysql.connect(host='10.10.21.103', user='root', password='00000000',
                              db='education_app', charset='utf8')
        # conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='00000000', db='education_app',
        #                        charset='utf8')
        cursor = conn.cursor()
        cursor.execute(f"insert into memberinfo (ID,Password,User_Name,Division) \
                        values('{self.signal[1]}','{self.signal[2]}','{self.signal[3]}','{self.signal[4]}')")
        conn.commit()
        conn.close()
        # 희희
        information = ["가입 완료"]
        message = json.dumps(information)
        socket.send(message.encode())

    def real_time_chat(self):  # signal = ["실시간채팅",보낸사람,받는사람,메세지,시간]
        chat_msg = json.dumps(self.signal)
        count = 0
        i=0
        for id in self.idlist:  # 목록에 있는 모든 소켓에 대해
            if id[1] == self.signal[1] or id[1] == self.signal[2]:
                count+=1
                socket = self.clients[i]
                socket.sendall(chat_msg.encode())
            if count ==2 :
                break
            i += 1

    def invite_message(self): # signal =["채팅초대", 보낸사람, 받는사람]
        i = 0
        invite_msg = json.dumps(self.signal)
        for id in self.idlist:  # 목록에 있는 모든 소켓에 대해
            if id[1] == self.signal[2]:
                socket = self.clients[i]
                socket.sendall(invite_msg.encode())
            i += 1
    def invite_accept(self,socket): # signal = ['채팅수락', 수락메시지, 수락한 사람, 보낸 사람]

        i = 0
        invite_msg = json.dumps(self.signal)
        for id in self.idlist:  # 목록에 있는 모든 소켓에 대해
            if id[1] == self.signal[3]:
                r_socket = self.clients[i]
                r_socket.sendall(invite_msg.encode())
                socket.sendall(invite_msg.encode())
            i += 1
    def invite_already(self):  # signal= ['이미 채팅중', '000님은\n이미 상담중입니다.', 초대받은사람, 초대한사람]
        i = 0
        invite_already_msg = json.dumps(self.signal)
        for id in self.idlist:  # 목록에 있는 모든 소켓에 대해
            if id[1] == self.signal[3]:
                socket = self.clients[i]
                socket.sendall(invite_already_msg.encode())
            i += 1

    # 데이터를 수신하여 모든 클라이언트에게 전송한다.
    def receive_messages(self, socket):
        """
        서버 수신 스레드
        수신한 메세지의 식별 코드에 따라 메서드로 이동하거나 다시 반환해준다.
        """
        while True:
            try:
                incoming_message = socket.recv(8192)
                self.signal = json.loads(incoming_message.decode())
                print('self.signal: ',self.signal)
                if not incoming_message:  # 연결이 종료됨
                    break
            except ConnectionAbortedError as e:
                print(e)
                print('??')
                self.remove_socket(socket)
                break
            except ConnectionResetError as e:
                print(e)
                print('!!')
                self.remove_socket(socket)
                break
            else:
                if self.signal[0] =="로그인":  # signal = ["로그인", ID, pw, 학생/교사]
                    self.new_login_user(socket)
                elif self.signal[0] == "ID중복확인":  # signal = ["ID중복확인", ID]
                    self.login_id_duplicate_check(socket)
                elif self.signal[0] == "회원가입":  # signal = ["회원가입", id,pw,chk_pw,name]
                    self.sign_up(socket)
                elif self.signal[0] == "TC문제등록":  # signal = ["문제등록", 문제내용,img_URL,test_correct_answer,종류]
                    self.teacher.testentry()
                elif self.signal[0] == "TCDB검색요청":  # signal = ["DB검색요청", 종류, 검색어]
                    self.teacher.request_db_name_list(socket)
                elif self.signal[0] == "TCDB설명요청":  # signal = ["DB설명요청", 종류, 검색어]
                    self.teacher.request_db_description(socket)
                elif self.signal[0] == "SCDB요청 Q&A":  # signal = ['SCDB요청', ID, 이름, 학생]
                    self.student.request_DB_QNA(socket)
                elif self.signal[0] == "로그아웃":  # signal = ["로그아웃", ID, 이름, 학생/교사]
                    self.user_logout()
                elif self.signal[0] == "종료":   # signal = ["종료", ID, 이름, 학생/교사]
                    self.remove_socket(socket)
                elif self.signal[0] == "실시간채팅" :  # signal = ["실시간채팅",보낸사람,받는사람,메세지,시간]
                    print(self.signal)
                    self.real_time_chat()
                elif self.signal[0] == "TC답변등록" : # signal = ["TC답변등록 ,문제번호 ,답변,답변자]
                    self.teacher.entry_answer()
                elif self.signal[0] == "SCDB 문의추가": #signal = ['SCDB 문의추가',이름,날짜,문의제목,문의내용]
                    self.student.request_add_QNA(socket)
                elif self.signal[0] == "채팅초대": # signal =["채팅초대", 보낸사람, 받는사람]
                    self.invite_message()
                elif self.signal[0] == "채팅수락": # signal = ['채팅수락', 수락메시지, 수락한 사람, 보낸 사람]
                    self.invite_accept(socket)
                elif self.signal[0] == "이미 채팅중":  # signal= ['이미 채팅중', '000님은\n이미 상담중입니다.', 초대받은사람, 초대한사람]
                    self.invite_already()
                elif self.signal[0] == 'SCDB요청 문제':  #signal = ['SCDB요청 문제', ID_Num]
                    self.student.request_test(socket)
                elif self.signal[0] == "SCDB시험 결과": # signal = ['SCDB시험 결과', ID_Num,[[시험결과]]]
                    self.student.request_test_result()
                elif self.signal[0] == "TC학생DB요청":  # signal= [TC학생DB요청]
                    self.teacher.request_student_DB(socket)
                elif self.signal[0] == "TC시험결과요청":  # signal= ["TC시험결과요청",학생번호]
                    self.teacher.reqeuest_student_test_result(socket)
                elif self.signal[0] == "학습완료": # signal = ['학습완료', IDnum, contents, IDnum+contents]
                    self.student.request_learning_completed()
                elif self.signal[0] == "TC문제통계요청":  # signal= ["TC문제통계요청"]
                    self.teacher.request_test_stat(socket)
                elif self.signal[0] == "상담종료":  # signal = ["상담종료", 보낸사람, 받는사람]
                    self.consult_end()

    def consult_end(self):    # signal = ["상담종료", 보낸사람, 받는사람]
        chat_end_temp = [self.signal[0]]
        chat_end_msg = json.dumps(chat_end_temp)
        i = 0
        for id in self.idlist:  # 목록에 있는 모든 소켓에 대해
            if id[1] == self.signal[2]:
                socket = self.clients[i]
                socket.sendall(chat_end_msg.encode())
            i+=1

    def send_all_client(self):
        for client in self.clients:  # 목록에 있는 모든 소켓에 대해
            socket = client
            try:
                socket.sendall(self.send_message.encode())
                print('메시지 전송')
            except Exception as e:  # 연결종료
                print(e)
                self.clients.remove(client)  # 소켓 제거

    def remove_socket(self, c_socket):
        """
        나갔을때 연결이 끊기기 전 self.clients에서
        client를 제거해주면서 소켓 정보와 id 정보를 없애준다.
        또한 idlist가 갱신됐으므로 이 정보를 다시 클라이언트로 보내준다.
        """
        i = 0
        for client in self.clients:  # 목록에 있는 모든 소켓에 대해
            print(client, "고객")
            socket = client
            if socket == c_socket:
                print("소켓을 제거합니다")
                self.clients.remove(client)  # 소켓 제거
                try:
                    self.idlist.remove(self.idlist[i])
                except Exception as e :
                    print(c_socket)
                    print (e,"리무브 소켓 에러")
                    pass
                finally:
                    self.student_list = []
                    self.teacher_list = []
                    for i in self.idlist:
                        print(i)
                        if i[2] == '학생':
                            self.student_list.append(i)
                        else:
                            self.teacher_list.append(i)
                    temp_msg = ['로그인', self.student_list, self.teacher_list]
                    self.send_message = json.dumps(temp_msg)
                    self.send_all_client()
                    break
            i += 1


if __name__ == "__main__":
    Multi_server = MultiChatServer()
    HOST, PORT = "127.0.0.1", 9048
    with ThreadedTCPServer((HOST, PORT), MyTCPHandler) as server:
        server.serve_forever()
