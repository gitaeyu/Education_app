# 모듈 import
import requests
import pprint
import pandas as pd
import bs4
import xml
a= input("검색어를 입력해주세요")
#인증키 입력
encoding = '11xBqPRCrKxDRnzolBiWVGwhexbmYELfieu%2BGvVw7z2HYGWD67SB2EGIMJHoG8KYEvkNOd3LaHsvIp7cDZPhzg%3D%3D'
decoding = '11xBqPRCrKxDRnzolBiWVGwhexbmYELfieu+GvVw7z2HYGWD67SB2EGIMJHoG8KYEvkNOd3LaHsvIp7cDZPhzg=='
url = 'http://apis.data.go.kr/1400119/MammService/mammIlstrSearch'
params ={'serviceKey' : '11xBqPRCrKxDRnzolBiWVGwhexbmYELfieu+GvVw7z2HYGWD67SB2EGIMJHoG8KYEvkNOd3LaHsvIp7cDZPhzg==', 'st' : '1', 'sw' : a ,'numOfRows' : '10', 'pageNo' : '1' }
response = requests.get(url, params=params)
# xml 내용
content = response.text
# 깔끔한 출력 위한 코드
pp = pprint.PrettyPrinter(indent=4)
#bs4 사용하여 item 태그 분리
xml_obj = bs4.BeautifulSoup(content,'lxml-xml')
rows = xml_obj.findAll('item')
# 컬럼 값 조회용
columns = rows[0].find_all()
# 각 행의 컬럼, 이름, 값을 가지는 리스트 만들기
row_list = [] # 행값
name_list = [] # 열이름값
value_list = [] #데이터값

# xml 안의 데이터 수집
for i in range(0, len(rows)):
    columns = rows[i].find_all()
    #첫째 행 데이터 수집
    for j in range(0,len(columns)):
        if i ==0 :
            # 컬럼 이름 값 저장
            name_list.append(columns[j].name)
        if j == 0 or j ==2 :
            # 컬럼의 각 데이터 값 저장
            value_list.append(columns[j].text)
        # 각 행의 value값 전체 저장
            row_list.append(value_list)
    # 데이터 리스트 값 초기화
    value_list=[]
print(name_list)
#xml값 DataFrame으로 만들기
df = pd.DataFrame(row_list, columns=['anmlGnrlNm','anmlSpecsId'])
print(df.head(200))

q1 = input("anmlSpecsId 를 입력해주세요")

url = 'http://apis.data.go.kr/1400119/MammService/mammIlstrInfo'
params ={'serviceKey' : decoding, 'q1' : q1 }

response = requests.get(url, params=params)
print(response.content)
# xml 내용
content = response.text

#bs4 사용하여 item 태그 분리

xml_obj = bs4.BeautifulSoup(content,'lxml-xml')
rows = xml_obj.findAll('item')
# xml 안의 데이터 수집
row_list = [] # 행값
name_list = [] # 열이름값
value_list = [] #데이터값
for i in range(0, len(rows)):
    columns = rows[i].find_all()
    #첫째 행 데이터 수집
    for j in range(0,len(columns)):
        if i ==0 :
            # 컬럼 이름 값 저장
            name_list.append(columns[j].name)
        if j == 6 or j ==15 or j ==16 or j ==17 : # 원하는 컬럼 데이터
            # 컬럼의 각 데이터 값 저장
            value_list.append(columns[j].text)
        # 각 행의 value값 전체 저장
            row_list.append(value_list)
    # 데이터 리스트 값 초기화
    value_list=[]
print(name_list)
pd.set_option('display.width', 1000)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
#xml값 DataFrame으로 만들기
df = pd.DataFrame(row_list, columns=['anmlGnrlNm','eclgDpftrCont','gnrlSpftrCont','imgUrl'])
# print(df.head(10))
print(df.iloc[0]['eclgDpftrCont'])
print("나이스")
print(df.iloc[0]['gnrlSpftrCont'])
print(df.iloc[0]['imgUrl'])