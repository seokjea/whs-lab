import requests
from pprint import pprint

url = f'http://board.nyan101.com/comments/1'
response = requests.get(url)

# response.json()은 왜 .text, .content와 다르게 함수일까요?
comments = response.json()

pprint(comments)
