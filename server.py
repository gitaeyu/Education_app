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

    def requests_online_teacher_list(self,socket):
        self.parent.idlist

class TeacherClass:
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

    def testentry(self):
        con = pymysql.connect(host='10.10.21.103', user='root', password='00000000',
                              db='education_app', charset='utf8')
        with con:
            with con.cursor() as cur:
                sql = f"INSERT INTO test (Test_contents,Test_img_URL,Test_correct_answer,Test_subject) values\
                ('{self.parent.signal[1]}','{self.parent.signal[2]}',\
                '{self.parent.signal[3]}','{self.parent.signal[4]}')"
                cur.execute(sql)
                con.commit()

    def request_db_name_list(self,socket):
        # signal = ["DB검색요청", 종류, 검색어]
        print(self.parent.signal)
        con = pymysql.connect(host='10.10.21.103', user='root', password='00000000',
                              db='education_app', charset='utf8')
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
    def new_login_user(self,socket): #signal = ['로그인',ID, 이름, 학생/교사]
        result = self.login_check()
        if result == "성공":
            if socket not in self.clients:
                self.clients.append(socket)
                print(self.clients)
            temp= [self.signal[1],self.signal[2],self.signal[3]]
            self.idlist.append(temp)
            for i in self.idlist:
                print(i)
                if i[3] =='학생':
                    self.student_list.append(i)
                else:
                    self.teacher_list.append(i)
            temp_msg = ['로그인', self.student_list, self.teacher_list]
            self.send_message = json.dumps(temp_msg)
            self.send_all_client()
            login_info = ['로그인 완료'] # 1, 'ksi', '1234', '김성일', 0, '4', '학생'
            for x in self.login_user :
                login_info.append(x)
            #login_info = ['로그인 완료', 1, 'ksi', '1234', '김성일', 0, '4', '학생']
            message = json.dumps(login_info)
            socket.send(message.encode())
        elif result == "실패" :
            information = ["로그인 실패"]
            message = json.dumps(information)
            socket.send(message.encode())

    def login_check(self):
        id = self.signal[1]
        pw = self.signal[2]
        conn = pymysql.connect(host='10.10.21.103', port=3306, user='root', password='00000000', db='education_app',
                               charset='utf8')
        # conn = pymysql.connect(host='localhost', port=3306, user='root', password='00000000', db='education_app',
        #                        charset='utf8')
        cursor = conn.cursor()
        cursor.execute(f"select * from memberinfo where ID='{id}' and Password='{pw}'")
        self.login_user = cursor.fetchone()
        print(self.login_user) # (1, 'ksi', '1234', '김성일', 0, '4', '학생')
        if self.login_user == None:
            return "실패"
        else:
            return "성공"
    def login_id_duplicate_check(self,socket):
        id = self.signal[1]
        conn = pymysql.connect(host='10.10.21.103', port=3306, user='root', password='00000000', db='education_app',
                               charset='utf8')
        # conn = pymysql.connect(host='localhost', port=3306, user='root', password='00000000', db='education_app', charset='utf8')
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
    def sign_up(self,socket):
        # signal = ["회원가입", id,pw,name,'선생']
        conn = pymysql.connect(host='10.10.21.103', port=3306, user='root', password='00000000', db='education_app',
                               charset='utf8')
        # conn = pymysql.connect(host='localhost', port=3306, user='root', password='00000000', db='education_app', charset='utf8')
        cursor = conn.cursor()
        cursor.execute(f"insert into memberinfo (ID,Password,User_Name,Division) \
                        values('{self.signal[1]}','{self.signal[2]}','{self.signal[3]}','{self.signal[4]}')")
        conn.commit()
        conn.close()
        #희희
        information = ["가입 완료"]
        message = json.dumps(information)
        socket.send(message.encode())
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
                break
            else:#['로그인',self.login_user[1],self.login_user[3],self.login_user[-1]]
                if self.signal[0] =="로그인":  # signal = ["로그인", ID, PW]
                    self.new_login_user(socket)
                elif self.signal[0] =="ID중복확인":  # signal = ["ID중복확인", ID]
                    self.login_id_duplicate_check(socket)
                elif self.signal[0] =="회원가입":  # signal = ["회원가입", id,pw,chk_pw,name]
                    self.sign_up(socket)
                elif self.signal[0] == "TC문제등록":  # signal = ["문제등록", 문제내용,img_URL,test_correct_answer,종류]
                    self.teacher.testentry()
                elif self.signal[0] == "TCDB검색요청":  # signal = ["DB검색요청", 종류, 검색어]
                    self.teacher.request_db_name_list(socket)
                elif self.signal[0] == "TCDB설명요청":  # signal = ["DB설명요청", 종류, 검색어]
                    self.teacher.request_db_description(socket)
                elif self.signal[0] == "SC온라인교사목록":  # signal = ["SC온라인교사목록", 요청자이름]
                    self.student.requests_online_teacher_list(socket)


    # self.clients에 더 이상 ip와 port 저장하지않아서 ip,port 빼버림 (02.07 10:40)
    def send_all_client(self):
        for client in self.clients:  # 목록에 있는 모든 소켓에 대해
            print(self.clients)
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
                self.idlist.remove(self.idlist[i])
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
