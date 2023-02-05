# import requests
#
# key = f"3R%2BSur%2BruWT%2F2MXwVvEJR5V39S2A5QoImBYPWyzEESJt5WwC4MEVIV5JacV50D97kscWEykWIPpB08XmaHpgnA%3D%3D"
# url = f"http://openapi.nature.go.kr/openapi/service/rest/InsectService/isctPrtctList?serviceKey={key}"
#
#
#
#
#
# content = requests.get(url).content
#
#
# print(content)


# Python3 샘플 코드 #


# import requests, xmltodict, json
#
#
# key = '3R%2BSur%2BruWT%2F2MXwVvEJR5V39S2A5QoImBYPWyzEESJt5WwC4MEVIV5JacV50D97kscWEykWIPpB08XmaHpgnA%3D%3D'
# url = 'http://openapi.nature.go.kr/openapi/service/rest/InsectService/isctPrtctList'
# params ={'serviceKey' : key }
#
# content = requests.get(url, params=params).content
# dict = xmltodict.parse(content)
# print(len(dict))
# jsonString = json.dumps(dict['response']['body']['items'], ensure_ascii=False)
# jsonObj = json.loads(jsonString)
# # print(jsonString)
# print(len(jsonString))
#
# for i in jsonObj['item']:
#     print(i)
# for i in jsonObj['item']:
#     print(i['insctFamilyNm'])
#
#
#
#
# url = 'http://openapi.nature.go.kr/openapi/service/rest/InsectService/isctIlstrSearch'
# params ={'serviceKey' : '서비스키', 'st' : '1', 'sw' : '밤나방', 'numOfRows' : '10', 'pageNo' : '1' }
#
# content_two = requests.get(url, params=params).content
# dict_two = xmltodict.parse(content_two)
# jsonString_two = json.dumps(dict_two[])



# Python3 샘플 코드 #


# import requests
# key = '3R%2BSur%2BruWT%2F2MXwVvEJR5V39S2A5QoImBYPWyzEESJt5WwC4MEVIV5JacV50D97kscWEykWIPpB08XmaHpgnA%3D%3D'
# url = 'http://apis.data.go.kr/1400119/MammService/mammSpcmSearch'
# params ={'serviceKey' : key, 'st' : '1', 'sw' : '호', 'numOfRows' : '10', 'pageNo' : '1' }
#
# response = requests.get(url, params=params)
# print(response.content)


# import json
# import requests
# import xmltodict
# from bs4 import BeautifulSoup
#
# # 인증키 저장
# key = "11xBqPRCrKxDRnzolBiWVGwhexbmYELfieu+GvVw7z2HYGWD67SB2EGIMJHoG8KYEvkNOd3LaHsvIp7cDZPhzg=="
#
# # 인증키 정보가 들어간 url 저장
# url = f'http://openapi.nature.go.kr/openapi/service/rest/InsectService/isctPrtctList?serviceKey={key}'
#
#
# content = requests.get(url).content                     # request 모듈을 이용해서 정보 가져오기(byte형태로 가져와지는듯)
# dict = xmltodict.parse(content)                         # xmltodict 모듈을 이용해서 딕셔너리화 & 한글화
# jsonString = json.dumps(dict, ensure_ascii=False)       # json.dumps를 이용해서 문자열화(데이터를 보낼때 이렇게 바꿔주면 될듯)
# jsonObj = json.loads(jsonString)                        # 데이터 불러올 때(딕셔너리 형태로 받아옴)
#
# for item in jsonObj['response']['body']['items']['item']:
#     # print(item)
#     print(item['imgUrl'], item['insctFamilyNm'], item['insctOfnmScnm'],
#           item['insctPcmtt'], item['insctPilbkNo'], item['insctofnmkrlngnm'])



# import requests
# import xmltodict
# import json
# key = '11xBqPRCrKxDRnzolBiWVGwhexbmYELfieu+GvVw7z2HYGWD67SB2EGIMJHoG8KYEvkNOd3LaHsvIp7cDZPhzg=='
# url = f'http://apis.data.go.kr/1400119/MammService/mammSpcmInfo?serviceKey={key}&q1=KNAM-MM-0000126'
#
# content = requests.get(url).content                     # request 모듈을 이용해서 정보 가져오기(byte형태로 가져와지는듯)
# dict = xmltodict.parse(content)                         # xmltodict 모듈을 이용해서 딕셔너리화 & 한글화
# jsonString = json.dumps(dict, ensure_ascii=False)       # json.dumps를 이용해서 문자열화(데이터를 보낼때 이렇게 바꿔주면 될듯)
# jsonObj = json.loads(jsonString)
#
# for item in jsonObj['response']['body']['items']['item']:
#     # print(item)
#     print(item['imgUrl'], item['insctFamilyNm'], item['insctOfnmScnm'],
#           item['insctPcmtt'], item['insctPilbkNo'], item['insctofnmkrlngnm'])


# import requests
# import xmltodict
# import json
# key = '11xBqPRCrKxDRnzolBiWVGwhexbmYELfieu+GvVw7z2HYGWD67SB2EGIMJHoG8KYEvkNOd3LaHsvIp7cDZPhzg=='
# url = f'http://apis.data.go.kr/1400119/MammService/mammSpcmSearch?serviceKey={key}'
#
# # params ={'serviceKey' : key, 'st' : '1', 'sw' : '호', 'numOfRows' : '10', 'pageNo' : '1' }
#
# content = requests.get(url).content                     # request 모듈을 이용해서 정보 가져오기(byte형태로 가져와지는듯)
# dict = xmltodict.parse(content)                         # xmltodict 모듈을 이용해서 딕셔너리화 & 한글화
# jsonString = json.dumps(dict, ensure_ascii=False)       # json.dumps를 이용해서 문자열화(데이터를 보낼때 이렇게 바꿔주면 될듯)
# jsonObj = json.loads(jsonString)                        # 데이터 불러올 때(딕셔너리 형태로 받아옴)
#
# for item in jsonObj['response']['body']['items']['item']:
#     # print(item)
#     print(item['imgUrl'], item['insctFamilyNm'], item['insctOfnmScnm'],
#           item['insctPcmtt'], item['insctPilbkNo'], item['insctofnmkrlngnm'])
#
import json
import requests
import xmltodict
from bs4 import BeautifulSoup

# 인증키 저장
key = "jAB8gOQ%2BEjRxryPTRcGIWjS6sTl2FCowle%2Bb%2FVaRrcoCuQZTgCIEID85tLqWiPIfuY4%2FzUsqf81dQj6dYuTyYg%3D%3D"

# 인증키 정보가 들어간 url 저장
url = f'http://openapi.nature.go.kr/openapi/service/rest/InsectService/isctPrtctList?serviceKey={key}'


content = requests.get(url).content                     # request 모듈을 이용해서 정보 가져오기(byte형태로 가져와지는듯)
dict = xmltodict.parse(content)                         # xmltodict 모듈을 이용해서 딕셔너리화 & 한글화
jsonString = json.dumps(dict, ensure_ascii=False)       # json.dumps를 이용해서 문자열화(데이터를 보낼때 이렇게 바꿔주면 될듯)
jsonObj = json.loads(jsonString)                        # 데이터 불러올 때(딕셔너리 형태로 받아옴)

for item in jsonObj['response']['body']['items']['item']:
    # print(item)
    print(item['imgUrl'], item['insctFamilyNm'], item['insctOfnmScnm'],
          item['insctPcmtt'], item['insctPilbkNo'], item['insctofnmkrlngnm'])