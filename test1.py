import string
import random

test_dic = {}

test_dic[0] = ["this is title", "this very interesting value"]


print(test_dic.get(0))

random_letter = random.choice(list(string.ascii_lowercase))

print(random_letter)


