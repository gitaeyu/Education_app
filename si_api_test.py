#api DB 저장
import requests
import pymysql
import xmltodict
import json
key = '3R%2BSur%2BruWT%2F2MXwVvEJR5V39S2A5QoImBYPWyzEESJt5WwC4MEVIV5JacV50D97kscWEykWIPpB08XmaHpgnA%3D%3D'
url = f'http://openapi.nature.go.kr/openapi/service/rest/InsectService/isctPrtctList?serviceKey={key}'
# conn = pymysql.connect(host='10.10.21.103', port=3306, user='root', password='00000000', db='education_app',
#                                     charset='utf8')
# cursor = conn.cursor()
content = requests.get(url).content                     # request 모듈을 이용해서 정보 가져오기(byte형태로 가져와지는듯)
dict = xmltodict.parse(content)                         # xmltodict 모듈을 이용해서 딕셔너리화 & 한글화
jsonString = json.dumps(dict, ensure_ascii=False)       # json.dumps를 이용해서 문자열화(데이터를 보낼때 이렇게 바꿔주면 될듯)
jsonObj = json.loads(jsonString)                        # 데이터 불러올 때(딕셔너리 형태로 받아옴)

item_list = []

for item in jsonObj['response']['body']['items']['item']:
    temp_list=['곤충',item['insctofnmkrlngnm'],'','',item['imgUrl'],item['insctPilbkNo']]
    item_list.append(temp_list)


key = '3R%2BSur%2BruWT%2F2MXwVvEJR5V39S2A5QoImBYPWyzEESJt5WwC4MEVIV5JacV50D97kscWEykWIPpB08XmaHpgnA%3D%3D'
url = 'http://openapi.nature.go.kr/openapi/service/rest/InsectService/isctIlstrInfo'

for i in item_list:
    params = {'serviceKey': key, 'q1': i[5]}
    content = requests.get(url, params=params).content
    dict = xmltodict.parse(content)  # xmltodict 모듈을 이용해서 딕셔너리화 & 한글화
    jsonString = json.dumps(dict, ensure_ascii=False)  # json.dumps를 이용해서 문자열화(데이터를 보낼때 이렇게 바꿔주면 될듯)
    jsonObj = json.loads(jsonString)
    i[2] = jsonObj['response']['body']['item']['cont7']
    if i[2] == None:
        i[2] = '일반적인 생태적 특징은 잘 알려지지 않았다.'
    i[3] = jsonObj['response']['body']['item']['cont1']
#     cursor.execute(f"insert into 학습자료 values ('{i[0]}','{i[1]}','{i[2]}','{i[3]}','{i[4]}')")
# conn.commit()
# conn.close()
