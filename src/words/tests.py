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

listt = ["wd", "wf"]

# a = listt.pop()
# print(listt)
# print(a)

listt[0] = 1
print(listt)