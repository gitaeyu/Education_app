import socketserver
import pymysql
import time
import json

host_str = '10.10.21.112'
user_str = 'root3'
password_str = '123456789'


class MyTCPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        (ip, port) = self.client_address
        client = self.request, (ip, port)
        if client not in Multi_server.clients:
            Multi_server.clients.append(client)
        print(ip, ":", str(port), '가 연결되었습니다.')
        Multi_server.receive_messages(self.request)


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


class StudentClass:
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

    def test(self):
        print('test')


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
        self.signal = ''
        self.final_received_message = ""  # 최종 수신 메시지
        self.student = StudentClass(self)
        self.teacher = TeacherClass(self)

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
                self.remove_socket(socket)
                break
            except ConnectionResetError as e:
                print(e)
                break
            else:
                if self.signal[0] == "문제등록":  # signal = ["문제등록", 문제내용,img_URL,test_correct_answer,종류]
                    self.teacher.testentry()
                elif self.signal[0] == "DB검색요청":  # signal = ["DB검색요청", 종류, 검색어]
                    self.teacher.request_db_name_list(socket)
                elif self.signal[0] == "DB설명요청":  # signal = ["DB설명요청", 종류, 검색어]
                    self.teacher.request_db_description(socket)

    def send_all_client(self):
        """
        모든 클라이언트에게 끝말잇기 채팅 정보를 전달함.
        """
        for client in self.clients:  # 목록에 있는 모든 소켓에 대해
            print(client, "고객")
            socket, (ip, port) = client
            try:
                socket.sendall(self.final_received_message.encode())
            except Exception as e:  # 연결종료
                print(e)
                self.clients.remove(client)  # 소켓 제거
                print(f"{ip},{port} 연결이 종료 되었습니다.")

    def remove_socket(self, c_socket):
        """
        나갔을때 연결이 끊기기 전 self.clients에서
        client를 제거해주면서 소켓 정보와 id 정보를 없애준다.
        또한 idlist가 갱신됬으므로 이 정보를 다시 클라이언트로 보내준다.
        """
        i = 0
        for client in self.clients:  # 목록에 있는 모든 소켓에 대해
            print(client, "고객")
            socket, (ip, port) = client
            if socket == c_socket:
                print("소켓을 제거합니다")
                self.clients.remove(client)  # 소켓 제거
                self.idlist.remove(self.idlist[i])
                print(f"IP:{ip},Port:{port} 연결이 종료 되었습니다.")
                tempdata = json.dumps(self.idlist)
                senddata = tempdata + "985674"
                self.final_received_message = senddata
                self.send_all_client()
                break
            i += 1


if __name__ == "__main__":
    Multi_server = MultiChatServer()
    HOST, PORT = "127.0.0.1", 9048
    with ThreadedTCPServer((HOST, PORT), MyTCPHandler) as server:
        server.serve_forever()
