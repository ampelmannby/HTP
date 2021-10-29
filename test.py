import time

class User:
    def __init__(self, name: str, number: int):
        self.name = name
        print(f'I am User {self.name=}.')
        for i in range(number):
            print(number)
            number -= 1
            time.sleep(1)

user = dict()
names = ('Misha', 'Masha', 'Lev')

for i in range(1,4):
    user[i] = User(names[i-1], i*3)

