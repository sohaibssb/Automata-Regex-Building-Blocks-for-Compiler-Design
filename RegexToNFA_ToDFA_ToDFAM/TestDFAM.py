import re
import json

with open('regex.json', 'r') as f:
    regex_dict = json.load(f)
    regex = regex_dict['regex']


word = input("Введите слово для проверки: ")

if re.match(regex, word):

    print("Слово принимается регулярным выражением!")
else:
    print("Слово не принимается регулярным выражением!")



with open('regex.json', 'r') as f:
    regex_dict = json.load(f)
    regex = regex_dict['regex']


word = input("Enter a word to test: ")


if re.fullmatch(regex, word):
    print("Word is accepted by the regular expression!")
else:
    print("Word is not accepted by the regular expression.")



