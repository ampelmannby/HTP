import time
from enum import Enum

class Market(Enum):
    USDCAD = 'Bla'
    US30 = 'US30'
    USDJPY = 'USDJPY'
    def __init__(self):
        self.



user = Market('Bla')
print(user.US30)
print(user)


# class User:
#     def __init__(self, name: str, number: int):
#         self.name = name
#         self.number = number
#         print(f'I am User No.{self.number}, my name is {self.name}.')
#
#
# user = dict()
# names = ('Misha', 'Masha', 'Lev')
#
# for i in range(len(names)):
#     user[i] = User(names[i], i+1)


"""{
  "FirstName": "Kirill",
  "LastName": "Zalessky",
  "Age": 41,
  "Smoking": null,
  "Address": {
    "City": "Minsk",
    "Street": "Bogdanovicha",
    "Building": 86,
    "APT": 235
  }
}""" => dict()

