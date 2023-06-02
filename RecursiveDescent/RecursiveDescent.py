#Parsing using recursive descent
#Синтаксический разбор с использованием метода рекурсивного спуска

#Вариант 1. Грамматика G1

# Terminal: a b not or div mod and ( ) = <> < <= > >= + - * / 

# Non Terminal: S Z H T K C Y F 

#  Grammar: 
#  S -->  Z  |  Z H Z
#  Z --> T | K T | Z C T
#  T --> F | T Y F
#  F --> a | b | ( < Z > ) | not F
#  H --> = | <> | < | <= | > | >=
#  K --> + | -
#  C --> + | - | or
#  Y --> * | / | div | mod | and 

print("\nТерминал: a b not or div mod and ( ) = <> < <= > >= + - * /")
print("Не Терминал: S Z H T K C Y F \n")
print("Вариант 1. Грамматика G1:\n")
print("S -->  Z  |  Z H Z")
print("Z --> T | K T | Z C T")
print("T --> F | T Y F")
print("F --> a | b | ( < Z > ) | not F")
print("H --> = | <> | < | <= | > | >=")
print("K --> + | -")
print("C --> + | - | or")
print("Y --> * | / | div | mod | and")
print("\n")
import re

rules = {
    'S': ['Z', 'ZHZ'],
    'Z': ['T', 'KT', 'ZCT'],
    'T': ['F', 'TYF'],
    'F': ['a', 'b', '(<Z>)', 'not F'],
    'H': ['=', '<>', '<', '<=', '>', '>='],
    'K': ['+', '-'],
    'C': ['+', '-', 'or'],
    'Y': ['*', '/', 'div', 'mod', 'and']
}

class Parser:
    def __init__(self, input_string):
        self.tokens = input_string.split()
        self.current_token = None

    def parse(self):
        self.current_token = self.get_next_token()
        self.S()

        if self.current_token is not None:
            print("Ошибка: неожиданный токен:", self.current_token)
        else:
            print("Парсинг выполнен успешно")

    def get_next_token(self):
        if self.tokens:
            return self.tokens.pop(0)
        return None

    def match(self, expected_token):
        if self.current_token == expected_token:
            self.current_token = self.get_next_token()
        else:
            print("Ошибка: ожидаемый токен:", expected_token)

    def S(self):
        if self.current_token in ['a', 'b', '(', 'not']:
            self.Z()

        while self.current_token in ['=', '<>', '<', '<=', '>', '>=', '+', '-']:
            self.H()
            self.Z()

    def Z(self):
        if self.current_token in ['a', 'b', '(', 'not']:
            self.T()

        while self.current_token in ['+', '-', 'or']:
            self.C()
            self.T()

    def T(self):
        if self.current_token in ['a', 'b', '(', 'not']:
            self.F()

        while self.current_token in ['*', '/', 'div', 'mod', 'and']:
            self.Y()
            self.F()

    def F(self):
        if self.current_token == 'a':
            self.match('a')
        elif self.current_token == 'b':
            self.match('b')
        elif self.current_token == '(':
            self.match('(')
            self.match('<')
            self.Z()
            self.match('>')
            self.match(')')
        elif self.current_token == 'not':
            self.match('not')
            self.F()
        else:
            print("Ошибка: неожиданный токен:", self.current_token)

    def H(self):
        if self.current_token in ['=', '<>', '<', '<=', '>', '>=']:
            self.match(self.current_token)
        else:
            print("Ошибка: неожиданный токен:", self.current_token)

    def K(self):
        if self.current_token in ['+', '-']:
            self.match(self.current_token)
        else:
            print("Ошибка: неожиданный токен:", self.current_token)

    def C(self):
        if self.current_token in ['+', '-', 'or']:
            self.match(self.current_token)
        else:
            print("Ошибка: неожиданный токен:", self.current_token)

    def Y(self):
        if self.current_token in ['*', '/', 'div', 'mod', 'and']:
            self.match(self.current_token)
        else:
            print("Ошибка: неожиданный токен:", self.current_token)


while True:
    input_string = input("\nВведите выражение\n >> (или 0 выйти): ")

    if input_string == "0":
        break

    parser = Parser(input_string)
    parser.parse()


# Examples for Testing:
# not a and b or a
# a + b * a
# a < b and a >= b
# ( < a > )          acc
# a = b or c     acc 
# a = b + * c           n acc