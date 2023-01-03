# from googletrans import Translator
# from faker import Faker
#
# faker = Faker()
# translator = Translator()
# word1 = faker.word()
# print(word1)
# tr = translator.translate(str(word1), src="en", dest="ru")
# word2 = tr.text
# print(word2)
# f = ["aeg", 'ef', "r"]
# a = f.pop(1)
# print(a)


import re
import json

# sampleJson = """{
#    "company":{
#       "employee":{
#          "name":"emma",
#          "payble":{
#             "salary":7000,
#             "bonus":800
#          }
#       }
#    }
# }"""
#
# py_dict = json.loads(sampleJson)
# print(py_dict['company']['employee']["payble"]["salary"])

# a = "sdf       sfsf"
# a = a.split(" ")
# print(a)
# print(type(a))
# if type(a) is list:
#     print("GF")

# import re
#
# def normalize_word(word):
#     pattern = r", *"
#     word = re.sub(pattern, ", ", word)
#     return word.strip(" ").strip(",")
#
# print(normalize_word("wefwef,     wdg,wfgw, w, ").split(", "))
#
# s = "fescds"
# print(s.split(","))

# listt = ["wd", "wf"]

# a = listt.pop()
# print(listt)
# print(a)
#
# listt[0] = 1
# print(listt)

# import requests
#
# req = requests.post('http://127.0.0.1:8000/words/delete/bbecd282-02ad-4a7f-ab18-4d7718226f34/',
#                     data={"csrfmiddlewaretoken": 'JXGrHZgfjfOddi8naH3ZiC0SCNcWm0cAcebcFsop3F3wgmqhzOgRaClj3zX48aIc'},
#                     cookies={"csrftoken": "kj6la9ioLbRbRyEtifS8FlJZdN8Wz5Z8NAB68CqyvB6uUCWnHm50xl4qEzT4lfvK"})
# print(req.text)
# print(req.status_code)
# print(req.reason)
print({} == False)

print({'d': 'f'} == dict())
