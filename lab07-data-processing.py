from tqdm import tqdm
import requests
from pprint import pprint

total_comments = []
num_posts = 100
for post_id in tqdm(range(1, num_posts + 1)):
    url = f'http://board.nyan101.com/comments/{post_id}'
    response = requests.get(url)
    comments = response.json()
    total_comments.extend(comments)

print(f'[+] get {len(total_comments)} comments')
print()

# 댓글 데이터 처리
# 계정별 댓글 목록 정리용
print(f'[+] processing...')
user_comments = {}
for comment in total_comments:
    author_id = comment['author_id']
    # 해당 댓글이 처음 등장한 경우 빈 리스트 초기화
    if author_id not in user_comments:
        user_comments[author_id] = []
    user_comments[author_id].append(comment)

# 계정 목록 출력
print(f'[+] get {len(user_comments.keys())} users')
print(f'[+] users : {user_comments.keys()}')
print()
# 첫 계정이 작성한 댓글 목록 출력
user_id = list(user_comments.keys())[0]
print(f'[+] User #{user_id} wrote {len(user_comments[user_id])} comments')
print(f'[+] example comments :')
pprint(user_comments[user_id][:3])
print()
