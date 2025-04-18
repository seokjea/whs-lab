# pip install requests
# 혹은
# poetry add requests
import requests

url = 'http://board.nyan101.com/sample/list'
response = requests.get(url)
print(response.text)
