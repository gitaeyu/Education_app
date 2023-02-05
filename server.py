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


class MultiChatServer:

    # 소켓을 생성하고 연결되면 accept_client() 호출

    def __init__(self):
        self.idlist = []
        self.clients = []
        self.final_received_message = ""  # 최종 수신 메시지

    # 데이터를 수신하여 모든 클라이언트에게 전송한다.
    def receive_messages(self, socket):
        """
        서버 수신 스레드
        수신한 메세지의 식별 코드에 따라 메서드로 이동하거나 다시 반환해준다.
        """
        while True:
            try:
                incoming_message = socket.recv(1024)
                self.recv_signal = incoming_message
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

                if self.final_received_message[-3:] in ('000', '010', '011'):  # 채팅창 불러오기 code
                    self.send_all_clients(socket)


    def send_all_clients(self, senders_socket):
        """
        모든 클라이언트에게 끝말잇기 채팅 정보를 전달함.
        """
        for client in self.clients:  # 목록에 있는 모든 소켓에 대해
            print(client, "고객")
            socket, (ip, port) = client
            try:
                socket.sendall(self.final_received_message_gt.encode())
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
                try:
                    tempdata = json.dumps(self.idlist)
                    senddata = tempdata + "985674"
                except:
                    print("리시브 메시지 오류발생")
                else:
                    self.final_received_message_gt \
                        = senddata
                    self.fu_send_all_client(c_socket)
                break
            i += 1


if __name__ == "__main__":
    Multi_server = MultiChatServer()
    HOST, PORT = "127.0.0.1", 9048
    with ThreadedTCPServer((HOST, PORT), MyTCPHandler) as server:
        server.serve_forever()
