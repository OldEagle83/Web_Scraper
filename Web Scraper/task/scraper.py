import requests
import json

#url = 'http://api.quotable.io/quotes/-4WQ_JwFWI'
e_msg0 = 'Invalid quote resource!'


def quoteContent(url):
    r = requests.get(url)
    try:
        return r.json()['content']
    except:
        return e_msg0

print(quoteContent(input()))