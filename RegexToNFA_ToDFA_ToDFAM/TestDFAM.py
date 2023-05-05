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




# read regular expression from JSON file
with open('regex.json', 'r') as f:
    regex_dict = json.load(f)
    regex = regex_dict['regex']

# ask user to enter word to test
word = input("Enter a word to test: ")

# test word against regular expression
if re.fullmatch(regex, word):
    print("Word is accepted by the regular expression!")
else:
    print("Word is not accepted by the regular expression.")



