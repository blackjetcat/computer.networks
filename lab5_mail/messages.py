"""
Класс, описывабщий сообщение
"""


class Message:
    def __init__(self, date, sender, receiver, text, owner=None):
        self.date = date
        self.owner = owner
        self.sender = sender
        self.receiver = receiver
        self.message = text

    def printm(self, login):
        if login == self.receiver:
            print('Вам от пользователя', self.sender)
            print('     ', self.message)
        elif login == self.sender:
            print('Вы пользователю', self.receiver)
            print('     "', self.message, '"')


def print_messages(pull, login):
    if not pull:
        print('Не найдено сообщений')
        return
    print('--------------------')
    for i in pull:
        tmp = Message(i[0], i[2], i[3], i[4], i[1])
        tmp.printm(login)
        print('--------------------')