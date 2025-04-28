from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from pprint import pprint
import time

# 웹드라이버 설정 (headless 모드 + 직접 설치한 chromedriver 사용)
chrome_options = Options()
chrome_options.add_argument('--headless')   # WSL 필수
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

# chromedriver 경로 직접 지정
service = Service(executable_path="/usr/bin/chromedriver")

driver = webdriver.Chrome(service=service, options=chrome_options)

# 게시글 페이지 로드
driver.get('http://board.nyan101.com/post/1')

# 댓글이 동적으로 로딩될 때까지 기다릴 여유시간 설정(10초)
driver.implicitly_wait(10)

# 댓글 목록 추출
comments = driver.find_elements(By.CLASS_NAME, 'comment')

for comment in comments:
    print(comment.text)
    author = comment.find_element(By.CLASS_NAME, 'comment-author-name').text
    print(f'[+] 추출된 author-name: {author}')
    print()

# 즉시 종료 방지용
time.sleep(3)

