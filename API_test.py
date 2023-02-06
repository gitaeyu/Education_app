# 모듈 import
import requests
import pprint
import pandas as pd
import bs4
import json
import requests
import xmltodict
import pymysql
from xml.etree import ElementTree
import lxml
# a= input("검색어를 입력해주세요")
# #인증키 입력
encoding = '11xBqPRCrKxDRnzolBiWVGwhexbmYELfieu%2BGvVw7z2HYGWD67SB2EGIMJHoG8KYEvkNOd3LaHsvIp7cDZPhzg%3D%3D'
decoding = '11xBqPRCrKxDRnzolBiWVGwhexbmYELfieu+GvVw7z2HYGWD67SB2EGIMJHoG8KYEvkNOd3LaHsvIp7cDZPhzg=='
# url = 'http://apis.data.go.kr/1400119/MammService/mammIlstrSearch'
# params ={'serviceKey' : decoding, 'st' : '1', 'sw' : a ,'numOfRows' : '10', 'pageNo' : '1' }
#
# response = requests.get(url, params=params)
# content = response.content                    # request 모듈을 이용해서 정보 가져오기(byte형태로 가져와지는듯)
# print(content)
# dict = xmltodict.parse(content)                         # xmltodict 모듈을 이용해서 딕셔너리화 & 한글화
# jsonString = json.dumps(dict, ensure_ascii=False)       # json.dumps를 이용해서 문자열화(데이터를 보낼때 이렇게 바꿔주면 될듯)
# jsonObj = json.loads(jsonString)                        # 데이터 불러올 때(딕셔너리 형태로 받아옴)
#
# for item in jsonObj['response']['body']['items']['item']:
#     print(item['anmlGnrlNm'], item['anmlSpecsId'])
#
# q1 = input("anmlSpecsId 를 입력해주세요")

# url = 'http://apis.data.go.kr/1400119/MammService/mammIlstrInfo'
# params ={'serviceKey' : decoding, 'q1' : q1 }

#
#
#
# url = 'http://down.edunet4u.net/KEDNCM/OPENAPI/WKSTCONT/nedu_wkst_cont_CLSS0000000362.xml'
# response = requests.get(url)
# print(response.content)
# # xml 내용
# content = response.text
#
# #bs4 사용하여 item 태그 분리
#
# xml_obj = bs4.BeautifulSoup(content,'lxml-xml')
# rows = xml_obj.findAll('row_small_data')
# # xml 안의 데이터 수집
# row_list = [] # 행값
# name_list = [] # 열이름값
# value_list = [] #데이터값
# for i in range(0, len(rows)):
#     columns = rows[i].find_all()
#     #첫째 행 데이터 수집
#     for j in range(0,len(columns)):
#         if i ==0 :
#             # 컬럼 이름 값 저장
#             name_list.append(columns[j].name)
#         if j == 3 or j ==4 : # 원하는 컬럼 데이터
#             # 컬럼의 각 데이터 값 저장
#             value_list.append(columns[j].text)
#         # 각 행의 value값 전체 저장
#             row_list.append(value_list)
#     # 데이터 리스트 값 초기화
#     value_list=[]
# print(name_list)
# pd.set_option('display.width', 1000)
# pd.set_option('display.max_rows', None)
# pd.set_option('display.max_columns', None)
# #xml값 DataFrame으로 만들기
# df = pd.DataFrame(row_list, columns=['tcp_atcl','url'])
# print(df.head(10))
# print(df.iloc[0]['eclgDpftrCont'])
# print("나이스")
# print(df.iloc[0]['gnrlSpftrCont'])
# print(df.iloc[0]['imgUrl'])

from bs4 import BeautifulSoup

# 인증키 저장
key = "11xBqPRCrKxDRnzolBiWVGwhexbmYELfieu%2BGvVw7z2HYGWD67SB2EGIMJHoG8KYEvkNOd3LaHsvIp7cDZPhzg%3D%3D"

# 인증키 정보가 들어간 url 저장
url = 'http://openapi.nature.go.kr/openapi/service/rest/InsectService/isctIlstrSearch'
params ={'serviceKey' : decoding, 'st' : '1', 'sw' : '', 'numOfRows' : '20', 'pageNo' : '1' }

response = requests.get(url, params=params)

content = response.content                     # request 모듈을 이용해서 정보 가져오기(byte형태로 가져와지는듯)
print(content)
dict = xmltodict.parse(content)                         # xmltodict 모듈을 이용해서 딕셔너리화 & 한글화
jsonString = json.dumps(dict, ensure_ascii=False)       # json.dumps를 이용해서 문자열화(데이터를 보낼때 이렇게 바꿔주면 될듯)
jsonObj = json.loads(jsonString)                        # 데이터 불러올 때(딕셔너리 형태로 받아옴)
animalID = []
for item in jsonObj['response']['body']['items']['item']:
    animalID.append(item['insctPilbkNo'])


for x in animalID :

    url = 'http://openapi.nature.go.kr/openapi/service/rest/InsectService/isctIlstrInfo'
    params ={'serviceKey' : decoding , 'q1' : x }


    response = requests.get(url, params=params)
    content = response.content  # request 모듈을 이용해서 정보 가져오기(byte형태로 가져와지는듯)
    dict = xmltodict.parse(content)  # xmltodict 모듈을 이용해서 딕셔너리화 & 한글화
    jsonString = json.dumps(dict, ensure_ascii=False)  # json.dumps를 이용해서 문자열화(데이터를 보낼때 이렇게 바꿔주면 될듯)
    jsonObj = json.loads(jsonString)  # 데이터 불러올 때(딕셔너리 형태로 받아옴)
    print(jsonObj['response']['body']['item']['cont1'])
    print(jsonObj['response']['body']['item']['cont7'])
    print(jsonObj['response']['body']['item']['imgUrl'])
    print(jsonObj['response']['body']['item']['insctOfnmKrlngNm'])
    con = pymysql.connect(host='10.10.21.103', user='root', password='00000000',
                          db='education_app', charset='utf8')
    with con:
        with con.cursor() as cur:
            sql = f"INSERT INTO 학습자료 values('곤충','{jsonObj['response']['body']['item']['insctOfnmKrlngNm']}',\
            '{jsonObj['response']['body']['item']['cont1']}','{jsonObj['response']['body']['item']['cont7']}',\
            '{jsonObj['response']['body']['item']['imgUrl']}')"
            cur.execute(sql)
            con.commit()
