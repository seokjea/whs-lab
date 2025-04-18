import requests
from bs4 import BeautifulSoup
from pprint import pprint

total_titles = []
num_pages = 10
for page in range(1, num_pages + 1):
    print(f'[+] load page {page}...')
    url = f'http://board.nyan101.com/list/{page}'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # CSS 선택자를 사용하여 게시글 목록 추출
    posts = soup.select('body > div > div.bg-white.rounded-lg.shadow-md.p-6 > ul')[0]

    # 게시글 목록에서 제목 추출
    titles = posts.select('li > a > div > h3')
    total_titles.extend(titles)

pprint(total_titles)
print(f'[+] get {len(total_titles)} posts')
