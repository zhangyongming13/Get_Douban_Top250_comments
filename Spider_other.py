import json


with open('comments.json', 'r')as f:
    yong = json.load(f)
    print(yong['html'])
